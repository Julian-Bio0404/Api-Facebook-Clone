#!/bin/sh

set -o errexit
set -o nounset

cd facebook/ && celery -A taskapp worker -l INFO
