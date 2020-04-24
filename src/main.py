from typing import List, Dict
from msrest.authentication import BasicAuthentication
from azure.devops.connection import Connection

from azdevops_migration_lib.task_groups import (
    deleteAllTaskGroups, syncTaskGroups,)

from azdevops_migration_lib.azdevops_project import AzDevOpsProject
from azdevops_migration_lib.services import syncServiceEndpoints, deleteAllServiceEndpoints
from azdevops_migration_lib.variable_groups import syncVariableGroups, deleteAllVariableGroups
from azdevops_migration_lib.task_groups import syncTaskGroups, deleteAllTaskGroups


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

deleteAllTaskGroups(destinationProject)
deleteAllVariableGroups(destinationProject)
deleteAllServiceEndpoints(destinationProject)

syncServiceEndpoints(destinationProject, sourceProject)
syncVariableGroups(destinationProject, sourceProject)
syncTaskGroups(destinationProject, sourceProject)
