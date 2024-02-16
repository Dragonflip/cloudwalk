#!/bin/bash
alembic upgrade head
python cloudwalk/main.py
