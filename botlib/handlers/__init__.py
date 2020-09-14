import importlib

__all__ = ["start", "newspace", "myspaces"]
for module in __all__:
    importlib.import_module(f"handlers.{module}")
