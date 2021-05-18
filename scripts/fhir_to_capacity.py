import logging
import sys

from clize import run

from capacity_mapping import mapping

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def fhir_to_capacity(fhir_base_url, capacity_url, capacity_token):
    """
    Queries a FHIR server for patients, converts this to records matching the
    CAPACITY codebook, and uploads the result to a REDCAP server.

    :param fhir_base_url:
    :param capacity_url:
    :param capacity_token:
    :return:
    """
    mapping.fhir_to_capacity(fhir_base_url, capacity_url, capacity_token)


if __name__ == '__main__':
    run(fhir_to_capacity)
