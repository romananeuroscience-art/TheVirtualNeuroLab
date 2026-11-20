#!/bin/bash
# Double-click me: serves The Virtual Neuro Lab on http://localhost:8200 and opens it in your browser.
# It also runs the "Ask Claude" panel (tools/server.py). Claude needs your Anthropic API key in .env
# (ANTHROPIC_API_KEY=...) in this folder or in "Fly Brain/.env"; without it the lab still works and the panel says Claude is offline.
# Close this Terminal window (or press Ctrl+C) to stop the server.
cd "$(dirname "$0")"
PORT=8200
pid=$(lsof -ti tcp:$PORT 2>/dev/null)
if [ -n "$pid" ]; then echo "Freeing port $PORT (process $pid)"; kill $pid 2>/dev/null; sleep 1; fi
python3 -c "import anthropic" 2>/dev/null || { echo "Installing the 'anthropic' package for Claude (one time)..."; python3 -m pip install --user --quiet anthropic; }
( sleep 1.5; open "http://localhost:$PORT/" ) &
FLYLAB_PORT=$PORT exec python3 tools/server.py
