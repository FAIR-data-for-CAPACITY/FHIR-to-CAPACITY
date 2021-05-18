# -*- coding: utf-8 -*-
import logging

import redcap
from fhirclient.models.patient import Patient
from fhirclient.server import FHIRServer

from capacity_mapping.codebook import Capacity

logger = logging.getLogger(__name__)


def map_patient(patient: Patient) -> dict:
    # TODO: subjid, sex, age_estimateyears, age_estimateyearsu, ethnic,
    #  other_ethnic
    return {
        Capacity.patient_id.name: patient.id,
        Capacity.sex.name: Capacity.sex.mapping[patient.gender]
    }


def fhir_to_capacity(fhir_base_url, capacity_url, capacity_token):
    logger.info('Mapping all patients in FHIR server at %s to redcap server '
                'at %s', fhir_base_url, capacity_url)

    # Query all patients on fhir server
    fhir_server = FHIRServer(None, fhir_base_url)

    logger.info('Querying patients')
    search = Patient.where({})
    patients = search.perform_resources(fhir_server)

    logger.info('Mapping patients')
    mapped = [map_patient(patient) for patient in patients]

    logger.info('Uploading patients')
    project = redcap.Project(capacity_url, capacity_token)
    project.import_records(mapped)
