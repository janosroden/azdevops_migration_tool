from typing import List, Dict

from azure.devops.client import AzureDevOpsServiceError
from azure.devops.v5_1.task_agent.models import (
    TaskGroup,
    TaskGroupCreateParameter,
    TaskGroupStep,
    TaskDefinitionReference,
)

from .azdevops_project import AzDevOpsProject
from .export import toExportJson


def getAllTaskGroups(project: AzDevOpsProject) -> List[TaskGroup]:
    return project.taskAgentClient.get_task_groups(project.project_name)


def syncTaskGroups(destProject: AzDevOpsProject, srcProject: AzDevOpsProject):
    print('=== Sync task groups ===')

    destTaskGroupsByName: Dict[str, TaskGroup] = {
        taskGroup.name: taskGroup for taskGroup in getAllTaskGroups(destProject)}
    srcTaskGroupsById: Dict[str, TaskGroup] = {
        taskGroup.id: taskGroup for taskGroup in getAllTaskGroups(srcProject)}

    while len(destTaskGroupsByName) < len(srcTaskGroupsById):
        print(
            f'Task group count: dst: {len(destTaskGroupsByName)}, src: {len(srcTaskGroupsById)}')

        for _, taskGroup in srcTaskGroupsById.items():
            if taskGroup.name in destTaskGroupsByName:
                print(f'Skipping task group {taskGroup.name}, already exists')
                continue

            print(f'Processing task group {taskGroup.name}')

            taskGroupSteps: List[TaskGroupStep] = taskGroup.tasks
            for taskGroupStep in taskGroupSteps:
                task: TaskDefinitionReference = taskGroupStep.task
                if task.definition_type == 'metaTask':
                    if task.id in srcTaskGroupsById:
                        if srcTaskGroupsById[task.id].name in destTaskGroupsByName:
                            task.id = destTaskGroupsByName[srcTaskGroupsById[task.id].name].id
                        else:
                            print(
                                f'Defer processing task group {taskGroup.name}')
                            break
                    else:
                        # We're updating TaskDefinitionReference instances in srcTaskGroupsById so this could happen if we're already translated the step
                        print(
                            f'Skip translating build step {taskGroupStep.display_name}, already exists')
            else:
                taskGroup = destProject.taskAgentClient.add_task_group(
                    TaskGroupCreateParameter(
                        name=taskGroup.name,
                        author=taskGroup.author,
                        category=taskGroup.category,
                        description=taskGroup.description,
                        friendly_name=taskGroup.friendly_name,
                        inputs=taskGroup.inputs,
                        icon_url=taskGroup.icon_url,
                        instance_name_format=taskGroup.instance_name_format,
                        runs_on=taskGroup.runs_on,
                        tasks=taskGroupSteps,
                        version=taskGroup.version,
                    ), destProject.project_name,
                )
                destTaskGroupsByName[taskGroup.name] = taskGroup


def deleteAllTaskGroups(project: AzDevOpsProject):
    print('=== Delete all task groups ===')
    for taskGroup in getAllTaskGroups(project):
        print(f'Deleting {taskGroup.name}')
        project.taskAgentClient.delete_task_group(
            project.project_name, taskGroup.id)


def exportTaskGroups(project: AzDevOpsProject):
    import json
    print('=== Export task groups ===')

    for taskGroup in getAllTaskGroups(project):
        print(f'Exporting group {taskGroup.name}...')
        with open('export.json', 'wb') as f:
            exportJson: dict = toExportJson(taskGroup.as_dict())
            f.write(json.dumps(exportJson).encode('utf-8'))

        break
