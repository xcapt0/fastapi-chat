#!/bin/bash

alembic upgrade head
alembic -n testing upgrade head
uvicorn main:app --app-dir /app/src --workers 4 --host=0.0.0.0 --reload