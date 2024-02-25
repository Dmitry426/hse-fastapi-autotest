__all__ = "traverse_and_import"

import importlib.util
import logging
import os
from pathlib import Path
from types import ModuleType

from fastapi import FastAPI

logger = logging.getLogger("fastapi_autotest")


def import_main_module(module_path: str) -> ModuleType:
    """Import main module"""
    spec = importlib.util.spec_from_file_location("main", module_path)
    main_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_module)
    return main_module


# pylint: disable=no-else-return,inconsistent-return-statements
def traverse_and_import(directory_path: Path) -> FastAPI:
    """Traverse through given dir and fin Fastapi app
    :param directory_path: Fast api repo path
    :return : Fast api app
    """

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file == "main.py":
                module_path = os.path.join(root, file)
                main_module = import_main_module(module_path)
                if hasattr(main_module, "app"):
                    app_object = main_module.app
                    return app_object
                else:
                    logger.error(f"No 'app' object found in {module_path}")
                    raise FileExistsError
