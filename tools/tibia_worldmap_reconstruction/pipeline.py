from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import json

OBS_SCHEMA = "otclient.worldmap.observation.v1"
CATALOG_SCHEMA = "otclient.worldmap.appearance-catalog.v1"
MAPPING_SCHEMA = "otclient.worldmap.otb-mapping.v1"
SNAPSHOT_SCHEMA = "otclient.worldmap.snapshot.v1"
REFERENCE_SCHEMA = "otclient.worldmap.reference.v1"
DIFF_SCHEMA = "otclient.worldmap.diff.v1"
OTBM_PLAN_SCHEMA = "otclient.worldmap.otbm-plan.v1"

ALLOWED_ROLES = {"ground", "border", "static", "dynamic", "creature", "npc", "unknown"}


class ReconstructionError(ValueError):
    pass


def _require_int(value: Any, name: str, *, minimum: int = 0, maximum: int | None = None) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ReconstructionError(f"{name} must be an integer")
    if value < minimum or (maximum is not None and value > maximum):
        raise ReconstructionError(f"{name} out of range")
    return value


def _position(raw: Any) -> tuple[int, int, int]:
    if not isinstance(raw, dict):
        raise ReconstructionError("position must be an object")
    return (
        _require_int(raw.get("x"), "position.x", maximum=65535),
        _require_int(raw.get("y"), "position.y", maximum=65535),
        _require_int(raw.get("z"), "position.z", maximum=15),
    )


def _key(pos: tuple[int, int, int]) -> str:
    return f"{pos[0]},{pos[1]},{pos[2]}"


def validate_observations(doc: Any) -> list[dict[str, Any]]:
    if not isinstance(doc, dict) or doc.get("schema") != OBS_SCHEMA:
        raise ReconstructionError(f"observations schema must be {OBS_SCHEMA}")
    records = doc.get("observations")
    if not isinstance(records, list):
        raise ReconstructionError("observations must be an array")
    out: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ReconstructionError(f"observations[{index}] must be an object")
        pos = _position(record.get("position"))
        contents = record.get("contents")
        if not isinstance(contents, list):
            raise ReconstructionError(f"observations[{index}].contents must be an array")
        normalized_contents = [
            _require_int(v, f"observations[{index}].contents[{i}]", maximum=0xFFFFFFFF)
            for i, v in enumerate(contents)
        ]
        provenance = record.get("provenance", {})
        if not isinstance(provenance, dict):
            raise ReconstructionError(f"observations[{index}].provenance must be an object")
        out.append({"position": pos, "contents": normalized_contents, "provenance": provenance})
    return out


def validate_catalog(doc: Any) -> dict[int, set[str]]:
    if not isinstance(doc, dict) or doc.get("schema") != CATALOG_SCHEMA:
        raise ReconstructionError(f"appearance catalog schema must be {CATALOG_SCHEMA}")
    entries = doc.get("appearances")
    if not isinstance(entries, list):
        raise ReconstructionError("appearances must be an array")
    out: dict[int, set[str]] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ReconstructionError(f"appearances[{index}] must be an object")
        cid = _require_int(entry.get("client_id"), f"appearances[{index}].client_id", maximum=0xFFFFFFFF)
        roles = entry.get("roles")
        if not isinstance(roles, list) or not roles:
            raise ReconstructionError(f"appearances[{index}].roles must be a non-empty array")
        role_set: set[str] = set()
        for role in roles:
            if not isinstance(role, str) or role not in ALLOWED_ROLES:
                raise ReconstructionError(f"appearances[{index}] contains unsupported role")
            role_set.add(role)
        if cid in out and out[cid] != role_set:
            raise ReconstructionError(f"conflicting catalog definitions for client_id {cid}")
        out[cid] = role_set
    return out


def validate_mapping(doc: Any) -> dict[int, int]:
    if not isinstance(doc, dict) or doc.get("schema") != MAPPING_SCHEMA:
        raise ReconstructionError(f"OTB mapping schema must be {MAPPING_SCHEMA}")
    entries = doc.get("mappings")
    if not isinstance(entries, list):
        raise ReconstructionError("mappings must be an array")
    out: dict[int, int] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ReconstructionError(f"mappings[{index}] must be an object")
        client_id = _require_int(entry.get("client_id"), f"mappings[{index}].client_id", maximum=0xFFFFFFFF)
        otb_id = _require_int(entry.get("otb_id"), f"mappings[{index}].otb_id", maximum=0xFFFFFFFF)
        if client_id in out and out[client_id] != otb_id:
            raise ReconstructionError(f"conflicting OTB mappings for client_id {client_id}")
        out[client_id] = otb_id
    return out


@dataclass(frozen=True)
class TileObservation:
    position: tuple[int, int, int]
    contents: tuple[int, ...]


def reconstruct(observations_doc: Any, catalog_doc: Any, mapping_doc: Any) -> dict[str, Any]:
    observations = validate_observations(observations_doc)
    catalog = validate_catalog(catalog_doc)
    mapping = validate_mapping(mapping_doc)

    grouped: dict[tuple[int, int, int], list[tuple[int, ...]]] = {}
    for obs in observations:
        grouped.setdefault(obs["position"], []).append(tuple(obs["contents"]))

    tiles: list[dict[str, Any]] = []
    for pos in sorted(grouped):
        variants = sorted(set(grouped[pos]))
        tile: dict[str, Any] = {
            "position": {"x": pos[0], "y": pos[1], "z": pos[2]},
            "status": "OK",
            "observed_variants": [list(v) for v in variants],
            "ground_client_id": None,
            "ground_otb_id": None,
            "static_client_ids": [],
            "static_otb_ids": [],
            "dynamic_client_ids": [],
            "unmapped_client_ids": [],
            "unknown_role_client_ids": [],
        }
        if len(variants) != 1:
            tile["status"] = "CONFLICT"
            tiles.append(tile)
            continue

        contents = variants[0]
        ground_candidates: list[int] = []
        static_ids: list[int] = []
        dynamic_ids: list[int] = []
        unknown_roles: list[int] = []
        for client_id in contents:
            roles = catalog.get(client_id)
            if not roles or roles == {"unknown"} or "unknown" in roles:
                unknown_roles.append(client_id)
                continue
            if "ground" in roles:
                ground_candidates.append(client_id)
                continue
            if roles & {"dynamic", "creature", "npc"}:
                dynamic_ids.append(client_id)
                continue
            static_ids.append(client_id)

        tile["dynamic_client_ids"] = dynamic_ids
        tile["unknown_role_client_ids"] = unknown_roles
        if unknown_roles:
            tile["status"] = "UNKNOWN_ROLE"
        if len(ground_candidates) != 1:
            tile["status"] = "GROUND_UNRESOLVED"
        else:
            ground_client = ground_candidates[0]
            tile["ground_client_id"] = ground_client
            ground_otb = mapping.get(ground_client)
            tile["ground_otb_id"] = ground_otb
            if ground_otb is None:
                tile["unmapped_client_ids"].append(ground_client)

        tile["static_client_ids"] = static_ids
        for client_id in static_ids:
            otb_id = mapping.get(client_id)
            if otb_id is None:
                tile["unmapped_client_ids"].append(client_id)
            else:
                tile["static_otb_ids"].append(otb_id)
        tile["unmapped_client_ids"] = list(dict.fromkeys(tile["unmapped_client_ids"]))

        if tile["status"] == "OK" and tile["unmapped_client_ids"]:
            tile["status"] = "UNMAPPED_ID"
        tiles.append(tile)

    return {"schema": SNAPSHOT_SCHEMA, "tiles": tiles}


def validate_reference(doc: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(doc, dict) or doc.get("schema") != REFERENCE_SCHEMA:
        raise ReconstructionError(f"reference schema must be {REFERENCE_SCHEMA}")
    tiles = doc.get("tiles")
    if not isinstance(tiles, list):
        raise ReconstructionError("reference tiles must be an array")
    out: dict[str, dict[str, Any]] = {}
    for index, tile in enumerate(tiles):
        if not isinstance(tile, dict):
            raise ReconstructionError(f"reference tiles[{index}] must be an object")
        pos = _position(tile.get("position"))
        ground = _require_int(tile.get("ground_otb_id"), f"reference tiles[{index}].ground_otb_id", maximum=0xFFFFFFFF)
        items = tile.get("static_otb_ids")
        if not isinstance(items, list):
            raise ReconstructionError(f"reference tiles[{index}].static_otb_ids must be an array")
        norm_items = [_require_int(v, f"reference tiles[{index}].static_otb_ids", maximum=0xFFFFFFFF) for v in items]
        out[_key(pos)] = {"ground_otb_id": ground, "static_otb_ids": norm_items}
    return out


def compare(snapshot_doc: Any, reference_doc: Any) -> dict[str, Any]:
    if not isinstance(snapshot_doc, dict) or snapshot_doc.get("schema") != SNAPSHOT_SCHEMA:
        raise ReconstructionError(f"snapshot schema must be {SNAPSHOT_SCHEMA}")
    ref = validate_reference(reference_doc)
    observed: dict[str, dict[str, Any]] = {}
    for tile in snapshot_doc.get("tiles", []):
        pos = _position(tile.get("position"))
        observed[_key(pos)] = tile

    coordinates = sorted(set(ref) | set(observed), key=lambda s: tuple(map(int, s.split(","))))
    diffs: list[dict[str, Any]] = []
    for coord in coordinates:
        tile = observed.get(coord)
        expected = ref.get(coord)
        status = "MATCH"
        if tile is None:
            status = "NOT_OBSERVED"
        elif expected is None:
            status = "REFERENCE_MISSING"
        elif tile.get("status") == "CONFLICT":
            status = "CONFLICT"
        elif tile.get("unmapped_client_ids"):
            status = "UNMAPPED_ID"
        elif tile.get("ground_otb_id") != expected["ground_otb_id"]:
            status = "GROUND_MISMATCH"
        elif tile.get("static_otb_ids") == expected["static_otb_ids"]:
            status = "MATCH"
        elif sorted(tile.get("static_otb_ids", [])) == sorted(expected["static_otb_ids"]):
            status = "STACK_ORDER_MISMATCH"
        else:
            status = "CONTENT_MISMATCH"
        diffs.append({"position": coord, "status": status, "observed": tile, "reference": expected})
    return {"schema": DIFF_SCHEMA, "diffs": diffs}


def build_otbm_plan(snapshot_doc: Any) -> dict[str, Any]:
    if not isinstance(snapshot_doc, dict) or snapshot_doc.get("schema") != SNAPSHOT_SCHEMA:
        raise ReconstructionError(f"snapshot schema must be {SNAPSHOT_SCHEMA}")
    blockers: list[dict[str, Any]] = []
    export_tiles: list[dict[str, Any]] = []
    for tile in snapshot_doc.get("tiles", []):
        pos = _position(tile.get("position"))
        status = tile.get("status")
        if status != "OK":
            blockers.append({"position": _key(pos), "reason": status})
            continue
        if tile.get("ground_otb_id") is None:
            blockers.append({"position": _key(pos), "reason": "GROUND_UNRESOLVED"})
            continue
        if tile.get("unmapped_client_ids"):
            blockers.append({"position": _key(pos), "reason": "UNMAPPED_ID"})
            continue
        export_tiles.append({
            "position": {"x": pos[0], "y": pos[1], "z": pos[2]},
            "ground_otb_id": tile["ground_otb_id"],
            "static_otb_ids": list(tile.get("static_otb_ids", [])),
        })
    return {
        "schema": OTBM_PLAN_SCHEMA,
        "exportable": not blockers,
        "blockers": blockers,
        "tiles": export_tiles if not blockers else [],
    }


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(path: str, doc: Any) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(doc, handle, indent=2, sort_keys=True)
        handle.write("\n")
