"""Open socket and stream all points."""
from __future__ import annotations

from socket import socket

from ebl_coords.backend.observable.observer import Observer
from ebl_coords.decorators import override

DELIMITER = ";"


class StreamObserver(Observer):
    """Streaming observer."""

    def __init__(self, ip: str, port: int) -> None:
        """Open a tcp socket.

        Args:
            ip (str): ip4v
            port (int): port
        """
        self.ip = ip
        self.port = port
        self.sock = socket()
        self.sock.bind((self.ip, self.port))
        self.sock.listen()
        self.conn, _ = self.sock.accept()

    def __del__(self) -> None:
        """Close socket."""
        self.sock.close()

    @override
    def update(self) -> None:
        """Send [x, y, z]; to socket."""
        msg = f"[{self.result[0]} {self.result[1]} {self.result[2]}]{DELIMITER}"
        self.conn.send(msg.encode("utf-8"))
