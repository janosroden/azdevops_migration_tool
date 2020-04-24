from typing import List, Dict

from azure.devops.client import AzureDevOpsServiceError
from azure.devops.v5_1.git import (
    GitRepository,
)
from azure.devops.v5_1.build import (
    Folder,
)

from .azdevops_project import AzDevOpsProject
from .utils import ResourceMapping, ResourceData, replaceAllInJson


def getAllBuildDefinitionFolders(project: AzDevOpsProject) -> List[Folder]:
    return [f for f in project.buildClient.get_folders(project.project_name) if f.path != '\\']


def syncBuildDefinitionFolders(srcProject: AzDevOpsProject, destProject: AzDevOpsProject):
    print('=== Sync build definition folders ===')

    existingFolderPaths = [
        f.path for f in getAllBuildDefinitionFolders(destProject)]

    for buildDefFolder in getAllBuildDefinitionFolders(srcProject):
        if buildDefFolder.path in existingFolderPaths:
            print(f'Skipping {buildDefFolder.path}, already exists')
            continue

        print(f'Processing {buildDefFolder.path}...')
        destProject.buildClient.create_folder(Folder(
            description=buildDefFolder.description), destProject.project_name, buildDefFolder.path)


def deleteAllBuildDefinitionFolders(project: AzDevOpsProject):
    print('=== Delete all build definition folders ===')
    for buildDefFolder in getAllBuildDefinitionFolders(project):
        print(f'Deleting {buildDefFolder.path}')
        project.buildClient.delete_folder(
            project.project_name, buildDefFolder.path)
