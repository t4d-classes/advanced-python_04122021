import socket


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:

    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_server.bind(('127.0.0.1', 5000))
    socket_server.listen(10)

    conn, addr = socket_server.accept()

    print(addr)

    conn.sendall(b"Connected")
    # conn.sendall("Connected".encode("UTF-8"))

    try:
        while True:
            data = conn.recv(2048)
            response = data.decode('UTF-8') + ";"
            if not data:
                break
            conn.sendall(response.encode("UTF-8"))
    except OSError:
        pass



