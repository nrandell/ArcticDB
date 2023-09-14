from arcticdb.version_store import NativeVersionStore
from IPython.display import display, Markdown
import pandas as pd
from arcticdb.supported_types import time_types as supported_time_types
from arcticdb.version_store.library import Library


def check_and_adapt_library(lib):
    """
    Verifies that the type of the library is compatible with the diagnostics engine, and if necessary,
    adapts the library to the type used internally by the engine. It also returns if the original library
    type belongs to the internal API.
    """
    if isinstance(lib, NativeVersionStore):
        return lib, True
    elif isinstance(lib, Library):
        lib._nvs, False
    else:
        display(Markdown(f"the provided library is not supported"))
        return None, False


def get_string_version(as_of):
    if as_of is not None:
        if isinstance(as_of, supported_time_types):
            string_version = "the as_of date ***" + as_of.strftime("%Y-%m-%d %H:%M:%S %Z") + "***"
        elif isinstance(as_of, str):
            string_version = f"the snapshot name ***{as_of}***"
        else:
            string_version = f"the version number ***{as_of}***"
    else:
        string_version = "***the latest version***"
    return string_version


def check_symbol_exists(lib, symbol, as_of=None):
    """
    Verifies that the symbol and version (in case it is specified) exist
    """
    string_version = get_string_version(as_of)
    if not lib.has_symbol(symbol, as_of=as_of):
        display(Markdown(f"Symbol does not exists for {string_version} from symbol {symbol}"))
        return False
    else:
        return True
