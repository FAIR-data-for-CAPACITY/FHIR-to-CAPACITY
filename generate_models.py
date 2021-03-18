#!/usr/bin/env python3

import shutil
from pathlib import Path
import os
import subprocess


ROOT_PATH = Path()
FHIR_PARSER_PATH = ROOT_PATH/'fhir-parser'
MAPPINGS_FILE = 'mappings.py'
SETTINGS_FILE = 'settings.py'


def main():
    # Copy mappings and settings to fhir-parser submodule
    shutil.copy(ROOT_PATH/MAPPINGS_FILE, FHIR_PARSER_PATH/MAPPINGS_FILE)
    shutil.copy(ROOT_PATH / SETTINGS_FILE, FHIR_PARSER_PATH / SETTINGS_FILE)

    os.chdir(FHIR_PARSER_PATH)

    # I don't like to call generate as subprocess but here we are
    subprocess.run('./generate.py')


if __name__ == '__main__':
    main()
