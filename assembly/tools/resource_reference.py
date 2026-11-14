"""Load optional reference values for historical data formats."""
from functools import cache
import json
import os
from pathlib import Path
import re


_MARKER = "legacy-reference:"
_FIELD = re.compile(r"legacy-reference:[A-Za-z0-9_.:-]+")
_TEXT_FIELD = r"[0-9a-fA-F]{64}"


@cache
def _catalog():
    location = os.environ.get("G5510_REFERENCE_CATALOG")
    if location:
        with Path(location).open(encoding="utf-8") as input_file:
            values = json.load(input_file)
        if type(values) is not dict or any(type(value) is not str for value in values.values()):
            raise ValueError("Reference catalog requires named text fields")
        return values
    return {}


def reference_value(module, field):
    """Find an optional external value by module and field name."""
    key = module + ":" + field
    return _catalog().get(key, _MARKER + key)


def reference_pattern(text):
    """Match the text layout of fields inherited from a resource package."""
    if not isinstance(text, str):
        return None
    fields = list(_FIELD.finditer(text))
    if not fields:
        return None
    pieces = []
    start = 0
    for field in fields:
        pieces.extend((re.escape(text[start:field.start()]), _TEXT_FIELD))
        start = field.end()
    pieces.append(re.escape(text[start:]))
    return re.compile("".join(pieces))
