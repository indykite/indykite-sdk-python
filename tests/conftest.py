import sys
sys.path.append('./jarvis_sdk')

import tests.fixtures
from tests.helpers.walk_packages import get_package_paths_in_module

pytest_plugins = [
    *get_package_paths_in_module(tests.fixtures),
]
