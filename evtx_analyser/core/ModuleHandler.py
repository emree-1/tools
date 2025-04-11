# core/loader.py
import importlib
import pkgutil
import inspect
from modules.extractors import __path__ as extractor_modules_path
from core.EventModule import EventModule


class ModuleHandler:
    @staticmethod
    def load_modules(type) -> list[EventModule]:
        """Loads all the modules from the modules subfolder.

        Returns:
            list[EventModule]: List of event modules.
        """
        event_modules = {}
        for _, name, _ in pkgutil.iter_modules(extractor_modules_path):
            try:
                # Import the module
                mod = importlib.import_module(f"modules.{type}.{name}")
                
                # Find all classes that are subclasses of EventModule
                for _, cls in inspect.getmembers(mod, inspect.isclass):
                    if issubclass(cls, EventModule) and cls != EventModule:
                        instance = cls()
                        event_modules[instance.eventID] = instance
            except Exception as e:
                print(f"Failed to load module '{name}': {e}")
        
        return event_modules