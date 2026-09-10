#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"
source "$DIR/.venv/bin/activate"
export PYTHONPATH="$DIR/agent:$PYTHONPATH"
export PYTHONWARNINGS="ignore"
exec python -u "$DIR/agent/mcp_server.py" "$@"
