import os
import importlib.util


def import_main_module(module_path):
    spec = importlib.util.spec_from_file_location("main", module_path)
    main_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_module)
    return main_module


def traverse_and_import(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file == "main.py":
                module_path = os.path.join(root, file)
                main_module = import_main_module(module_path)
                if hasattr(main_module, 'app'):
                    app_object = main_module.app
                    print(f"Imported 'app' object from {module_path}")
                    return app_object
                else:
                    print(f"No 'app' object found in {module_path}")
                    return None


