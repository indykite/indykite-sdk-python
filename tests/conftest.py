import sys
sys.path.append('./indykite_sdk')

import pytest
import fixtures

from helpers.walk_packages import get_package_paths_in_module

pytest_plugins = [
    *get_package_paths_in_module(fixtures),
]
