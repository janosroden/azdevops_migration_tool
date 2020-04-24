from typing import List, Dict

from addict import Dict as AdDict

from .azdevops_project import AzDevOpsProject
from .utils import ResourceMapping

predefinedSecureFiles: Dict[str, Dict[AzDevOpsProject, str]] = {}


def getSecureFileMapping(srcProject: AzDevOpsProject, destProject: AzDevOpsProject):

    sources = [AdDict({'name': name, 'id': mapping[srcProject]})
               for name, mapping in predefinedSecureFiles.items() if srcProject in mapping]
    destinations = [AdDict({'name': name, 'id': mapping[destProject]})
                    for name, mapping in predefinedSecureFiles.items() if destProject in mapping]

    return ResourceMapping(sources, destinations)
