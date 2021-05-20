"""
Wrapper around fhirclient FHIR server to perform queries.
"""
import logging

from fhirclient.models.bundle import Bundle
from fhirclient.models.encounter import Encounter
from fhirclient.models.patient import Patient
from fhirclient.server import FHIRServer

logger = logging.getLogger(__name__)

NEXT = 'next'


class FHIRWrapper:

    def __init__(self, fhir_base):
        self.server = FHIRServer(None, fhir_base)

    def get_patients(self):
        """
        Query all patients.

        :return:
        """
        search = Patient.where({})

        yield from self.query_paginated(search)

    def get_encounters(self):
        """
        Query all encounters
        :return:
        """
        search = Encounter.where({})

        yield from self.query_paginated(search)

    def query_paginated(self, search):
        bundle = search.perform(self.server)
        while True:
            yield from (e.resource for e in bundle.entry)

            try:
                next_url = FHIRWrapper.__get_next_url(bundle)

                logger.debug('Querying next page')
                bundle = Bundle.read_from(next_url, self.server)
            except NoNextPageException:
                break

    @staticmethod
    def get_bundle_resources(bundle):
        yield from (e.resource for e in bundle.entry)

    @staticmethod
    def __get_next_url(bundle: Bundle):
        for link in bundle.link:
            if link.relation == NEXT:
                return link.url

        raise NoNextPageException()


class NoNextPageException(Exception):
    pass
