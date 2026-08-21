from __future__ import annotations

from typing import Callable

from .runtime import EXPECTED_TARGET_CONTAINER
from .typed_presence import read_typed_presence

READER_ID = "action_protocol_typed_reader"
TYPE_NAME = "tibia::game::TPlayerProtocolMessageHandler"
MANGLED_TYPE_NAME = "N5tibia4game29TPlayerProtocolMessageHandlerE"


def read_action_protocol(
    *,
    pid: int,
    start_ticks: int,
    runner: Callable[[list[str]], str],
    container: str = EXPECTED_TARGET_CONTAINER,
) -> dict[str, object]:
    doc = read_typed_presence(
        reader_id=READER_ID,
        type_name=TYPE_NAME,
        mangled_name=MANGLED_TYPE_NAME,
        pid=pid,
        start_ticks=start_ticks,
        runner=runner,
        container=container,
    )
    if doc.get("state") != "AVAILABLE":
        return doc
    doc.update(
        {
            "semantic_state": "TYPED_ACTION_PROTOCOL_OBJECT_IDENTITY_ONLY",
            "protocol_message_handler_present": True,
            "action_to_protocol_connection_claimed": False,
            "serialized_message_semantics_claimed": False,
            "protocol_opcodes_claimed": False,
            "packet_payloads_retained": False,
            "in_game_claimed": False,
            "credentials_retained": False,
            "session_secrets_retained": False,
            "semantic_promotion_allowed": False,
        }
    )
    return doc
