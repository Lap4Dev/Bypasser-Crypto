#!/bin/bash

set -o errexit

alembic upgrade head

python3 -m src.main