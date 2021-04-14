""" rate client module """
import socket
import sys

try:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(("localhost", 5000))

        print(client_socket.recv(2048).decode("UTF-8"))

        while True:

            command = input("> ")

            if command == "exit":
                break
            else:
                client_socket.sendall(command.encode("UTF-8"))
                print(client_socket.recv(2048).decode("UTF-8"))

        client_socket.close()
except ConnectionResetError:
    print("Server connection was closed.")
except ConnectionRefusedError:
    print("Server is not running.")
except KeyboardInterrupt:
    pass

sys.exit(0)
