#!/bin/zsh
set -euo pipefail
cd "$(dirname "$0")/../backend"
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
python app.py
