import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:

    socket_client.connect(("127.0.0.1", 5000))

    print(socket_client.recv(2048).decode("UTF-8"))

    while True:

        command = input("> ")

        if command == "exit":
            break
        else:
            socket_client.sendall(command.encode("UTF-8"))

            response = ""
            while True:
                chunk = socket_client.recv(4)
                if not chunk:
                    break
                response_chunk = chunk.decode('UTF-8')
                response += response_chunk
                if response.endswith(";"):
                    response = response[:-1]
                    break

            print(response)

           
