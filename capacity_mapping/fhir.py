"""
Wrapper around fhirclient FHIR server to perform queries.

The fhirclient library seems to be unable to handle paginated results. This module implements a
wrapper that will request the additional pages that are tied to the results.
"""
import logging
from typing import Iterable

from fhirclient.models.bundle import Bundle
from fhirclient.models.encounter import Encounter
from fhirclient.models.fhirsearch import FHIRSearch
from fhirclient.models.patient import Patient
from fhirclient.models.resource import Resource
from fhirclient.server import FHIRServer

logger = logging.getLogger(__name__)

NEXT = 'next'


class FHIRWrapper:

    def __init__(self, fhir_base):
        self.server = FHIRServer(None, fhir_base)

    def get_patients(self) -> Iterable[Patient]:
        """
        Query all patients, including results on subsequent pages.

        :return: a generator of Patient objects
        """
        search = Patient.where({})

        yield from self.query_paginated(search)

    def get_encounters(self):
        """
        Query all encounters, including results on subsequent pages.

        :return: a generator of Encounter objects
        """
        search = Encounter.where({})

        yield from self.query_paginated(search)

    def query_paginated(self, search: FHIRSearch) -> Iterable[Resource]:
        """
        Perform query and retrieve result on subsequent pages as well.

        :param search: FHIRSearch object containing the query that needs to be run.
        :return: a generator of Resource objects
        """
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
    def get_bundle_resources(bundle: Bundle) -> Iterable[Resource]:
        """
        Get all resource entries from a FHIR bundle.

        :param bundle:
        :return: a generator of Resource objects.
        """
        yield from (e.resource for e in bundle.entry)

    @staticmethod
    def __get_next_url(bundle: Bundle) -> str:
        """
        Get the url indicated the next page of the results.

        Raises NoNextPageException if there is no next page.

        :param bundle:
        :return:
        """
        for link in bundle.link:
            if link.relation == NEXT:
                return link.url

        raise NoNextPageException()


class NoNextPageException(Exception):
    pass
