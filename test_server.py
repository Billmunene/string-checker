import pytest
import socket
import threading
from server import ThreadedTCPServer, ThreadedTCPRequestHandler, load_config

# Fixture to start and stop the server
@pytest.fixture
def server():
    HOST, PORT = "localhost", 9999
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    yield server
    server.shutdown()

def test_load_config():
    config = load_config()
    assert config['DEFAULT']['linuxpath'] == '200k.txt'
    assert config['DEFAULT'].getboolean('REREAD_ON_QUERY') is True
    assert config['DEFAULT'].getboolean('USE_SSL') is False

def test_server_response(server):
    with socket.create_connection(("localhost", 9999)) as sock:
        message = "test\n"
        sock.sendall(message.encode('utf-8'))
        response = sock.recv(1024).decode('utf-8')
        assert "DEBUG" in response
        assert "STRING EXISTS" in response or "STRING NOT FOUND" in response

def test_search_string():
    lines = ["test\n", "example\n", "sample\n"]
    assert ThreadedTCPRequestHandler.search_string(None, "test", lines) == True
    assert ThreadedTCPRequestHandler.search_string(None, "notfound", lines) == False

if __name__ == "__main__":
    pytest.main()
