#!/bin/bash
cd "$(dirname "$0")"

LOG="/tmp/talaria.log"
PID_FILE="/tmp/talaria.pid"

# Kill existing if running
if [[ -f "$PID_FILE" ]]; then
    kill "$(cat "$PID_FILE")" 2>/dev/null
    rm -f "$PID_FILE"
fi
# Also kill any orphan on port 8080
lsof -ti:8080 | xargs kill -9 2>/dev/null
sleep 1

# Generate tasks
scripts/md_to_talaria.sh

# Start server in background
python3 scripts/server.py > "$LOG" 2>&1 &
echo $! > "$PID_FILE"
sleep 1

# Check if started
if ! kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "Failed to start. Check $LOG"
    cat "$LOG"
    exit 1
fi

xdg-open http://localhost:8080 2>/dev/null &

echo "Talaria running on http://localhost:8080"

while true; do
    echo ""
    echo "[1] Minimize (continue in background)"
    echo "[2] Show logs"
    echo "[3] Stop & exit"
    read -p "> " choice
    case $choice in
        1) echo "Running in background. PID: $(cat $PID_FILE)"; break ;;
        2) echo "--- Logs (last 20 lines) ---"; tail -20 "$LOG"; echo "---" ;;
        3) kill "$(cat "$PID_FILE")" 2>/dev/null; rm -f "$PID_FILE"; echo "Stopped."; break ;;
        *) echo "Invalid" ;;
    esac
done
