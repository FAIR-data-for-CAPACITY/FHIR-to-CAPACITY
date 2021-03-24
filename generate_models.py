#!/usr/bin/env python3

import os
import shutil
from pathlib import Path

import fhirloader
import fhirspec
import settings

ROOT_PATH = Path()
FHIR_PARSER_PATH = ROOT_PATH / 'fhir-parser'
MAPPINGS_FILE = 'mappings.py'
SETTINGS_FILE = 'settings.py'


def load_fhirspec():
    # assure we have all files
    loader = fhirloader.FHIRLoader(settings)
    spec_source = loader.load(force_download=False, force_cache=False)

    return fhirspec.FHIRSpec(spec_source, settings)


# TODO: I'm following the instructions of the fhir-parser readme on how to integrate fhir parser into the project.
#  However, this approach makes for a very confusing package structure, especially now we're calling the fhirspec
#  module directly instead of running generate.py. Think about integrating fhir-parser in a cleaner way.
def main():
    # Copy mappings and settings to fhir-parser submodule
    shutil.copy(ROOT_PATH / MAPPINGS_FILE, FHIR_PARSER_PATH / MAPPINGS_FILE)
    shutil.copy(ROOT_PATH / SETTINGS_FILE, FHIR_PARSER_PATH / SETTINGS_FILE)

    os.chdir(FHIR_PARSER_PATH)

    # assure we have all files
    loader = fhirloader.FHIRLoader(settings)
    spec_source = loader.load(force_download=False, force_cache=False)

    spec = fhirspec.FHIRSpec(spec_source, settings)

    spec.write()


if __name__ == '__main__':
    main()
