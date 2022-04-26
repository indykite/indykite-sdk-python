from pkgutil import ModuleInfo
from pkgutil import walk_packages
from types import ModuleType
from typing import Iterable


def get_packages_in_module(m: ModuleType) -> Iterable[ModuleInfo]:
    return walk_packages(m.__path__, prefix=m.__name__ + '.')  # type: ignore


def get_package_paths_in_module(m: ModuleType) -> Iterable[str]:
    return [package.name for package in get_packages_in_module(m)]