# core/loader.py
import importlib
import pkgutil
from modules import __path__ as modules_path # filepath of the module folder
from core.EventModule import EventModule


def load_modules() -> list[EventModule]:
    """Loads all the modules from the modules subfolder. 

    Returns:
        list[EventModule]: list of event modules.
    """
    event_modules = []
    for _, name, _ in pkgutil.iter_modules(modules_path):
        mod = importlib.import_module(f"modules.{name}")
        for attr in dir(mod):
            cls = getattr(mod, attr)
            if isinstance(cls, type) and issubclass(cls, EventModule) and cls != EventModule:
                event_modules.append(cls())
    return event_modules