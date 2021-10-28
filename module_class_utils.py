import importlib

def load_class(package_name, module_name, class_name):
    module = importlib.import_module(f"{package_name}.{module_name}")
    return getattr(module, class_name)
