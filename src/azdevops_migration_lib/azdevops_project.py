from typing import List, Dict
from functools import cached_property

from azure.devops.connection import Connection
from azure.devops.v5_1.task_agent import TaskAgentClient
from azure.devops.v5_1.service_endpoint import ServiceEndpointClient
from azure.devops.v5_1.build import BuildClient
from azure.devops.v5_1.git import GitClient


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

    def __init__(self, connection: Connection, name: str):
        super().__init__()

        self._apiClientCache = {}

        self.connection = connection
        self.project_name = name

    def _getClientFromCache(self, client_type, factory_function):
        if client_type not in self._apiClientCache:
            self._apiClientCache[client_type] = factory_function()

        return self._apiClientCache[client_type]
