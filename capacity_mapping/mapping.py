# -*- coding: utf-8 -*-
import logging
import sys

from fhirclient.models.patient import Patient
from fhirclient.server import FHIRServer
import redcap
from capacity_mapping.codebook import Capacity
from clize import run

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


def map_patient(patient: Patient) -> dict:
    # TODO: subjid, sex, age_estimateyears, age_estimateyearsu, ethnic,
    #  other_ethnic
    return {
        Capacity.patient_id.name: patient.id,
        Capacity.sex.name: Capacity.sex.mapping[patient.gender]
    }


def fhir_to_capacity(fhir_base_url, capacity_url, capacity_token):
    logger.info(f'Mapping all patients in FHIR server at {fhir_base_url} to '
                f'redcap server at {capacity_url}')

    # Query all patients on fhir server
    fhir_server = FHIRServer(None, fhir_base_url)
    project = redcap.Project(capacity_url, capacity_token)

    logger.info('Querying patients')
    search = Patient.where({})
    patients = search.perform_resources(fhir_server)

    logger.info('Mapping patients')
    mapped = [map_patient(patient) for patient in patients]

    logger.info('Uploading patients')
    project.import_records(mapped)


if __name__ == '__main__':
    run(fhir_to_capacity)
