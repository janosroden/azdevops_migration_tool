from typing import List, Dict

from azure.devops.client import AzureDevOpsServiceError
from azure.devops.v5_1.service_endpoint import ServiceEndpointClient
from azure.devops.v5_1.service_endpoint.models import ServiceEndpoint

from .azdevops_project import AzDevOpsProject
from .utils import ResourceMapping


def getAllServiceEndpoints(project: AzDevOpsProject) -> List[ServiceEndpoint]:
    return project.serviceEndpointClient.get_service_endpoints(project.project_name, include_details=True)


def getServiceEndpointMapping(srcProject: AzDevOpsProject, destProject: AzDevOpsProject):
    return ResourceMapping(
        getAllServiceEndpoints(srcProject),
        getAllServiceEndpoints(destProject),
    )


def syncServiceEndpoints(destProject: AzDevOpsProject, srcProject: AzDevOpsProject):
    print('=== Sync service endpoints ===')

    destSeNames: List[str] = [
        serviceEndpoint.name for serviceEndpoint in getAllServiceEndpoints(destProject)]

    for serviceEndpoint in getAllServiceEndpoints(srcProject):
        if serviceEndpoint.name in destSeNames:
            print(f'Service endpoint {serviceEndpoint.name} already exists')
            continue

        print(f'Creating service endpoint {serviceEndpoint.name}')
        try:
            destProject.serviceEndpointClient.create_service_endpoint(
                serviceEndpoint, destProject.project_name)
        except AzureDevOpsServiceError as err:
            print(f'ERROR: {err}')


def deleteAllServiceEndpoints(project: AzDevOpsProject):
    print('=== Delete service endpoints ===')
    for serviceEndpoint in getAllServiceEndpoints(project):
        print(f'Deleting {serviceEndpoint.name}')
        project.serviceEndpointClient.delete_service_endpoint(
            project.project_name, serviceEndpoint.id)
