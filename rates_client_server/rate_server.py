""" rate server module """
from typing import Optional
import multiprocessing as mp
import socket
import sys


# Create "ClientConnectionThread" class that inherits from "Thread"

# Each time a client connects, a new thread should be created with the
# "ClientConnectionThread" class. The class is responsible for sending the
# welcome message and interacting with the client, echoing messages

# Use a multiprocessing shared "Value" object to track the count of
# connected clients
# increment the count when a client connects, and decrement the count when
# a client disconnects
# add new server command named "count" that displays the count of
# connected clients


def rate_server(host: str, port: int) -> None:
    """rate server"""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:

        socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_server.bind((host, port))
        socket_server.listen(100)

        conn, _ = socket_server.accept()

        conn.sendall(b"Connected to the Rate Server")

        try:
            while True:
                data = conn.recv(2048)
                if not data:
                    break
                conn.sendall(data)
        except OSError:
            pass


class RateServerError(Exception):
    """ rate server error class """


def command_start_server(server_process: Optional[mp.Process]) -> None:
    """ command start server """

    if server_process and server_process.is_alive():
        print("server is already running")
    elif server_process:
        server_process.start()
        print("server started")
    else:
        raise RateServerError("server process cannot be null")


def command_stop_server(server_process: Optional[mp.Process]) -> None:
    """ command stop server """

    if not server_process or not server_process.is_alive():
        print("server is not running")
    else:
        server_process.terminate()
        print("server stopped")


def command_server_status(server_process: Optional[mp.Process]) -> None:
    """ command server status """
    if server_process and server_process.is_alive():
        print("server is running")
    else:
        print("server is stopped")


def main() -> None:
    """Main Function"""

    try:

        server_process: Optional[mp.Process] = None

        while True:

            command = input("> ")

            if command == "start":
                server_process = mp.Process(target=rate_server,
                                            args=("localhost", 5000))
                command_start_server(server_process)
            elif command == "stop":
                command_stop_server(server_process)
                server_process = None
            elif command == "status":
                command_server_status(server_process)
            elif command == "exit":
                if server_process and server_process.is_alive():
                    server_process.terminate()
                break

    except KeyboardInterrupt:
        if server_process and server_process.is_alive():
            server_process.terminate()

    sys.exit(0)


if __name__ == '__main__':
    main()
