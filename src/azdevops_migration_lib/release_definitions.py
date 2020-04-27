from typing import List, Dict

from azure.devops.client import AzureDevOpsServiceError
from azure.devops.v5_1.git import (
    GitRepository,
)
from azure.devops.v5_1.release import (
    ReleaseClient,
    ReleaseDefinition,
    ReleaseDefinitionEnvironment,
)
from azure.devops.v5_1.build import (
    VariableGroup,
)

from .azdevops_project import AzDevOpsProject
from .repositories import getRepositoryMapping
from .service_endpoints import getServiceEndpointMapping
from .task_groups import getTaskGroupMapping
from .variable_groups import getVariableGroupMapping
from .secure_files import getSecureFileMapping
from .utils import ResourceMapping, ResourceData, replaceAllInJson


def getAllReleaseDefinitions(project: AzDevOpsProject) -> List[ReleaseDefinition]:
    response: ReleaseClient.GetReleaseDefinitionsResponseValue = project.releaseClient.get_release_definitions(
        project.project_name, expand=['artifacts', 'pipeline_process', 'environments', 'triggers', 'variables', 'variable_groups'])
    return response.value


def syncReleaseDefinitions(srcProject: AzDevOpsProject, destProject: AzDevOpsProject):
    print('=== Sync release definitions ===')

    existingReleaseNames = [
        b.name for b in getAllReleaseDefinitions(destProject)]

    oldIdsToNewRepoId: Dict[str, str] = getRepositoryMapping(
        srcProject, destProject).asDict()
    oldIdsToNewTaskGroupId: Dict[str, str] = getTaskGroupMapping(
        srcProject, destProject).asDict()
    oldIdsToNewServiceEndpointId: Dict[str, str] = getServiceEndpointMapping(
        srcProject, destProject).asDict()
    oldIdsToNewSecureFileId: Dict[str, str] = getSecureFileMapping(
        srcProject, destProject).asDict()
    oldIdsToNewVariableGrouptId: Dict[int, int] = getVariableGroupMapping(
        srcProject, destProject).asDict()

    oldIdsToNewIds = {**oldIdsToNewRepoId, **oldIdsToNewTaskGroupId,
                      **oldIdsToNewServiceEndpointId, **oldIdsToNewSecureFileId}

    for releaseDef in getAllReleaseDefinitions(srcProject):
        if releaseDef.name in existingReleaseNames:
            print(f'Skipping {releaseDef.name}, already exists')
            continue

        print(f'Processing {releaseDef.name}...')
        releaseDef = srcProject.releaseClient.get_release_definition(
            srcProject.project_name, releaseDef.id)

        if releaseDef.variable_groups:
            releaseDef.variable_groups = [
                oldIdsToNewVariableGrouptId[vgId] for vgId in releaseDef.variable_groups]

        releaseEnv: ReleaseDefinitionEnvironment = None
        for releaseEnv in releaseDef.environments:
            releaseEnv.variable_groups = [
                oldIdsToNewVariableGrouptId[vgId] for vgId in releaseEnv.variable_groups]

            for dp in releaseEnv.deploy_phases:
                del dp['deploymentInput']['queueId']

        newDefinition = ReleaseDefinition(
            name=releaseDef.name,
            artifacts=releaseDef.artifacts,
            description=releaseDef.description,
            environments=releaseDef.environments,
            pipeline_process=releaseDef.pipeline_process,
            properties=releaseDef.properties,
            release_name_format=releaseDef.release_name_format,
            tags=releaseDef.tags,
            triggers=releaseDef.triggers,
            variable_groups=releaseDef.variable_groups,
            variables=releaseDef.variables,
        )

        releaseDefJson = newDefinition.as_dict()
        releaseDefJson = replaceAllInJson(
            releaseDefJson, oldIdsToNewIds)
        newDefinition = ReleaseDefinition.from_dict(releaseDefJson)

        destProject.releaseClient.create_release_definition(
            newDefinition, destProject.project_name)


def deleteAllReleaseDefinitions(project: AzDevOpsProject):
    print('=== Delete all release definitions ===')
    for releaseDef in getAllReleaseDefinitions(project):
        print(f'Deleting {releaseDef.name}')
        project.releaseClient.delete_release_definition(
            project.project_name, releaseDef.id)
