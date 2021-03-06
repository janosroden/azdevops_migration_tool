from typing import List, Dict
from functools import cached_property

from msrest.authentication import BasicAuthentication

from azure.devops.connection import Connection
from azure.devops.v5_1.task_agent import TaskAgentClient
from azure.devops.v5_1.service_endpoint import ServiceEndpointClient
from azure.devops.v5_1.build import BuildClient
from azure.devops.v5_1.git import GitClient
from azure.devops.v5_1.release import ReleaseClient


class AzDevOpsProject():

    @property
    def taskAgentClient(self) -> TaskAgentClient:
        return self._getClientFromCache(TaskAgentClient, self.connection.clients_v5_1.get_task_agent_client)

    @property
    def serviceEndpointClient(self) -> ServiceEndpointClient:
        return self._getClientFromCache(ServiceEndpointClient, self.connection.clients_v5_1.get_service_endpoint_client)

    @property
    def buildClient(self) -> BuildClient:
        return self._getClientFromCache(BuildClient, self.connection.clients_v5_1.get_build_client)

    @property
    def gitClient(self) -> GitClient:
        return self._getClientFromCache(GitClient, self.connection.clients_v5_1.get_git_client)

    @property
    def releaseClient(self) -> ReleaseClient:
        return self._getClientFromCache(ReleaseClient, self.connection.clients_v5_1.get_release_client)

    def __init__(self, baseUrl: str = None, loginEmail: str = None, loginPAT: str = None, projectName: str = None):
        super().__init__()

        self._apiClientCache = {}

        self.connection = Connection(
            baseUrl, creds=BasicAuthentication(loginEmail, loginPAT))

        self.baseUrl = baseUrl
        self.project_name = projectName
        self.username = loginEmail
        self.password = loginPAT

    def _getClientFromCache(self, client_type, factory_function):
        if client_type not in self._apiClientCache:
            self._apiClientCache[client_type] = factory_function()

        return self._apiClientCache[client_type]
