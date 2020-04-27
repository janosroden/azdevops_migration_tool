This project tries to migrate several data types between two Azure DevOps projects.
The script extends the destination project so you can have existing definitions.
ID mapping uses names therefore you may need to rename your resources temporarily.

Supported resources:
- Service endpoints
- Variable groups
- Task groups
- Git repositories
- Build definition folders
- Build definitions
- Release definitions

# Prerequisites

## Programs

1. Install [Docker](https://www.docker.com/)
1. Install [VSCode](https://code.visualstudio.com/)
1. Install [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) VSCode extension


## Destination project

1. Must exists
1. Hard-code a PAT with write scopes (see main.py)

## Builds

### Azure DevOps extensions

You need to install all third-party extensions first. Note that the fresh install of an
extension doesn't install the previous versions. Therefore you need to update your steps
in the builds of the **source** project to match with the extension version of the
**destination** project. Otherwise the build creation will fail due the missing task version.

(Task version in the classic build editor can be found in the upper dropdown on
the task edit area.)

### Dependencies

Dependencies between builds are not implemented which means you have to turn off build
completion triggers in the build **source** otherwise migration will fail.
Reenable it manually.

## Service endpoints

This script unable to migrate endpoints which can't be fully queried. If you see errors
during service endpoint creation then go and create the failed endpoints with the proper
type manually and give them the **same name** as original.

## GIT repositories

1. You have to change default and compare branches if they aren't the defaults.
1. Also you have to setup branch policies if any.


## Secure files

There is no API to manage secure files, you have to create them manually and hard-code
their IDs in the script.
Call them whatever you want.

You can get the IDs from the url (secureFileId) during edit.
ht<span>tps://dev.azure.</span>com/example/MyProject/_library?itemType=SecureFiles&view=SecureFileView&secureFileId=**3a41393c-d8f9-4013-bb2b-02f3b9b2d17a**&path=fb_key_for_unit_tests.json



# Getting started

1. Open the project root in VSCode
1. Build the dev container
1. Edit `main.py`
1. Run

# Notes

1. Don't rush, migrate one resource type at a time.
1. Always check the result.
1. Use read-only PAT for the source project, just in case
1. Builds are modified to run in `Default` agent pool
1. Agent pool information is deleted for release jobs
