from datetime import date

from fhirclient.models.encounter import Encounter
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.patient import Patient
from fhirclient.models.period import Period

from fhirtocapacity import mapping


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

    mapped_records = mapping.map_patient(patient, encounters=[encounter])

    baseline_capacity = mapped_records[0]
    discharge_capacity = mapped_records[1]

    assert baseline_capacity['sex'] == 1
    assert baseline_capacity['subjid'] == '123'
    assert baseline_capacity['age_estimateyears'] == 31
    assert baseline_capacity['age_estimateyearsu'] == 2
    assert baseline_capacity['admission_date'] == '2021-04-20'
    assert baseline_capacity['admission_any_date'] == '2021-04-20'

    assert discharge_capacity['subjid'] == '123'
    assert discharge_capacity['capdis_outcomedate'] == '2021-05-20'
    assert discharge_capacity['capdis_date']
