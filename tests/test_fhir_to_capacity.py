from fhirclient.models.patient import Patient
from capacity_mapping import mapping


def test_map_patient_maps_gender():
    patient = Patient()
    patient.gender = 'male'
    patient.id = '123'

    mapped = mapping.map_patient(patient)

    assert mapped['sex'] == 1
    assert mapped['subjid'] == '123'
