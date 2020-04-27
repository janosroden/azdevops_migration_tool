from typing import List, Dict
from msrest.authentication import BasicAuthentication
from azure.devops.connection import Connection

from azdevops_migration_lib.task_groups import (
    deleteAllTaskGroups, syncTaskGroups,)

from azdevops_migration_lib.azdevops_project import AzDevOpsProject
from azdevops_migration_lib.service_endpoints import syncServiceEndpoints, deleteAllServiceEndpoints
from azdevops_migration_lib.variable_groups import syncVariableGroups, deleteAllVariableGroups
from azdevops_migration_lib.task_groups import syncTaskGroups, deleteAllTaskGroups
from azdevops_migration_lib.build_definitions import syncBuildDefinitions, deleteAllBuildDefinitions
from azdevops_migration_lib.build_definition_folders import syncBuildDefinitionFolders, deleteAllBuildDefinitionFolders
from azdevops_migration_lib.repositories import syncRepositories, deleteAllRepositories
from azdevops_migration_lib.release_definitions import syncReleaseDefinitions, deleteAllReleaseDefinitions
import azdevops_migration_lib.secure_files as secure_files


sourceProject = AzDevOpsProject(
    baseUrl='https://dev.azure.com/<src org>',
    loginEmail='email@example.com',
    loginPAT='<Read-only PAT>',
    projectName='<Project name>',
)

destinationProject = AzDevOpsProject(
    baseUrl='https://dev.azure.com/<destination org>',
    loginEmail='email@example.com',
    loginPAT='PAT',
    projectName='<Project name>',
)

secure_files.predefinedSecureFiles = {
    'firebase_pk_test.json': {
        sourceProject: '9af73789-d227-46b7-980d-2488e6f1b648',
        destinationProject: '3a41393c-d8f9-4013-bb2b-02f3b9b2d17a',
    },
    'google_play_json_key_file.json': {
        sourceProject: '3691a224-0a4c-4386-b344-201f647de9f5',
        destinationProject: '3123efb1-fd1b-404e-ba01-773deb680831',
    },
}

# # deleteAllServiceEndpoints(destinationProject)
# syncServiceEndpoints(sourceProject, destinationProject)

# # deleteAllVariableGroups(destinationProject)
# syncVariableGroups(sourceProject, destinationProject)

# # For some reason not allowed to delete all, the last delete will fail
# # deleteAllRepositories(destinationProject)
# syncRepositories(sourceProject, destinationProject)

# # deleteAllTaskGroups(destinationProject)
# syncTaskGroups(sourceProject, destinationProject)

# # deleteAllBuildDefinitionFolders(destinationProject)
# syncBuildDefinitionFolders(sourceProject, destinationProject)

# # deleteAllBuildDefinitions(destinationProject)
# syncBuildDefinitions(sourceProject, destinationProject)

# # deleteAllReleaseDefinitions(destinationProject)
# syncReleaseDefinitions(sourceProject, destinationProject)
