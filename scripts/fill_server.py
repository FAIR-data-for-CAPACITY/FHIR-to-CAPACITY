#! /usr/bin/env python3
"""
# `fill_server.py`
This script is meant to be used for testing purposes only! I creates a bunch
of resources on a fhir server that can be used to test the mappings.
"""
import random

from clize import run
from fhirclient.models.encounter import Encounter
from fhirclient.models.patient import Patient
from fhirclient.server import FHIRServer
from fhirclient.models.fhirreference import FHIRReference

from capacity_mapping.codebook import Capacity

DEFAULT_NUM_PATIENTS = 10


def fill_server(fhir_base, n=DEFAULT_NUM_PATIENTS):
    """
    Fills the server with n ramdom patients.
    :param fhir_base: the url to the FHIR api
    :param n: number of patients to create
    :return:
    """
    fhir_server = FHIRServer(None, fhir_base)

    patients = create_patients(n)

    for p in patients:
        result_json = p.create(fhir_server)

        created_patient = Patient.with_json(result_json)

        encounter = create_encounter(created_patient)

        encounter.create(fhir_server)


def create_patients(num_patients):
    for _ in range(num_patients):
        p = Patient()
        p.gender = random.choice(list(Capacity.sex.mapping.keys()))
        yield p


def create_encounter(patient: Patient) -> Encounter:
    patient_reference = FHIRReference()
    patient_reference.reference = patient.relativePath()
    encounter = Encounter()
    encounter.subject = patient_reference
    encounter.status = random.choice(['planned', 'arrived', 'triaged',
                                      'in-progress', 'onleave', 'finished',
                                      'cancelled'])
    return encounter


if __name__ == '__main__':
    run(fill_server)
