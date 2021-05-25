# -*- coding: utf-8 -*-
import logging
from typing import List, Dict

import redcap
from dateutil.relativedelta import relativedelta
from fhirclient.models.encounter import Encounter
from fhirclient.models.patient import Patient

from capacity_mapping.codebook import Capacity
from capacity_mapping.fhir import FHIRWrapper

logger = logging.getLogger(__name__)
DATE_FORMAT = '%Y-%m-%d'


def map_patient(patient: Patient, encounters: List[Encounter] = None) -> dict:
    # TODO: For now assuming one encounter
    # TODO: Should I query encounters first instead of patients?
    # TODO: For now I'm skipping patients without encounters
    age = None
    age_unit = None
    admission_date = None

    if encounters:
        encounter = encounters[0]

        age, age_unit = get_patient_age(encounter, patient)

        admission_date = encounter.period.start.date.strftime(DATE_FORMAT)

    return {
        Capacity.patient_id.name: patient.id,
        Capacity.sex.name: Capacity.sex.mapping[patient.gender],
        Capacity.age_estimateyears.name: age,
        Capacity.age_estimateyearsu.name: age_unit,
        Capacity.admission_date.name: admission_date,
        Capacity.admission_any_date.name: admission_date
    }


def get_patient_age(encounter, patient):
    """
    Determines patient age at time of encounter

    :param encounter:
    :param patient:
    :return:
    """
    admission_date = encounter.period.start.date
    # Relativedelta takes leap years into account and gives correct age
    age_delta = relativedelta(admission_date, patient.birthDate.date)

    if age_delta.years < 1:
        age = age_delta.months
        age_unit = Capacity.age_estimateyearsu.mapping['months']
    else:
        age = age_delta.years
        age_unit = Capacity.age_estimateyearsu.mapping['years']

    return age, age_unit


def map_all_patients(patient_records: Dict[str, dict]):
    success = 0
    fails = 0
    for record in patient_records.values():
        try:
            yield map_patient(**record)
            success += 1
        except Exception as e:
            logger.error('Could not map patient %s, reason: %s',
                         record['patient'].relativePath(), e)
            fails += 1

    logger.info('Transformed %i records', success)
    logger.info('Failed to transform %i records', fails)


def fhir_to_capacity(fhir_base_url, capacity_url, capacity_token):
    logger.info('Mapping all patients in FHIR server at %s to redcap server '
                'at %s', fhir_base_url, capacity_url)

    # Query all patients on fhir server
    fhir_wrapper = FHIRWrapper(fhir_base_url)

    logger.info('Querying patients')

    patient_records = query_patient_related_data(fhir_wrapper)

    print(patient_records)

    logger.info('Mapping patients')
    mapped = list(map_all_patients(patient_records))

    logger.info('Uploading patients')
    project = redcap.Project(capacity_url, capacity_token)
    project.import_records(mapped)


def query_patient_related_data(fhir_wrapper):
    patients = fhir_wrapper.get_patients()
    encounters = fhir_wrapper.get_encounters()

    # Create dictionary mapping patient id to resources

    patient_records = \
        {patient.relativePath(): {'patient': patient} for patient in patients}

    # Add encounters to the dict
    for encounter in encounters:

        if encounter.subject is not None:
            patient_reference = encounter.subject.processedReferenceIdentifier()

            if patient_reference in patient_records.keys():
                # There could be more than one encounter per patient. Add the new
                # encounter to the existing list if it exists.
                patient_records[patient_reference]['encounters'] = \
                    patient_records[patient_reference].get('encounters', []) + [encounter]

            else:
                logger.warning('Patient id %s not found for some reason', patient_reference)

    return patient_records
