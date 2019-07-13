env/bin/python3 file_server.py </dev/null &>/dev/null &
env/bin/python3 tornado_websocket.py </dev/null &>/dev/null &
echo "Go to localhost:8081"
open http://localhost:8081/