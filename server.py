import socket
import ssl
import threading
import configparser
import os
import time

# Configuration loading
config = configparser.ConfigParser()
config.read('server_config.ini')

# Server configuration
SERVER_HOST = config.get('server', 'host')
SERVER_PORT = int(config.get('server', 'port'))
SSL_ENABLED = config.getboolean('server', 'ssl_enabled')
CERTFILE = config.get('server', 'certfile')
KEYFILE = config.get('server', 'keyfile')
REREAD_ON_QUERY = config.getboolean('server', 'reread_on_query')

# File configuration
LINUX_PATH = os.path.join(os.getcwd(), config.get('file', 'path'))  # Assuming file path in configuration file

# Global variable to track if server should continue running
server_running = True

# Function to handle each client connection
def handle_client(conn, addr):
    print(f"DEBUG: Connected by {addr}")
    try:
        while True:
            start_time = time.time()  # Measure start time for execution time calculation

            data = conn.recv(1024).strip(b'\x00')
            if not data:
                break
            query_string = data.decode('utf-8').strip()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp

            print(f"DEBUG: [{timestamp}] Received query: {query_string} from {addr}")

            if REREAD_ON_QUERY:
                with open(LINUX_PATH, 'r') as file:
                    lines = file.readlines()
                result = "STRING EXISTS" if query_string + '\n' in lines else "STRING NOT FOUND"
            else:
                if 'file_contents' not in globals():
                    global file_contents
                    with open(LINUX_PATH, 'r') as file:
                        file_contents = file.readlines()
                result = "STRING EXISTS" if query_string + '\n' in file_contents else "STRING NOT FOUND"

            execution_time = time.time() - start_time  # Calculate execution time
            log_message = f"DEBUG: [{timestamp}] Query: {query_string}, Client: {addr}, Result: {result}, Execution Time: {execution_time:.6f} seconds"
            print(log_message)
            conn.sendall((result + '\n').encode('utf-8'))

    except Exception as e:
        print(f"DEBUG: Error: {str(e)}")
    finally:
        conn.close()
        print(f"DEBUG: Disconnected from {addr}")

# Function to start the server
def start_server():
    global server_running
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen()
        print(f"DEBUG: Server listening on {SERVER_HOST}:{SERVER_PORT}")
        
        while server_running:  # Loop as long as server_running is True
            try:
                conn, addr = server_socket.accept()
                if SSL_ENABLED:
                    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                    context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)
                    conn = context.wrap_socket(conn, server_side=True)

                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.start()

            except KeyboardInterrupt:
                print("DEBUG: Keyboard interrupt received, stopping server...")
                server_running = False  # Set server_running to False to exit the loop

        print("DEBUG: Server stopped.")

if __name__ == '__main__':
    start_server()
