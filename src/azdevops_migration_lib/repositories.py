from typing import List, Dict
from time import sleep

from azure.devops.client import AzureDevOpsServiceError
from azure.devops.v5_1.service_endpoint import (
    EndpointAuthorization,
    ServiceEndpointClient,
    ServiceEndpoint,
)
from azure.devops.v5_1.git import (
    GitClient,
    GitRepository,
    GitRepositoryCreateOptions,
    GitImportRequest,
    GitImportRequestParameters,
    GitImportGitSource,
)

from .azdevops_project import AzDevOpsProject
from .utils import ResourceMapping, ResourceData


def getAllRepositories(project: AzDevOpsProject) -> List[GitRepository]:
    return project.gitClient.get_repositories(project.project_name)


def getRepositoryMapping(srcProject: AzDevOpsProject, destProject: AzDevOpsProject):
    return ResourceMapping(
        getAllRepositories(srcProject),
        getAllRepositories(destProject),
    )


def syncRepositories(srcProject: AzDevOpsProject, destProject: AzDevOpsProject):
    print('=== Sync repositories ===')

    pendingImportRequests: List[GitImportRequest] = []
    existingRepoNames = [repo.name for repo in getAllRepositories(destProject)]

    serviceEndpoint = destProject.serviceEndpointClient.create_service_endpoint(
        ServiceEndpoint(
            name='Git import',
            type='generic',
            url=srcProject.baseUrl,
            authorization=EndpointAuthorization(parameters={
                'username': srcProject.username,
                'password': srcProject.password,
            }, scheme='UsernamePassword')
        ),
        destProject.project_name,
    )

    try:
        # Create import requests
        for repo in getAllRepositories(srcProject):
            if repo.name in existingRepoNames:
                print(f'Skipping {repo.name}, already exists')
                continue

            print(f'Processing {repo.name}...')

            print(f'  Create repository: {repo.name}')
            newGitRepo = destProject.gitClient.create_repository(
                GitRepositoryCreateOptions(name=repo.name),
                destProject.project_name,
            )

            print(f'  Request import: {repo.name}')
            importRequest = GitImportRequest(
                parameters=GitImportRequestParameters(
                    service_endpoint_id=serviceEndpoint.id,
                    git_source=GitImportGitSource(url=repo.remote_url)),
                repository=newGitRepo,
            )

            importRequest = destProject.gitClient.create_import_request(
                importRequest, destProject.project_name, repo.name)
            pendingImportRequests.append(importRequest)

        # Wait imports
        for importRequest in pendingImportRequests:
            while True:
                importRequests = destProject.gitClient.query_import_requests(
                    destProject.project_name, importRequest.repository.id)

                if importRequests:
                    importRequest = importRequests[0]

                    if importRequest.status == 'failed':
                        print(
                            f'ERROR: Import of {importRequest.repository.name} failed: {importRequest.detailed_status.error_message}')
                        return
                    elif importRequest.status == 'completed':
                        print(
                            f'Import of {importRequest.repository.name} has completed')
                        break
                    else:
                        print(
                            f'Waiting for import {importRequest.repository.name}, status: {importRequest.status}')
                        sleep(5)

    finally:
        destProject.serviceEndpointClient.delete_service_endpoint(
            destProject.project_name, serviceEndpoint.id)


def deleteAllRepositories(project: AzDevOpsProject):
    print('=== Delete all repositories ===')
    for repo in getAllRepositories(project):
        print(f'Deleting {repo.name}')
        project.gitClient.delete_repository(repo.id, project.project_name)
