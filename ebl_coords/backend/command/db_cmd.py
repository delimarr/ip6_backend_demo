"""Command pattern Graph Db."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ebl_coords.backend.command.command import Command
from ebl_coords.decorators import override
from ebl_coords.graph_db.data_elements.bpk_enum import Bpk
from ebl_coords.graph_db.data_elements.edge_relation_enum import TRAINRAILS
from ebl_coords.graph_db.data_elements.edge_relation_enum import EdgeRelation
from ebl_coords.graph_db.data_elements.node_dc import Node
from ebl_coords.graph_db.data_elements.switch_item_enum import SwitchItem
from ebl_coords.graph_db.graph_db_api import GraphDbApi


def get_strecken_df() -> pd.DataFrame:
    """Get df containing all trainswitches from all strecken."""
    cmd = "MATCH (node:WEICHE) RETURN node.bhf AS bhf, node.name AS name, node.node_id AS node_id"
    strecken_df = GraphDbApi().run_query(cmd)[::2]
    shape = strecken_df.shape[0]
    strecken_df = pd.concat([strecken_df] * 3, ignore_index=True)
    exits = TRAINRAILS * shape
    exits.sort()
    strecken_df.insert(strecken_df.shape[1], "exit", exits)
    mask = strecken_df.exit != EdgeRelation.NEUTRAL.value
    strecken_df.loc[mask, "node_id"] = strecken_df[mask]["node_id"].apply(lambda x: x[:-1] + "1")
    strecken_df.sort_values(by=["bhf", "name"], inplace=True)
    return strecken_df


def get_node(bpk: str, ts_number: str, relation: str) -> Node:
    """Create a node from input.

    Args:
        bpk (str): betriebspunkt
        ts_number (str): trainswitch number
        relation (str): relation from ts

    Returns:
        Node: node
    """
    strecken_df = get_strecken_df()
    n = strecken_df.loc[
        (strecken_df["bhf"] == bpk)
        & (strecken_df["name"] == ts_number)
        & (strecken_df["exit"] == relation)
    ].iloc[0, :]
    return Node(
        id=n["node_id"],
        ecos_id="",
        switch_item=SwitchItem.WEICHE,
        ts_number=n["name"],
        bpk=Bpk[bpk],
        coords=np.zeros((3,)),
    )

class DbCommand(Command):
    """Command pattern.

    Args:
        Command (_type_): interface
    """

    def __init__(self, content: str) -> None:
        """Initialize command with query.

        Args:
            content (str): query call
        """
        super().__init__(content)
        self.context: GraphDbApi = GraphDbApi()

    @override
    def run(self) -> None:
        """Execute query."""
        self.context.run_query(self.content)
