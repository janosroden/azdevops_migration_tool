from typing import List, Dict
from enum import Enum


class ResourceData(Enum):
    NATURAL_KEY = 1
    ID_SRC = 2
    ID_DST = 3
    OBJECT_SRC = 4
    OBJECT_DST = 5
    OBJECT_BOTH = 5


class ResourceMapping():
    def __init__(self, sourceResources: list, destinationResources: list, naturalKeyFunc=None):
        super().__init__()

        self.sourceResources = sourceResources
        self.destinationResources = destinationResources
        self.naturalKeyFunc = naturalKeyFunc

        if not self.naturalKeyFunc:
            self.naturalKeyFunc = lambda res: res.name

        self._srcResByNatural = {self.naturalKeyFunc(
            res): res for res in self.sourceResources}
        self._dstResByNatural = {self.naturalKeyFunc(
            res): res for res in self.destinationResources}

    def asDict(self, key: ResourceData = ResourceData.ID_SRC, value: ResourceData = ResourceData.ID_DST):
        keyFunction = self._funcForResourceData(key)
        valueFunction = self._funcForResourceData(value)

        result = {}
        for naturalKey, srcRes in self._srcResByNatural.items():
            dstRes = self._dstResByNatural.get(naturalKey)

            result[keyFunction(srcRes, dstRes)] = valueFunction(srcRes, dstRes)

        return result

    def _funcForResourceData(self, resourceData: ResourceData):
        if resourceData == ResourceData.NATURAL_KEY:
            return lambda srcRes, dstRes: self.naturalKeyFunc(srcRes)
        elif resourceData == ResourceData.ID_SRC:
            return lambda srcRes, dstRes: srcRes.id if srcRes else None
        elif resourceData == ResourceData.ID_DST:
            return lambda srcRes, dstRes: dstRes.id if dstRes else None
        elif resourceData == ResourceData.OBJECT_SRC:
            return lambda srcRes, dstRes: srcRes
        elif resourceData == ResourceData.OBJECT_DST:
            return lambda srcRes, dstRes: dstRes
        elif resourceData == ResourceData.OBJECT_BOTH:
            return lambda srcRes, dstRes: (srcRes, dstRes)


def toCamelCase(snakeStr: str) -> str:
    components = snakeStr.split('_')
    return components[0] + ''.join(c.title() for c in components[1:])


def replaceAllInJson(obj, values: dict):
    if isinstance(obj, dict):
        return {values.get(k, k): replaceAllInJson(v, values) for k, v in obj.items()}

    if isinstance(obj, list):
        return [replaceAllInJson(v, values) for v in obj]

    return values.get(obj, obj)
