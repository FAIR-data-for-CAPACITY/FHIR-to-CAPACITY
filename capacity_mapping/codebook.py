from collections import namedtuple
from typing import Any, Dict, List

Variable = namedtuple('Variable', ['name', 'mapping'])

REDCAP_EVENT_NAME = 'redcap_event_name'

# Unique event names
BASELINE_CAPACITY = 'baseline_capacity_arm_1'
CAPACITY_OUTCOME = 'discharge_capacity_arm_1'


class Capacity:
    sex = Variable('sex', {'male': 1, 'female': 2, 'other': -1, 'unknown': -1, None: -1})
    patient_id = Variable('subjid', None)
    age_estimateyears = Variable('age_estimateyears', None)
    age_estimateyearsu = Variable('age_estimateyearsu', {'months': 1, 'years': 2})
    admission_date = Variable('admission_date', None)
    admission_any_date = Variable('admission_any_date', None)

    # CAPACITY-Discharge
    outcome = Variable('capdis_outcome', {'discharged_alive': 1, 'transfer': 3, 'death': 4,
                                          'palliative_discharge': 5, 'unknown': 6, None: 6})
    outcome_date_known = Variable('capdis_date', {True: 1, False: 2})
    outcome_date = Variable('capdis_outcomedate', None)

    def __init__(self, patient_id, sex=None, age_estimateyears=None, age_estimateyearsu=None,
                 admission_date=None, admission_any_date=None, outcome=None,
                 outcome_date_known=None, outcome_date=None):
        self.patient_id = patient_id
        self.sex = sex
        self.age_estimateyears = age_estimateyears
        self.age_estimateyearsu = age_estimateyearsu
        self.admission_date = admission_date
        self.admission_any_date = admission_any_date
        self.outcome = outcome
        self.outcome_date_known = outcome_date_known
        self.outcome_date = outcome_date

    def to_records(self) -> List[Dict[str, Any]]:
        # Baseline CAPACITY record
        baseline_capacity = {
            REDCAP_EVENT_NAME: BASELINE_CAPACITY,
            Capacity.patient_id.name: self.patient_id,
            Capacity.sex.name: Capacity.sex.mapping[self.sex],
            Capacity.age_estimateyears.name: self.age_estimateyears,
            Capacity.age_estimateyearsu.name: self.age_estimateyearsu,
            Capacity.admission_date.name: self.admission_date,
            Capacity.admission_any_date.name: self.admission_any_date,
        }

        # CAPACITY outcome record
        capacity_outcome = {
            Capacity.patient_id.name: self.patient_id,
            REDCAP_EVENT_NAME: CAPACITY_OUTCOME,
            Capacity.outcome_date_known.name: self.outcome_date_known,
            Capacity.outcome_date.name: self.outcome_date
        }

        return [baseline_capacity, capacity_outcome]
