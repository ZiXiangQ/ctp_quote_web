#!/bin/zsh
set -euo pipefail
cd "$(dirname "$0")/../frontend"
npm i
npm run dev -- --port 5173
