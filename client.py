"""Example client using REST Api and listen to socket."""
from socket import AF_INET, SOCK_STREAM, socket

import requests

DELIMITER = b";"


def listen(ipv4: str, port: int) -> None:
    """Read socket and print recv to console.

    Args:
        ipv4 (str): local ipv4
        port (int): port
    """
    buffer = b""
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((ipv4, port))
        while True:
            block = sock.recv(1024)
            if not block:
                return

            while DELIMITER not in buffer:
                buffer += block

            line, _, buffer = buffer.partition(DELIMITER)
            print(line.decode("utf-8"))


if __name__ == "__main__":
    URL = "http://127.0.0.1:50000/attach"
    r = requests.post(url=URL)
    ip, my_port = r.text.split(":")
    listen(ip, int(my_port))
