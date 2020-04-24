from typing import List, Dict
from msrest.authentication import BasicAuthentication
from azure.devops.connection import Connection

from azdevops_migration_lib.task_groups import (
    deleteAllTaskGroups, syncTaskGroups,)

from azdevops_migration_lib.azdevops_project import AzDevOpsProject
from azdevops_migration_lib.service_endpoints import syncServiceEndpoints, deleteAllServiceEndpoints
from azdevops_migration_lib.variable_groups import syncVariableGroups, deleteAllVariableGroups
from azdevops_migration_lib.task_groups import syncTaskGroups, deleteAllTaskGroups
from azdevops_migration_lib.build import syncBuildDefinitions, deleteAllBuildDefinitions
import azdevops_migration_lib.secure_files as secure_files


sourceProject = AzDevOpsProject(
    Connection(base_url='https://dev.azure.com/<src org>',
               creds=BasicAuthentication(
                   '', '<Read-only PAT>'),
               ),
    '<Project name>',
)

destinationProject = AzDevOpsProject(
    Connection(base_url='https://dev.azure.com/<destination org>',
               creds=BasicAuthentication(
                   '', 'PAT'),
               ),
    '<Project name>',
)

secure_files.predefinedSecureFiles = {
    'firebase_pk_test.json': {
        sourceProject: '9af73789-d227-46b7-980d-2488e6f1b648',
        destinationProject: '3a41393c-d8f9-4013-bb2b-02f3b9b2d17a',
    },
}

# deleteAllTaskGroups(destinationProject)
# syncTaskGroups(destinationProject, sourceProject)

deleteAllBuildDefinitions(destinationProject)
syncBuildDefinitions(destinationProject, sourceProject)

# deleteAllVariableGroups(destinationProject)

# syncServiceEndpoints(destinationProject, sourceProject)
# syncVariableGroups(destinationProject, sourceProject)
