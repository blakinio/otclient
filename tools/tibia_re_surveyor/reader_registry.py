from __future__ import annotations

from typing import Callable

from .action_protocol import read_action_protocol
from .auth_session import read_auth_session
from .player_state import read_player_state
from .ui_settings import read_ui_settings

Reader = Callable[..., dict[str, object]]

READERS: dict[str, Reader] = {
    "action_protocol_typed_reader": read_action_protocol,
    "auth_session_typed_reader": read_auth_session,
    "player_state_typed_reader": read_player_state,
    "ui_settings_typed_reader": read_ui_settings,
}

IMPLEMENTED_TYPED_READER_IDS = frozenset(READERS)
