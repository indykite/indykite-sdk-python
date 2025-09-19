#!/bin/bash
# pipefail - BASH only, not supported in POSIX Shell
set -o errexit -o nounset -o pipefail

PROJECT_NAME=$1

if [[ "${PROJECT_NAME}" = "" ]]; then
    echo "PROJECT_NAME is not set"
    echo "eg: sh init.sh cms-server"
    exit 1
fi

export DEFAULT_NAME=spaces

sed -i "s/${DEFAULT_NAME}/${PROJECT_NAME}/g" ./README.md
