from fhirclient.models.patient import Patient
from capacity_mapping import mapping


def test_map_patient_maps_gender():
    patient = Patient()
    patient.gender = 'male'

    mapped = mapping.map_patient(patient)

    assert mapped['sex'] == 1
