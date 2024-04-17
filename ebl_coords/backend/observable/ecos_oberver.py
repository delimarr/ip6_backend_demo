"""Observer in order to receive ecos updates."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ebl_coords.backend.command.command import Command
from ebl_coords.backend.command.ecos_cmd import UpdateStateCommand
from ebl_coords.backend.observable.observer import Observer
from ebl_coords.decorators import override

if TYPE_CHECKING:
    from queue import Queue

    from ebl_coords.backend.observable.ecos_subject import EcosSubject
    from ebl_coords.main import EblCoords


class EcosObserver(Observer):
    """Obersver pattern for ecos.

    Args:
        Observer (_type_): interface
    """

    def __init__(
        self,
        ebl_coords: EblCoords,
    ) -> None:
        """Initialize ecos observer.

        Args:
            ebl_coords (Ebl_coords): ebl_coords containing ecos_df and worker queue
        """
        self.ebl_coords = ebl_coords

    @override
    def update(self) -> None:
        """Put update command in queue."""
        self.ebl_coords.worker_queue.put(
            UpdateStateCommand(content=self.result, context=self.ebl_coords.ecos_df)
        )


class AttachEcosObsCommand(Command):
    """Create and attach an EcosObserver.

    Args:
        Command (_type_): interface
    """

    def __init__(
        self,
        content: EblCoords,
        context: EcosSubject,
    ) -> None:
        """Initialize this command.

        Args:
            content (EblCoords): ebl_coords containing worker queue and ecos_df
            context (EcosSubject): EcosSubject
        """
        super().__init__(content, context)
        self.content: Queue[Command]
        self.context: EcosSubject

    @override
    def run(self) -> None:
        """Create and attach an EcosObserver."""
        self.context.attach(
            EcosObserver(ebl_coords=self.content)
        )
