from datetime import date

from fhirclient.models.encounter import Encounter
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.patient import Patient
from fhirclient.models.period import Period

from capacity_mapping import mapping


def test_map_patient():
    patient = Patient()
    patient.gender = 'male'
    patient.id = '123'
    patient.birthDate = FHIRDate()
    patient.birthDate.date = date(1990, 1, 2)

    encounter = Encounter()
    encounter.period = Period()
    encounter.period.start = FHIRDate()
    encounter.period.start.date = date(2021, 4, 20)

    encounter.period.end = FHIRDate()
    encounter.period.end.date = date(2021, 5, 20)

    mapped = mapping.map_patient(patient, encounters=[encounter])

    assert mapped['sex'] == 1
    assert mapped['subjid'] == '123'
    assert mapped['age_estimateyears'] == 31
    assert mapped['age_estimateyearsu'] == 2
    assert mapped['admission_date'] == '2021-04-20'
    assert mapped['admission_any_date'] == '2021-04-20'
    assert mapped['capdis_outcomedate'] == '2021-05-20'
    assert mapped['capdis_date']
