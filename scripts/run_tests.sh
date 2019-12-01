#!/bin/bash
python3 -m pytest tests/ --cov-branch --cov-report html --cov-report xml  --cov-report term --cov=. -v
