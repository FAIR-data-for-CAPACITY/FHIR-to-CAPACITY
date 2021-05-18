# -*- coding: utf-8 -*-
import logging
from capacity_mapping.codebook import Capacity
from fhirclient.models import patient

logger = logging.getLogger(__name__)


def map_patient(patient: patient.Patient) -> dict:
    # TODO: subjid, sex, age_estimateyears, age_estimateyearsu, ethnic,
    #  other_ethnic
    return {
        Capacity.sex.name: Capacity.sex.mapping[patient.gender]
    }
