""" rate server module """
from typing import Optional
import multiprocessing as mp
import sys


def rate_server() -> None:
    """rate server"""
    while True:
        pass


class RateServerError(Exception):
    """ rate server error class """


def command_start_server(server_process: Optional[mp.Process]) -> mp.Process:
    """ command start server """

    if server_process and server_process.is_alive():
        print("server is already running")
    else:
        server_process = mp.Process(target=rate_server)
        server_process.start()
        print("server started")

    return server_process


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
                server_process = command_start_server(server_process)
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