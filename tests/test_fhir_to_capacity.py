from fhirclient.models.patient import Patient
from capacity_mapping import fhir_to_capacity


def test_map_patient_maps_gender():
    patient = Patient()
    patient.gender = 'male'

    mapped = fhir_to_capacity.map_patient(patient)

    assert mapped['sex'] == 1
