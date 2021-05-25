from collections import namedtuple

Variable = namedtuple('Variable', ['name', 'mapping'])


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
    
