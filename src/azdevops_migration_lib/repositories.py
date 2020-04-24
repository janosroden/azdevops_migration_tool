from typing import List, Dict

from azure.devops.client import AzureDevOpsServiceError
from azure.devops.v5_1.git import (
    GitClient,
    GitRepository,
    GitImportRequest,
    GitImportRequestParameters,
    GitImportGitSource,
)

from .azdevops_project import AzDevOpsProject
from .utils import ResourceMapping


def getAllRepositories(project: AzDevOpsProject) -> List[GitRepository]:
    return project.gitClient.get_repositories(project.project_name)


def getRepositoryMapping(srcProject: AzDevOpsProject, destProject: AzDevOpsProject):
    return ResourceMapping(
        getAllRepositories(srcProject),
        getAllRepositories(destProject),
    )


def syncRepositories(destProject: AzDevOpsProject, srcProject: AzDevOpsProject):
    print('=== Sync repositories ===')

    for repo in getAllRepositories(srcProject):
        print(f'Processing {repo.name}...')
        # newDefinition =
        importRequest = GitImportRequest(
            parameters=GitImportRequestParameters(
                git_source=GitImportGitSource())
        )
        destProject.gitClient.create_import_request()
        destProject.connection._creds
        break


# def deleteAllBuildDefinitions(project: AzDevOpsProject):
#     print('=== Delete all task groups ===')
#     for buildDefRef in getAllBuildDefinitionReferences(project):
#         print(f'Deleting {buildDefRef.name}')
#         project.buildClient.delete_definition(
#             project.project_name, buildDefRef.id)
