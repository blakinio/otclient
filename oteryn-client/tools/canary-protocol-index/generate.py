#!/usr/bin/env python3
"""Generate a deterministic source-backed Canary protocol index.

The generator intentionally records declarations and literal wire evidence only.
It never copies producer implementation bodies, captures, credentials, keys or
asset bytes into the client repository.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Iterator, Sequence

PROTOCOL_GAME_CPP = Path("src/server/network/protocol/protocolgame.cpp")
PROTOCOL_GAME_HPP = Path("src/server/network/protocol/protocolgame.hpp")
PROFILE_CPP = Path("src/server/network/protocol/protocol_profile.cpp")
PROFILE_HPP = Path("src/server/network/protocol/protocol_profile.hpp")
PORT_UTILS_HPP = Path("src/server/network/protocol/protocol_port_utils.hpp")
SESSION_HINT_HPP = Path("src/server/network/protocol/protocol_session_hint.hpp")
CORE_HPP = Path("src/core.hpp")

REQUIRED_SOURCES = (
    CORE_HPP,
    PROFILE_HPP,
    PROFILE_CPP,
    PORT_UTILS_HPP,
    SESSION_HINT_HPP,
    PROTOCOL_GAME_HPP,
    PROTOCOL_GAME_CPP,
)

PACKAGE_BY_FAMILY = {
    "bootstrap": "protocol-canary-bootstrap",
    "map": "protocol-canary-map",
    "entity": "protocol-canary-entity",
    "movement": "protocol-canary-movement",
    "player": "protocol-canary-player",
    "items": "protocol-canary-items",
    "containers": "protocol-canary-containers",
    "chat": "protocol-canary-chat",
    "combat": "protocol-canary-combat",
    "social": "protocol-canary-social",
    "economy": "protocol-canary-economy",
    "progression": "protocol-canary-progression",
    "modern": "protocol-canary-modern-features",
    "operational": "protocol-canary-operational",
    "unclassified": "protocol-canary-unclassified-review",
}

PREREQUISITE_BY_FAMILY = {
    "bootstrap": "authenticated session/profile; transport and bootstrap order",
    "map": "active session; accepted map geometry and item/entity contracts",
    "entity": "active session; known-creature cache and game-domain handles",
    "movement": "active session; authoritative map/entity state and current command generation",
    "player": "active session; local-player identity and bounded player-state contracts",
    "items": "active session; item/appearance IDs and canonical object locations",
    "containers": "active session; item handles, container handles and slot bounds",
    "chat": "active session; bounded text and authoritative channel identity",
    "combat": "active session; current creature handles and player combat state",
    "social": "active session; authoritative membership/presence state",
    "economy": "active session; item identities, balances and stale-offer rejection",
    "progression": "active session; exact profile feature and bounded progression state",
    "modern": "active session; explicit feature/build gate and selected product capability",
    "operational": "authenticated session; explicit operational authorization",
    "unclassified": "manual source review required before package assignment",
}

FAMILY_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "bootstrap",
        (
            "login",
            "challenge",
            "session",
            "entergame",
            "pendingstate",
            "worldenter",
            "motd",
            "ping",
            "logout",
            "disconnect",
        ),
    ),
    (
        "map",
        (
            "map",
            "tile",
            "floor",
            "position",
            "teleport",
            "browsefield",
            "worldlight",
            "ambient",
        ),
    ),
    (
        "entity",
        (
            "creature",
            "outfit",
            "mount",
            "effect",
            "distance",
            "animatedtext",
            "missile",
            "light",
        ),
    ),
    (
        "movement",
        (
            "walk",
            "move",
            "turn",
            "autowalk",
            "follow",
            "speed",
            "cancelwalk",
        ),
    ),
    (
        "containers",
        (
            "container",
            "browsefield",
            "depotsearch",
            "stash",
            "inbox",
        ),
    ),
    (
        "items",
        (
            "item",
            "inventory",
            "inspection",
            "lookat",
            "usewith",
            "useitem",
            "throw",
            "rotate",
            "wrap",
            "loot",
        ),
    ),
    (
        "chat",
        (
            "say",
            "channel",
            "private",
            "textmessage",
            "textwindow",
            "housewindow",
            "modalwindow",
            "npc",
            "greet",
        ),
    ),
    (
        "combat",
        (
            "attack",
            "fight",
            "combat",
            "condition",
            "cooldown",
            "spell",
            "death",
            "skull",
            "shield",
        ),
    ),
    (
        "social",
        (
            "party",
            "vip",
            "guild",
            "friend",
            "teamfinder",
            "sharedexperience",
        ),
    ),
    (
        "economy",
        (
            "market",
            "shop",
            "trade",
            "transaction",
            "resourcebalance",
            "price",
            "offer",
        ),
    ),
    (
        "progression",
        (
            "quest",
            "prey",
            "bestiary",
            "bosstiary",
            "taskhunting",
            "highscore",
            "achievement",
            "cyclopedia",
        ),
    ),
    (
        "modern",
        (
            "imbuement",
            "forge",
            "wheel",
            "gem",
            "soulseal",
            "monk",
            "proficiency",
            "vocation",
            "memorial",
            "bossdifficulty",
        ),
    ),
    (
        "player",
        (
            "player",
            "health",
            "mana",
            "skill",
            "stat",
            "capacity",
            "experience",
            "icons",
        ),
    ),
    (
        "operational",
        (
            "bugreport",
            "ruleviolation",
            "clientcheck",
            "clientdetails",
            "report",
            "debug",
        ),
    ),
)


class GenerationError(RuntimeError):
    """Deterministic source or extraction failure."""


@dataclasses.dataclass(frozen=True, order=True)
class SourceAnchor:
    path: str
    line: int


@dataclasses.dataclass(frozen=True, order=True)
class ProtocolEntry:
    direction: str
    dispatch_phase: str
    opcode: int | None
    method: str
    family: str
    package_owner: str
    prerequisite: str
    source: SourceAnchor
    profile_gates: tuple[str, ...]
    build_gates: tuple[str, ...]
    extraction: str

    def as_dict(self) -> dict[str, object]:
        return {
            "direction": self.direction,
            "dispatch_phase": self.dispatch_phase,
            "opcode": self.opcode,
            "opcode_hex": None if self.opcode is None else f"0x{self.opcode:02X}",
            "method": self.method,
            "family": self.family,
            "package_owner": self.package_owner,
            "state_prerequisite": self.prerequisite,
            "source": dataclasses.asdict(self.source),
            "profile_gates": list(self.profile_gates),
            "build_gates": list(self.build_gates),
            "extraction": self.extraction,
        }


@dataclasses.dataclass(frozen=True)
class SourceDocument:
    path: Path
    text: str
    lines: tuple[str, ...]

    @classmethod
    def read(cls, root: Path, path: Path) -> "SourceDocument":
        full = root / path
        if not full.is_file():
            raise GenerationError(f"required producer source is missing: {path.as_posix()}")
        text = full.read_text(encoding="utf-8")
        return cls(path=path, text=text, lines=tuple(text.splitlines()))

    def line_for_offset(self, offset: int) -> int:
        return self.text.count("\n", 0, offset) + 1


@dataclasses.dataclass(frozen=True)
class FunctionBody:
    name: str
    body: str
    line: int


@dataclasses.dataclass(frozen=True)
class IndexModel:
    producer_revision: str
    server_release: str
    client_version: int
    enabled_features: tuple[str, ...]
    profile_ids: tuple[str, ...]
    source_hashes: tuple[tuple[str, str], ...]
    entries: tuple[ProtocolEntry, ...]
    indirect_declarations: tuple[str, ...]
    unresolved_declarations: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "schema": "oteryn-canary-source-index-v1",
            "producer": {
                "repository": "blakinio/canary",
                "revision": self.producer_revision,
                "server_release": self.server_release,
                "client_version": self.client_version,
                "profile": "ProtocolProfileId::Current",
            },
            "enabled_features": list(self.enabled_features),
            "profile_ids": list(self.profile_ids),
            "source_hashes": dict(self.source_hashes),
            "entries": [entry.as_dict() for entry in self.entries],
            "indirect_declarations": list(self.indirect_declarations),
            "unresolved_declarations": list(self.unresolved_declarations),
        }


def _balanced_region(text: str, open_offset: int) -> tuple[str, int]:
    if open_offset >= len(text) or text[open_offset] != "{":
        raise GenerationError("balanced-region extraction did not start at an opening brace")
    depth = 0
    string_quote: str | None = None
    escaped = False
    line_comment = False
    block_comment = False
    index = open_offset
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if line_comment:
            if char == "\n":
                line_comment = False
            index += 1
            continue
        if block_comment:
            if char == "*" and next_char == "/":
                block_comment = False
                index += 2
                continue
            index += 1
            continue
        if string_quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == string_quote:
                string_quote = None
            index += 1
            continue
        if char == "/" and next_char == "/":
            line_comment = True
            index += 2
            continue
        if char == "/" and next_char == "*":
            block_comment = True
            index += 2
            continue
        if char in {'"', "'"}:
            string_quote = char
            index += 1
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[open_offset + 1 : index], index + 1
        index += 1
    raise GenerationError("unterminated balanced source region")


def _find_function(document: SourceDocument, pattern: str, name_group: int = 1) -> FunctionBody:
    match = re.search(pattern, document.text, re.MULTILINE)
    if match is None:
        raise GenerationError(f"required function not found in {document.path.as_posix()}: {pattern}")
    brace = document.text.find("{", match.end())
    if brace < 0:
        raise GenerationError(f"function body missing for {match.group(name_group)}")
    body, _ = _balanced_region(document.text, brace)
    return FunctionBody(
        name=match.group(name_group),
        body=body,
        line=document.line_for_offset(match.start()),
    )


def _iter_protocol_functions(document: SourceDocument) -> Iterator[FunctionBody]:
    pattern = re.compile(
        r"^[\w:<>,&*\s]+\bProtocolGame::((?:send|parse|Add)[A-Za-z0-9_]+)\s*\([^;]*?\)\s*(?:const\s*)?\{",
        re.MULTILINE,
    )
    consumed_until = -1
    for match in pattern.finditer(document.text):
        if match.start() < consumed_until:
            continue
        brace = document.text.rfind("{", match.start(), match.end())
        if brace < 0:
            continue
        try:
            body, consumed_until = _balanced_region(document.text, brace)
        except GenerationError:
            continue
        yield FunctionBody(
            name=match.group(1),
            body=body,
            line=document.line_for_offset(match.start()),
        )


def _literal_number(value: str) -> int:
    return int(value, 16 if value.lower().startswith("0x") else 10)


def _family_for(method: str) -> str:
    normalized = re.sub(r"[^a-z0-9]", "", method.lower())
    for family, needles in FAMILY_RULES:
        if any(needle in normalized for needle in needles):
            return family
    return "unclassified"


def _gates_for(body: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    features = tuple(sorted(set(re.findall(r"ProtocolFeature::([A-Za-z0-9_]+)", body))))
    build_patterns = set()
    for expression in re.findall(
        r"\b(?:version|clientVersion|getVersion\(\))\s*(?:==|!=|>=|<=|>|<)\s*[A-Za-z0-9_:.]+",
        body,
    ):
        build_patterns.add(" ".join(expression.split()))
    for expression in re.findall(r"\bCLIENT_VERSION\b", body):
        build_patterns.add(expression)
    return features, tuple(sorted(build_patterns))


def _method_from_case(case_body: str) -> tuple[str, str]:
    stripped = re.sub(r"//.*?$|/\*.*?\*/", "", case_body, flags=re.MULTILINE | re.DOTALL)
    stripped = re.sub(r"\bbreak\s*;", "", stripped).strip("{} ;\t\r\n")
    if not stripped:
        return "no-op", "no-op-dispatch"
    parse_calls = re.findall(r"\b(parse[A-Za-z0-9_]+)\s*\(", case_body)
    if parse_calls:
        unique = tuple(dict.fromkeys(parse_calls))
        return unique[0] if len(unique) == 1 else "+".join(unique), "literal-dispatch"
    game_calls = re.findall(r"(?:&Game::|\bg_game\(\)\.)([A-Za-z0-9_]+)", case_body)
    if game_calls:
        unique = tuple(dict.fromkeys(game_calls))
        return "inline:" + "+".join(unique), "inline-dispatch"
    protocol_calls = re.findall(r"\b((?:send|logout|disconnect)[A-Za-z0-9_]*)\s*\(", case_body)
    if protocol_calls:
        unique = tuple(dict.fromkeys(protocol_calls))
        return "inline:" + "+".join(unique), "inline-dispatch"
    return "unresolved-dispatch", "unresolved"


def _parse_inbound(document: SourceDocument) -> tuple[ProtocolEntry, ...]:
    dispatcher = _find_function(
        document,
        r"\bProtocolGame::(parsePacketFromDispatcher)\s*\([^)]*\)",
    )
    switch_pattern = re.compile(r"\bswitch\s*\(\s*recvbyte\s*\)\s*\{")
    switch_matches = list(switch_pattern.finditer(dispatcher.body))
    if not switch_matches:
        raise GenerationError("no recvbyte switch was found in the dispatcher")
    if len(switch_matches) == 1:
        phases = ("gameplay-session",)
    elif len(switch_matches) == 2:
        phases = ("livestream-viewer", "gameplay-session")
    else:
        phases = tuple(f"dispatch-{index + 1}" for index in range(len(switch_matches)))

    case_pattern = re.compile(r"\bcase\s+(0x[0-9A-Fa-f]+|[0-9]+)\s*:")
    entries: list[ProtocolEntry] = []
    dispatcher_offset = document.text.find(dispatcher.body)
    for switch_index, switch_match in enumerate(switch_matches):
        brace = dispatcher.body.find("{", switch_match.start(), switch_match.end())
        switch_body, _ = _balanced_region(dispatcher.body, brace)
        switch_body_offset = brace + 1
        cases = list(case_pattern.finditer(switch_body))
        for case_index, match in enumerate(cases):
            body_index = case_index
            body = ""
            while body_index < len(cases):
                end = cases[body_index + 1].start() if body_index + 1 < len(cases) else len(switch_body)
                body = switch_body[cases[body_index].end() : end]
                meaningful = re.sub(r"//.*?$|/\*.*?\*/", "", body, flags=re.MULTILINE | re.DOTALL).strip()
                if meaningful or body_index + 1 >= len(cases):
                    break
                body_index += 1
            method, extraction = _method_from_case(body)
            features, builds = _gates_for(body)
            family = _family_for(method)
            entries.append(
                ProtocolEntry(
                    direction="client-to-server",
                    dispatch_phase=phases[switch_index],
                    opcode=_literal_number(match.group(1)),
                    method=method,
                    family=family,
                    package_owner=PACKAGE_BY_FAMILY[family],
                    prerequisite=PREREQUISITE_BY_FAMILY[family],
                    source=SourceAnchor(
                        path=document.path.as_posix(),
                        line=document.line_for_offset(
                            dispatcher_offset + switch_body_offset + match.start()
                        ),
                    ),
                    profile_gates=features,
                    build_gates=builds,
                    extraction=extraction,
                )
            )
    if not entries:
        raise GenerationError("no client-to-server dispatcher cases were extracted")
    return tuple(entries)


def _first_literal_opcode(body: str) -> int | None:
    matches = list(
        re.finditer(
            r"\b(?:addByte|add<uint8_t>)\s*\(\s*(0x[0-9A-Fa-f]+|[0-9]+)\s*\)",
            body,
        )
    )
    if not matches:
        return None
    return _literal_number(matches[0].group(1))


def _parse_outbound(document: SourceDocument) -> tuple[ProtocolEntry, ...]:
    entries: list[ProtocolEntry] = []
    for function in _iter_protocol_functions(document):
        if not function.name.startswith("send"):
            continue
        opcode = _first_literal_opcode(function.body)
        features, builds = _gates_for(function.body)
        family = _family_for(function.name)
        entries.append(
            ProtocolEntry(
                direction="server-to-client",
                dispatch_phase="server-send",
                opcode=opcode,
                method=function.name,
                family=family,
                package_owner=PACKAGE_BY_FAMILY[family],
                prerequisite=PREREQUISITE_BY_FAMILY[family],
                source=SourceAnchor(path=document.path.as_posix(), line=function.line),
                profile_gates=features,
                build_gates=builds,
                extraction="literal-send" if opcode is not None else "declared-send-no-literal",
            )
        )
    if not entries:
        raise GenerationError("no server-to-client send functions were extracted")
    return tuple(entries)


def _declared_methods(document: SourceDocument, prefix: str) -> tuple[str, ...]:
    return tuple(
        sorted(
            set(
                re.findall(
                    rf"\b(?:void|bool|uint\w*|std::\w+)\s+({prefix}[A-Za-z0-9_]+)\s*\(",
                    document.text,
                )
            )
        )
    )


def _profile_ids(document: SourceDocument) -> tuple[str, ...]:
    enum = re.search(r"enum\s+class\s+ProtocolProfileId\s*:[^\{]+\{([^}]+)\}", document.text, re.DOTALL)
    if enum is None:
        raise GenerationError("ProtocolProfileId enumeration not found")
    values = []
    for raw in enum.group(1).split(","):
        value = re.sub(r"//.*", "", raw).strip()
        if value:
            values.append(value.split("=")[0].strip())
    return tuple(values)


def _current_profile_features(document: SourceDocument) -> tuple[str, ...]:
    anchor = document.text.find("currentProfile")
    if anchor < 0:
        raise GenerationError("currentProfile definition not found")
    brace = document.text.find("{", anchor)
    if brace < 0:
        raise GenerationError("currentProfile initializer missing")
    block, _ = _balanced_region(document.text, brace)
    features = tuple(sorted(set(re.findall(r"ProtocolFeature::([A-Za-z0-9_]+)", block))))
    if not features:
        raise GenerationError("currentProfile enabled feature set is empty")
    return features


def _constant(document: SourceDocument, name: str, pattern: str) -> str:
    match = re.search(pattern, document.text)
    if match is None:
        raise GenerationError(f"constant {name} not found")
    return match.group(1)


def _source_hashes(documents: Iterable[SourceDocument]) -> tuple[tuple[str, str], ...]:
    return tuple(
        sorted(
            (
                document.path.as_posix(),
                hashlib.sha256(document.text.encode("utf-8")).hexdigest(),
            )
            for document in documents
        )
    )


def build_model(source_root: Path, producer_revision: str) -> IndexModel:
    documents = {path: SourceDocument.read(source_root, path) for path in REQUIRED_SOURCES}
    core = documents[CORE_HPP]
    profile_hpp = documents[PROFILE_HPP]
    profile_cpp = documents[PROFILE_CPP]
    protocol_hpp = documents[PROTOCOL_GAME_HPP]
    protocol_cpp = documents[PROTOCOL_GAME_CPP]

    server_release = _constant(
        core,
        "SERVER_RELEASE_VERSION",
        r"SERVER_RELEASE_VERSION\s*=\s*\"([^\"]+)\"",
    )
    client_version = int(
        _constant(core, "CLIENT_VERSION", r"CLIENT_VERSION\s*=\s*([0-9]+)")
    )

    inbound = _parse_inbound(protocol_cpp)
    outbound = _parse_outbound(protocol_cpp)
    entries = tuple(
        sorted(
            inbound + outbound,
            key=lambda entry: (
                entry.direction,
                entry.dispatch_phase,
                0x1_0000 if entry.opcode is None else entry.opcode,
                entry.method,
                entry.source.line,
            ),
        )
    )

    direct_methods = {
        entry.method
        for entry in entries
        if entry.direction == "server-to-client" or entry.extraction == "literal-dispatch"
    }
    defined_methods = {function.name for function in _iter_protocol_functions(protocol_cpp)}
    declared = set(_declared_methods(protocol_hpp, "parse")) | set(
        _declared_methods(protocol_hpp, "send")
    )
    indirect = tuple(sorted((declared & defined_methods) - direct_methods))
    unresolved = tuple(sorted(declared - defined_methods))

    return IndexModel(
        producer_revision=producer_revision,
        server_release=server_release,
        client_version=client_version,
        enabled_features=_current_profile_features(profile_cpp),
        profile_ids=_profile_ids(profile_hpp),
        source_hashes=_source_hashes(documents.values()),
        entries=entries,
        indirect_declarations=indirect,
        unresolved_declarations=unresolved,
    )


def _markdown_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_protocol_markdown(model: IndexModel) -> str:
    directions = Counter(entry.direction for entry in model.entries)
    extraction = Counter(entry.extraction for entry in model.entries)
    lines = [
        "# Canary Current Source Protocol Index",
        "",
        "Status: mechanically generated exact-source evidence; not a deployed-compatibility claim  ",
        f"Producer: `blakinio/canary@{model.producer_revision}`  ",
        f"Producer release: `{model.server_release}`  ",
        f"Declared client version: `{model.client_version}`  ",
        "Profile: `ProtocolProfileId::Current`",
        "",
        "## Claim boundary",
        "",
        "This report records literal dispatch/send evidence, source anchors, feature/build gates and a proposed bounded client package. It does not copy producer method bodies, claim the inspected commit is deployed, or infer a wire layout when no literal evidence was found.",
        "",
        "## Deterministic summary",
        "",
        f"- client-to-server entries: **{directions['client-to-server']}**",
        f"- server-to-client entries: **{directions['server-to-client']}**",
        f"- literal inbound dispatches: **{extraction['literal-dispatch']}**",
        f"- inline inbound dispatches: **{extraction['inline-dispatch']}**",
        f"- explicit no-op inbound dispatches: **{extraction['no-op-dispatch']}**",
        f"- unresolved inbound dispatches: **{extraction['unresolved']}**",
        f"- literal outbound sends: **{extraction['literal-send']}**",
        f"- sends without a local literal opcode: **{extraction['declared-send-no-literal']}**",
        f"- defined indirect/orchestrator declarations: **{len(model.indirect_declarations)}**",
        f"- declarations without a source definition: **{len(model.unresolved_declarations)}**",
        "",
        "## Current profile features",
        "",
    ]
    lines.extend(f"- `{feature}`" for feature in model.enabled_features)
    lines.extend(
        [
            "",
            "## Source hashes",
            "",
            "| Source | SHA-256 |",
            "|---|---|",
        ]
    )
    lines.extend(f"| `{path}` | `{digest}` |" for path, digest in model.source_hashes)
    lines.extend(
        [
            "",
            "## Packet and send index",
            "",
            "| Direction | Phase | Opcode | Handler/send | Family | Proposed package | Gates | State/order prerequisite | Exact source | Extraction |",
            "|---|---|---:|---|---|---|---|---|---|---|",
        ]
    )
    for entry in model.entries:
        opcode = "UNKNOWN" if entry.opcode is None else f"`0x{entry.opcode:02X}`"
        gates = ", ".join(
            [*(f"feature:{gate}" for gate in entry.profile_gates), *entry.build_gates]
        ) or "none observed in local body"
        lines.append(
            "| "
            + " | ".join(
                (
                    entry.direction,
                    entry.dispatch_phase,
                    opcode,
                    f"`{_markdown_escape(entry.method)}`",
                    entry.family,
                    f"`{entry.package_owner}`",
                    _markdown_escape(gates),
                    _markdown_escape(entry.prerequisite),
                    f"`{entry.source.path}:{entry.source.line}`",
                    entry.extraction,
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Defined methods without a direct packet entry",
            "",
            "These are source-defined dispatch orchestrators or nested helpers. They are not missing implementations and are not assigned an opcode by inference.",
            "",
        ]
    )
    lines.extend(f"- `{method}`" for method in model.indirect_declarations)
    lines.extend(
        [
            "",
            "## Declarations without a source definition",
            "",
            "Only declarations absent from the inspected implementation appear here.",
            "",
        ]
    )
    lines.extend(f"- `{method}`" for method in model.unresolved_declarations)
    lines.extend(
        [
            "",
            "## Required downstream discipline",
            "",
            "- Re-read the exact source anchor before implementing any parser or encoder.",
            "- Treat `UNKNOWN` and `unresolved` as blockers for that method, not permission to guess.",
            "- Keep exact profile/build gates in the bounded protocol package.",
            "- Convert validated wire values into merged game-domain contracts rather than publishing substitute identifiers.",
            "- Require controlled fixtures before claiming deployed or end-to-end compatibility.",
            "",
        ]
    )
    return "\n".join(lines)


def _fixture_classification(family: str) -> tuple[str, str, str]:
    if family == "bootstrap":
        return (
            "controlled-environment-required",
            "synthetic framing/unit fixtures plus disposable controlled account/session capture",
            "session keys, credentials and private captures must never be committed",
        )
    if family in {"map", "entity", "movement", "player", "items", "containers", "chat", "combat"}:
        return (
            "synthetic-plus-controlled",
            "project-original malformed/boundary fixtures now; sanitized controlled packets later",
            "production equality remains unproven until exact staging evidence exists",
        )
    if family in {"social", "economy", "progression", "modern"}:
        return (
            "feature-gated-controlled",
            "project-original negative fixtures plus controlled enabled-feature evidence",
            "do not treat source declaration as configured release requirement",
        )
    if family == "operational":
        return (
            "not-release-fixture-by-default",
            "unit-only source-shape tests unless product/operations explicitly authorize more",
            "avoid staff/admin data and operational credentials",
        )
    return (
        "manual-review-required",
        "no fixture package until source ownership and exact layout are resolved",
        "unclassified methods cannot be guessed from neighboring opcodes",
    )


def render_fixture_markdown(model: IndexModel) -> str:
    by_family: dict[str, list[ProtocolEntry]] = defaultdict(list)
    for entry in model.entries:
        by_family[entry.family].append(entry)
    lines = [
        "# Canary Current Fixture Feasibility Index",
        "",
        "Status: generated provenance/feasibility metadata only  ",
        f"Producer: `blakinio/canary@{model.producer_revision}`  ",
        "No credentials, session keys, private packet captures, proprietary assets or producer implementation bodies are contained here.",
        "",
        "## Family feasibility",
        "",
        "| Family | Entries | Literal opcodes | Unknown opcodes | Feasibility | Allowed fixture source | Safety/claim boundary | Proposed package |",
        "|---|---:|---:|---:|---|---|---|---|",
    ]
    for family in sorted(by_family):
        entries = by_family[family]
        literal = sum(entry.opcode is not None for entry in entries)
        feasibility, source, boundary = _fixture_classification(family)
        lines.append(
            "| "
            + " | ".join(
                (
                    family,
                    str(len(entries)),
                    str(literal),
                    str(len(entries) - literal),
                    feasibility,
                    _markdown_escape(source),
                    _markdown_escape(boundary),
                    f"`{PACKAGE_BY_FAMILY[family]}`",
                )
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Provenance rules",
            "",
            "1. Synthetic fixtures must be project-original and describe the exact source anchor they exercise.",
            "2. Controlled runtime fixtures require an approved staging environment, disposable identity and explicit retention/redaction policy.",
            "3. Never commit credentials, session secrets, private captures or proprietary asset bytes.",
            "4. A method declaration or literal opcode proves source shape only; it does not prove deployment, configuration, ordering or product requirement.",
            "5. Re-generate this index from the pinned producer revision and require byte-identical output before accepting an update.",
            "",
            "## Suggested fixture identifiers",
            "",
        ]
    )
    for family in sorted(by_family):
        methods = sorted({entry.method for entry in by_family[family]})
        digest = hashlib.sha256("\n".join(methods).encode("utf-8")).hexdigest()[:12]
        lines.append(
            f"- `{family}`: `canary-{model.client_version}-{family}-{digest}` — metadata key only; no packet bytes embedded."
        )
    lines.append("")
    return "\n".join(lines)


def write_outputs(model: IndexModel, protocol_path: Path, fixture_path: Path, json_path: Path) -> None:
    protocol = render_protocol_markdown(model)
    fixture = render_fixture_markdown(model)
    machine = json.dumps(model.as_dict(), indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    for path, content in ((protocol_path, protocol), (fixture_path, fixture), (json_path, machine)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--producer-revision", required=True)
    parser.add_argument("--protocol-output", type=Path, required=True)
    parser.add_argument("--fixture-output", type=Path, required=True)
    parser.add_argument("--json-output", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        model = build_model(args.source_root, args.producer_revision)
        write_outputs(
            model,
            args.protocol_output,
            args.fixture_output,
            args.json_output,
        )
    except (GenerationError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
