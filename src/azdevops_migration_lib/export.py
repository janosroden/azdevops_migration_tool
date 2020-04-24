from typing import List, Dict

from .utils import toCamelCase


def toExportJson(obj):
    if isinstance(obj, dict):
        return {toCamelCase(k): toExportJson(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [toExportJson(v) for v in obj]

    return obj
