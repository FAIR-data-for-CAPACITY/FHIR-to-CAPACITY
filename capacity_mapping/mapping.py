# -*- coding: utf-8 -*-
"""
Mapping module

This module contains the code that maps
"""
import logging
import traceback
from typing import List, Dict, Any, Tuple, Iterable

import redcap
from dateutil.relativedelta import relativedelta
from fhirclient.models.encounter import Encounter
from fhirclient.models.patient import Patient

from capacity_mapping.codebook import Capacity
from capacity_mapping.fhir import FHIRWrapper

logger = logging.getLogger(__name__)
DATE_FORMAT = '%Y-%m-%d'


def map_patient(patient: Patient, encounters: List[Encounter] = None) -> List[Dict[str, Any]]:
    # TODO: For now assuming one encounter
    # TODO: Should I query encounters first instead of patients?
    # TODO: For now I'm skipping patients without encounters
    age = None
    age_unit = None
    admission_date = None

    outcome_date = None
    outcome_date_known = False

    # If there is a specific patient id, use that, otherwise use FHIR id
    patient_id = patient.id

    if patient.identifier:
        patient_id = patient.identifier[0].id

    if encounters:
        encounter = encounters[0]

        age, age_unit = get_patient_age(patient, encounter)
        admission_date = encounter.period.start.date.strftime(DATE_FORMAT)

        if encounter.period.end:
            outcome_date = encounter.period.end.date.strftime(DATE_FORMAT)
            outcome_date_known = True

    capacity_patient = Capacity(patient_id, sex=patient.gender, age_estimateyears=age,
                                age_estimateyearsu=age_unit, admission_date=admission_date,
                                admission_any_date=admission_date,
                                outcome_date_known=outcome_date_known,
                                outcome_date=outcome_date)

    return capacity_patient.to_records()


def get_patient_age(patient: Patient, encounter: Encounter) -> Tuple[int, int]:
    """
    Determines patient age at time of encounter.

    If the patient was younger than a year at the time, the age will be expressed in months.
    Otherwise the unit will be in years.

    :param encounter: an encounter referring to the patient.
    :param patient: a patient resource
    :return: a tuple containing age, age_unit
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


def map_all_patients(patient_records: Dict[str, dict]) -> Iterable[Dict[str, Any]]:
    """
    Takes a dict filled with patient records and maps them to CAPACITY records.

    The patient records are structured as follows:

    { 'PATIENT_ID': {'patient': PATIENT_OBJECT, 'encounters': [ENCOUNTER1, ENCOUNTER2]}, ...}

    :param patient_records: a dict mapping patient ids to the linked FHIR resources as follows:
                            { 'PATIENT_ID': {'patient': PATIENT_OBJECT,
                             'encounters': [ENCOUNTER1, ENCOUNTER2]}, ...}
    :return: a generator containing Capacity records
    """
    success = 0
    fails = 0
    for record in patient_records.values():
        try:
            yield from map_patient(**record)
            success += 1
        except Exception as e:
            logger.error('Could not map patient %s, reason: %s',
                         record['patient'].relativePath(), e)
            traceback.print_exc()

            fails += 1

    logger.info('Transformed %i records', success)
    logger.info('Failed to transform %i records', fails)


def fhir_to_capacity(fhir_base_url: str, capacity_url: str, capacity_token: str) -> None:
    """
    Retrieve records from FHIR endpoint, convert the data to conform to the CAPACITY codebook,
    and upload it to the CAPACITY registry.
    :param fhir_base_url: the base API url of the FHIR endpoint
    :param capacity_url: the base API url of the CAPACITY registry
    :param capacity_token: authentication token for CAPACITY registry
    """
    logger.info('Mapping all patients in FHIR server at %s to redcap server '
                'at %s', fhir_base_url, capacity_url)

    # Query all patients on fhir server
    fhir_wrapper = FHIRWrapper(fhir_base_url)

    logger.info('Querying patients')

    patient_records = query_patient_related_data(fhir_wrapper)

    logger.info('Mapping patients')
    mapped = list(map_all_patients(patient_records))

    logger.info('Uploading patients')
    project = redcap.Project(capacity_url, capacity_token)
    project.import_records(mapped)


def query_patient_related_data(fhir_wrapper:FHIRWrapper) -> Dict[str, Dict[str, Any]]:
    """
    Query all patient related data. As of now, this data is contained withing Encounter and
    related Patient resources.

    The data will be returned as a Dict that maps patient ids to a dict containing all related
    FHIR resources.

    :param fhir_wrapper: fhir wrapper instance connected to the FHIR endpoint.
    :return: a Dict mapping patient ids to all related resources as follows:
                 { 'PATIENT_ID':
                    {'patient': PATIENT_OBJECT, 'encounters': [ENCOUNTER1, ENCOUNTER2]}, ...}
    """
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
