import importlib

__all__ = ["start"]
for module in __all__:
    importlib.import_module(f"handlers.{module}")
