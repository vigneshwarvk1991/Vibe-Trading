#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"
source "$DIR/.venv/bin/activate"
export PYTHONPATH="$DIR/agent:$PYTHONPATH"
exec python "$DIR/agent/mcp_server.py" "$@"
