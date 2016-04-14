pkill -f AdderServer.py
python AdderServer.py localhost 7771 &
python AdderServer.py localhost 7772 &
python client.py localhost 7771 "localhost 7772"
