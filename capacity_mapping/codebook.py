from collections import namedtuple

Variable = namedtuple('Variable', ['name', 'mapping'])


class Capacity:
    sex = Variable('sex', {'male': 1, 'female': 2, 'other': -1, 'unknown': -1})
    patient_id = Variable('subjid', None)
