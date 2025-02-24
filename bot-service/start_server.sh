#!/bin/bash
.venv/bin/python -m alembic upgrade head && .venv/bin/fastapi run app/main.py --port 5000 --host 0.0.0.0
