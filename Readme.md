This project tries to migrate several data types between two Azure DevOps projects.

Supported resources:
- Service endpoints
- Variable groups
- Task groups
- Git repositories
- Builds

# Prerequisites

## Destination project

1. Must exists
1. Hard-code a PAT with write scopes (see main.py)

## Azure DevOps extensions

### Builds
You need to install all third-party extensions first. Note that the fresh install of an
extension doesn't install the previous versions. Therefore you need to update your steps
in the builds of the **source** project to match with the extension version of the
**destination** project. Otherwise the build creation will fail due the missing task version.

(Task version in the classic build editor can be found in the upper dropdown on
the task edit area.)

## Service endpoints

This script unable to migrate endpoints which can't be fully queried. If you see errors
during service endpoint creation then go and create the failed endpoint with the proper
type manually and give it the **same name** as the original.

## Secure files

There is no API to manage secure files, you have to create them manually and hard-code
their IDs in the script.
Call them whatever you want.

You can get the IDs from the url (secureFileId) during edit.
ht<span>tps://dev.azure.</span>com/example/MyProject/_library?itemType=SecureFiles&view=SecureFileView&secureFileId=**3a41393c-d8f9-4013-bb2b-02f3b9b2d17a**&path=fb_key_for_unit_tests.json


# Notes

1. Don't go fast, migrate one resource type at a time.
1. Always check the result.
1. Use read-only PAT for the source project, just in case
