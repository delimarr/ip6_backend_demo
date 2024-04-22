"""Slim backend with REST Api."""
from __future__ import annotations

from queue import Queue
from threading import Thread
from typing import TYPE_CHECKING

import pandas as pd
from flask import Flask

from ebl_coords.backend.command.invoker import Invoker
from ebl_coords.backend.constants import CALLBACK_DT_MS, CONFIG_JSON, ECOS_DF_LOCK, MOCK_FLG
from ebl_coords.backend.ecos import get_ecos_df, get_ecos_df_live, get_ecos_df_mock, load_config
from ebl_coords.backend.observable.ecos_subject import EcosSubject
from ebl_coords.backend.observable.gtcommand_subject import GtCommandSubject
from ebl_coords.backend.observable.stream_observer import StreamObserver
from ebl_coords.graph_db.graph_db_api import GraphDbApi

if TYPE_CHECKING:
    from ebl_coords.backend.command.command import Command

DOCKER_IP: str = "0.0.0.0"
DEVICE_IP: str = "192.168.103.98"
PORT: int = 42069


class EblCoords:
    """Main Backend."""

    def __init__(self) -> None:
        """Initialize and show the gui."""
        super().__init__()

        self.worker_queue: Queue[Command] = Queue()
        self.invoker = Invoker()
        self.invoker.start_loop(self.worker_queue, CALLBACK_DT_MS / 1000)

        self.bpks, self.ecos_config = load_config(config_file=CONFIG_JSON)
        self.ecos_df: pd.DataFrame

        if MOCK_FLG:
            ecos_ids = get_ecos_df_mock(self.ecos_config, self.bpks)["id"]
        else:
            ecos_ids = get_ecos_df_live(self.ecos_config)["id"]
        self.ecos = EcosSubject(ecos_config=self.ecos_config, ecos_ids=ecos_ids)
        self.ecos.start_record()

        self.update_ecos_df()

        self.graphdb = GraphDbApi()

        self.ip = DOCKER_IP
        self.port = PORT

    def update_ecos_df(self) -> None:
        """Crawl all ecos sockets, rebuild ecos_df."""
        df = get_ecos_df(config=self.ecos_config, bpks=self.bpks)
        with ECOS_DF_LOCK:
            self.ecos_df = df

    def attach_stream_socket(self) -> None:
        """Attach a stream observer to the gt_command_subject."""
        stream_obs = StreamObserver(self.ip, self.port)
        self.port += 1
        GtCommandSubject().attach_all_coord(stream_obs)


app = Flask(__name__)
ebl_coords = EblCoords()


@app.post("/attach")  # type: ignore
def attach() -> str:
    """Return local ipv4 port of tcp socket streaming all filtered coords from gt command.

    Returns:
        str: ip:port
    """
    Thread(target=ebl_coords.attach_stream_socket).start()
    return f"{DEVICE_IP}" ":" f"{PORT}"
    # return f"{DEVICE_IP}:{PORT}"
