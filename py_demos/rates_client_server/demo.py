""" rate server module """
from typing import Optional, Any
from multiprocessing.sharedctypes import Synchronized  # type: ignore
from datetime import datetime
import multiprocessing as mp
import decimal
import socket
import threading
import sys
import re
import json
import requests
import pyodbc

RATESAPP_CONN_OPTIONS = [
    "DRIVER={ODBC Driver 17 for SQL Server}",
    "SERVER=localhost\\SQLExpress",
    "DATABASE=ratesapp",
    "UID=sa",
    "PWD=sqldbpass",
]

RATESAPP_CONN_STRING = ";".join(RATESAPP_CONN_OPTIONS)

CLIENT_COMMAND_PARTS = [
    r"^(?P<name>[A-Z]*) ",
    r"(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2}) ",
    r"(?P<symbol>[A-Z]{3})$",
]

CLIENT_COMMAND_REGEX = re.compile("".join(CLIENT_COMMAND_PARTS))


class ClientConnectionThread(threading.Thread):
    """ client connection thread """

    def __init__(self,
                 conn: socket.socket,
                 client_count: Synchronized,
                 ) -> None:
        threading.Thread.__init__(self)
        self.conn = conn
        self.client_count = client_count

    def run(self) -> None:

        self.conn.sendall(b"Connected to the Rate Server")

        try:
            while True:
                data = self.conn.recv(2048)

                if not data:
                    break

                client_command_str: str = data.decode('UTF-8')

                client_command_match = CLIENT_COMMAND_REGEX.match(
                    client_command_str)

                if not client_command_match:
                    self.conn.sendall(b"Invalid Command Format")
                else:
                    self.process_client_command(
                        client_command_match.groupdict())

        except OSError:
            pass

        with self.client_count.get_lock():
            self.client_count.value -= 1

    def process_client_command(self, client_command: dict[str, Any]) -> None:
        """ process client command """

        if client_command["name"] == "GET":

            with pyodbc.connect(RATESAPP_CONN_STRING) as con:

                closing_date = datetime.strptime(
                    client_command["date"], "%Y-%m-%d")
                currency_symbol = str(client_command["symbol"])

                sql = " ".join([
                    "select closingdate, currencysymbol, exchangerate",
                    "from rates",
                    "where closingdate = ? and currencysymbol = ?"])

                cur = con.cursor()

                cur.execute(sql, (closing_date, currency_symbol))

                rate = cur.fetchone()

                if rate:
                    exchange_rate = str(rate.exchangerate)
                    self.conn.sendall(exchange_rate.encode("UTF-8"))
                    return

                url = "".join([
                    "https://api.ratesapi.io/api/",
                    client_command["date"],
                    "?base=USD&symbols=",
                    client_command["symbol"],
                ])

                response = requests.request("GET", url)

                rate_data = json.loads(response.text)

                sql = " ".join([
                    "insert into rates",
                    "(closingdate, currencysymbol, exchangerate)",
                    "values",
                    "(?, ?, ?)",
                ])

                exchange_rate = decimal.Decimal(  # type: ignore
                    str(rate_data["rates"][client_command["symbol"]]))

                con.execute(
                    sql, (closing_date, currency_symbol, exchange_rate))

                self.conn.sendall(
                    str(rate_data["rates"][client_command["symbol"]])
                    .encode("UTF-8"))
        else:
            self.conn.sendall(b"Invalid Command Name")


def rate_server(host: str, port: int, client_count: Synchronized) -> None:
    """rate server"""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:

        socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_server.bind((host, port))
        socket_server.listen(100)

        while True:

            conn, _ = socket_server.accept()

            client_con_thread = ClientConnectionThread(conn, client_count)
            client_con_thread.start()

            with client_count.get_lock():
                client_count.value += 1


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


def command_client_count(client_count: int) -> None:
    """ command client count """

    print(f"client count: {client_count}")


def main() -> None:
    """Main Function"""

    try:

        client_count: Synchronized = mp.Value('i', 0)
        server_process: Optional[mp.Process] = None

        while True:

            command = input("> ")

            if command == "start":
                server_process = mp.Process(target=rate_server,
                                            args=("localhost", 5000,
                                                  client_count))
                command_start_server(server_process)
            elif command == "stop":
                command_stop_server(server_process)
                server_process = None
            elif command == "status":
                command_server_status(server_process)
            elif command == "count":
                command_client_count(client_count.value)
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
