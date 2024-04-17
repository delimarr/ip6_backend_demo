import requests
from socket import socket, AF_INET, SOCK_STREAM

DELIMITER = b";"

def listen(ip: str, port: int) -> None:
    buffer = b""
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((ip, port))
        while True:
            block = sock.recv(1024)
            if not block:
                return

            while DELIMITER not in buffer:
                buffer += block
            
            line, _, buffer = buffer.partition(DELIMITER)
            print(line.decode("utf-8"))


if __name__=="__main__":
    url = "http://127.0.0.1:5000/attach"
    r = requests.post(url=url)
    ip, port = r.text.split(":")
    port = int(port)
    listen(ip, port)
