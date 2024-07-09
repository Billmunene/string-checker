import socket
import time

def send_message(message, host, port, use_ssl):
    with socket.create_connection((host, port)) as sock:
        if use_ssl:
            sock = ssl.wrap_socket(sock)
        sock.sendall(message.encode('utf-8'))
        response = sock.recv(1024).decode('utf-8')
        return response

def benchmark_server(message, host, port, use_ssl=False, iterations=100):
    total_time = 0
    for _ in range(iterations):
        start_time = time.time()
        response = send_message(message, host, port, use_ssl)
        end_time = time.time()
        total_time += (end_time - start_time) * 1000  # Convert to milliseconds
    average_time = total_time / iterations
    return average_time

if __name__ == "__main__":
    company_host = "135.181.96.160"
    company_port = 44445
    local_host = "localhost"
    local_port = 9999

    test_string = "test"
    not_found_string = "notfound"

    # Benchmark company's server
    company_avg_time = benchmark_server(test_string, company_host, company_port, use_ssl=False)
    company_not_found_avg_time = benchmark_server(not_found_string, company_host, company_port, use_ssl=False)

    # Benchmark local server
    local_avg_time = benchmark_server(test_string, local_host, local_port, use_ssl=False)
    local_not_found_avg_time = benchmark_server(not_found_string, local_host, local_port, use_ssl=False)

    print(f"Company Server (String Found) Average Time: {company_avg_time:.2f} ms")
    print(f"Company Server (String Not Found) Average Time: {company_not_found_avg_time:.2f} ms")
    print(f"Local Server (String Found) Average Time: {local_avg_time:.2f} ms")
    print(f"Local Server (String Not Found) Average Time: {local_not_found_avg_time:.2f} ms")
