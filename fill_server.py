"""
# `fill_server.py`
This script is meant to be used for testing purposes only! I creates a bunch
of resources on a fhir server that can be used to test the mappings.
"""

import click
from fhirclient.server import FHIRServer
from fhirclient.models.patient import Patient
import random
from capacity_mapping.codebook import Capacity

NUM_PATIENTS = 10


@click.command()
@click.argument('fhir_base')
@click.option('--n', default=NUM_PATIENTS, help='Number of records to create')
def main(fhir_base, n):
    fhir_server = FHIRServer(None, fhir_base)

    patients = create_patients(n)

    for p in patients:
        p.create(fhir_server)


def create_patients(num_patients):
    for _ in range(num_patients):
        p = Patient()
        p.gender = random.choice(list(Capacity.sex.mapping.keys()))
        yield p


if __name__ == '__main__':
    main()
