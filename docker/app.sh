#!/bin/bash

cd app

alembic upgrade head

python main.py