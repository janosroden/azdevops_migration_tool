from typing import List, Dict

from azure.devops.client import AzureDevOpsServiceError
from azure.devops.v5_1.task_agent import (
    TaskAgentClient,
    VariableGroup,
    VariableGroupParameters,
)

from .azdevops_project import AzDevOpsProject
from .utils import ResourceMapping


def getAllVariableGroups(project: AzDevOpsProject) -> List[VariableGroup]:
    return project.taskAgentClient.get_variable_groups(project.project_name)


def getVariableGroupMapping(srcProject: AzDevOpsProject, destProject: AzDevOpsProject):
    return ResourceMapping(
        getAllVariableGroups(srcProject),
        getAllVariableGroups(destProject),
    )


def syncVariableGroups(srcProject: AzDevOpsProject, destProject: AzDevOpsProject):
    print('=== Sync variable groups ===')

    variableGroup: VariableGroup = None
    destVariableGroupNames: List[str] = [
        variableGroup.name for variableGroup in getAllVariableGroups(destProject)]

    for variableGroup in getAllVariableGroups(srcProject):
        if variableGroup.name in destVariableGroupNames:
            print(f'Variable group {variableGroup.name} already exists')
            continue

        print(f'Creating variable group {variableGroup.name}')

        destProject.taskAgentClient.add_variable_group(
            VariableGroupParameters(
                name=variableGroup.name,
                description=variableGroup.description,
                provider_data=variableGroup.provider_data,
                type=variableGroup.type,
                variables=variableGroup.variables,
            ),
            destProject.project_name,
        )


def deleteAllVariableGroups(project: AzDevOpsProject):
    print('=== Delete variable groups ===')
    for variableGroup in getAllVariableGroups(project):
        print(f'Deleting {variableGroup.name}')
        project.taskAgentClient.delete_variable_group(
            project.project_name, variableGroup.id)
