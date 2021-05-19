from collections import namedtuple

Variable = namedtuple('Variable', ['name', 'mapping'])


class Capacity:
    sex = Variable('sex', {'male': 1, 'female': 2, 'other': -1, 'unknown': -1, None: -1})
    patient_id = Variable('subjid', None)
    age_estimateyears = Variable('age_estimateyears', None)
    age_estimateyearsu = Variable('age_estimateyearsu', {'months': 1, 'years': 2})
