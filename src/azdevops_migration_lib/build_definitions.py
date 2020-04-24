from typing import List, Dict

from azure.devops.client import AzureDevOpsServiceError
from azure.devops.v5_1.git import (
    GitRepository,
)
from azure.devops.v5_1.build import (
    AgentPoolQueue,
    BuildClient,
    BuildDefinition,
    BuildDefinitionReference,
    BuildRepository,
    VariableGroup,
)

from .azdevops_project import AzDevOpsProject
from .repositories import getRepositoryMapping
from .service_endpoints import getServiceEndpointMapping
from .task_groups import getTaskGroupMapping
from .variable_groups import getVariableGroupMapping
from .secure_files import getSecureFileMapping
from .utils import ResourceMapping, ResourceData, replaceAllInJson


def getAllBuildDefinitionReferences(project: AzDevOpsProject) -> List[BuildDefinitionReference]:
    response: BuildClient.GetDefinitionsResponseValue = project.buildClient.get_definitions(
        project.project_name)
    return response.value


def getAllBuildDefinitions(project: AzDevOpsProject) -> List[BuildDefinition]:
    buildDefsRefs: List[BuildDefinitionReference] = getAllBuildDefinitionReferences(
        project)

    result = []
    for buildDefRef in buildDefsRefs:
        buildDef: BuildDefinition = project.buildClient.get_definition(
            project.project_name, buildDefRef.id)
        result.append(buildDef)

    return result


def syncBuildDefinitions(srcProject: AzDevOpsProject, destProject: AzDevOpsProject):
    print('=== Sync build definitions ===')

    existingBuildNames = [
        b.name for b in getAllBuildDefinitionReferences(destProject)]

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

    for buildDef in getAllBuildDefinitions(srcProject):
        if buildDef.name in existingBuildNames:
            print(f'Skipping {buildDef.name}, already exists')
            continue

        print(f'Processing {buildDef.name}...')

        if buildDef.variable_groups:
            varGroup: VariableGroup = None
            for varGroup in buildDef.variable_groups:
                varGroup.id = oldIdsToNewVariableGrouptId[varGroup.id]

        newDefinition = BuildDefinition(
            name=buildDef.name,
            path=buildDef.path,
            type=buildDef.type,
            quality=buildDef.quality,
            queue=AgentPoolQueue(name='Default'),
            badge_enabled=buildDef.badge_enabled,
            build_number_format=buildDef.build_number_format,
            # comment='Created by migration tool',
            demands=buildDef.demands,
            description=buildDef.description,
            job_authorization_scope=buildDef.job_authorization_scope,
            job_cancel_timeout_in_minutes=buildDef.job_cancel_timeout_in_minutes,
            job_timeout_in_minutes=buildDef.job_timeout_in_minutes,
            options=buildDef.options,
            process=buildDef.process,
            process_parameters=buildDef.process_parameters,
            properties=buildDef.properties,
            repository=buildDef.repository,
            tags=buildDef.tags,
            triggers=buildDef.triggers,
            variable_groups=buildDef.variable_groups,
            variables=buildDef.variables,
        )

        buildDefJson = newDefinition.as_dict()
        buildDefJson = replaceAllInJson(
            buildDefJson, oldIdsToNewIds)
        newDefinition = BuildDefinition.from_dict(buildDefJson)

        destProject.buildClient.create_definition(
            newDefinition, destProject.project_name)


def deleteAllBuildDefinitions(project: AzDevOpsProject):
    print('=== Delete all build definitions ===')
    for buildDefRef in getAllBuildDefinitionReferences(project):
        print(f'Deleting {buildDefRef.name}')
        project.buildClient.delete_definition(
            project.project_name, buildDefRef.id)
