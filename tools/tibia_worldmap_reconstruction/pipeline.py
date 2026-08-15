from __future__ import annotations

from collections import Counter
import json
from typing import Any

OBS_SCHEMA = "otclient.worldmap.observation.v1"
CATALOG_SCHEMA = "otclient.worldmap.appearance-catalog.v1"
MAPPING_SCHEMA = "otclient.worldmap.otb-mapping.v1"
SNAPSHOT_SCHEMA = "otclient.worldmap.snapshot.v1"
REFERENCE_SCHEMA = "otclient.worldmap.reference.v1"
DIFF_SCHEMA = "otclient.worldmap.diff.v1"
OTBM_PLAN_SCHEMA = "otclient.worldmap.otbm-plan.v1"

ALLOWED_ROLES = {"ground", "border", "static", "dynamic", "creature", "npc", "unknown"}
DYNAMIC_ROLES = {"dynamic", "creature", "npc"}
STATIC_ROLES = {"static", "border"}
SNAPSHOT_STATUSES = {"OK", "CONFLICT", "GROUND_UNRESOLVED", "UNKNOWN_ROLE", "UNMAPPED_ID"}


class ReconstructionError(ValueError):
    pass


def _require_int(value: Any, name: str, *, minimum: int = 0, maximum: int | None = None) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ReconstructionError(f"{name} must be an integer")
    if value < minimum or (maximum is not None and value > maximum):
        raise ReconstructionError(f"{name} out of range")
    return value


def _require_optional_int(
    value: Any, name: str, *, minimum: int = 0, maximum: int | None = None
) -> int | None:
    if value is None:
        return None
    return _require_int(value, name, minimum=minimum, maximum=maximum)


def _require_int_list(value: Any, name: str, *, maximum: int = 0xFFFFFFFF) -> list[int]:
    if not isinstance(value, list):
        raise ReconstructionError(f"{name} must be an array")
    return [_require_int(v, f"{name}[{i}]", maximum=maximum) for i, v in enumerate(value)]


def _require_nonempty_str(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReconstructionError(f"{name} must be a non-empty string")
    return value.strip()


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


def validate_observations(doc: Any) -> tuple[str, list[dict[str, Any]]]:
    if not isinstance(doc, dict) or doc.get("schema") != OBS_SCHEMA:
        raise ReconstructionError(f"observations schema must be {OBS_SCHEMA}")
    client_version = _require_nonempty_str(doc.get("client_version"), "client_version")
    records = doc.get("observations")
    if not isinstance(records, list):
        raise ReconstructionError("observations must be an array")
    out: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ReconstructionError(f"observations[{index}] must be an object")
        pos = _position(record.get("position"))
        contents = _require_int_list(record.get("contents"), f"observations[{index}].contents")
        provenance = record.get("provenance")
        if not isinstance(provenance, dict):
            raise ReconstructionError(f"observations[{index}].provenance must be an object")
        _require_nonempty_str(provenance.get("source"), f"observations[{index}].provenance.source")
        _require_nonempty_str(provenance.get("capture_id"), f"observations[{index}].provenance.capture_id")
        out.append({"position": pos, "contents": contents, "provenance": provenance})
    return client_version, out


def validate_catalog(doc: Any) -> tuple[str, dict[int, set[str]]]:
    if not isinstance(doc, dict) or doc.get("schema") != CATALOG_SCHEMA:
        raise ReconstructionError(f"appearance catalog schema must be {CATALOG_SCHEMA}")
    client_version = _require_nonempty_str(doc.get("client_version"), "client_version")
    entries = doc.get("appearances")
    if not isinstance(entries, list):
        raise ReconstructionError("appearances must be an array")
    out: dict[int, set[str]] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ReconstructionError(f"appearances[{index}] must be an object")
        cid = _require_int(entry.get("client_id"), f"appearances[{index}].client_id", maximum=0xFFFFFFFF)
        _require_nonempty_str(entry.get("evidence"), f"appearances[{index}].evidence")
        roles = entry.get("roles")
        if not isinstance(roles, list) or not roles:
            raise ReconstructionError(f"appearances[{index}].roles must be a non-empty array")
        role_set: set[str] = set()
        for role in roles:
            if not isinstance(role, str) or role not in ALLOWED_ROLES:
                raise ReconstructionError(f"appearances[{index}] contains unsupported role")
            role_set.add(role)
        if "unknown" in role_set and len(role_set) != 1:
            raise ReconstructionError(f"appearances[{index}] unknown role must stand alone")
        if "ground" in role_set and role_set & DYNAMIC_ROLES:
            raise ReconstructionError(f"appearances[{index}] ground cannot be dynamic")
        if role_set & DYNAMIC_ROLES and role_set & STATIC_ROLES:
            raise ReconstructionError(f"appearances[{index}] static and dynamic roles conflict")
        if "creature" in role_set and "npc" in role_set:
            raise ReconstructionError(f"appearances[{index}] creature and npc roles conflict")
        if cid in out and out[cid] != role_set:
            raise ReconstructionError(f"conflicting catalog definitions for client_id {cid}")
        out[cid] = role_set
    return client_version, out


def validate_mapping(doc: Any) -> tuple[str, str, dict[int, int]]:
    if not isinstance(doc, dict) or doc.get("schema") != MAPPING_SCHEMA:
        raise ReconstructionError(f"OTB mapping schema must be {MAPPING_SCHEMA}")
    client_version = _require_nonempty_str(doc.get("client_version"), "client_version")
    otb_version = _require_nonempty_str(doc.get("otb_version"), "otb_version")
    entries = doc.get("mappings")
    if not isinstance(entries, list):
        raise ReconstructionError("mappings must be an array")
    out: dict[int, int] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ReconstructionError(f"mappings[{index}] must be an object")
        client_id = _require_int(entry.get("client_id"), f"mappings[{index}].client_id", maximum=0xFFFFFFFF)
        otb_id = _require_int(entry.get("otb_id"), f"mappings[{index}].otb_id", maximum=0xFFFFFFFF)
        _require_nonempty_str(entry.get("evidence"), f"mappings[{index}].evidence")
        if client_id in out and out[client_id] != otb_id:
            raise ReconstructionError(f"conflicting OTB mappings for client_id {client_id}")
        out[client_id] = otb_id
    return client_version, otb_version, out


def reconstruct(observations_doc: Any, catalog_doc: Any, mapping_doc: Any) -> dict[str, Any]:
    observation_version, observations = validate_observations(observations_doc)
    catalog_version, catalog = validate_catalog(catalog_doc)
    mapping_version, otb_version, mapping = validate_mapping(mapping_doc)
    if len({observation_version, catalog_version, mapping_version}) != 1:
        raise ReconstructionError(
            "client_version mismatch between observations, appearance catalog and OTB mapping"
        )

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

        ground_candidates: list[int] = []
        static_ids: list[int] = []
        dynamic_ids: list[int] = []
        unknown_roles: list[int] = []
        for client_id in variants[0]:
            roles = catalog.get(client_id)
            if not roles or roles == {"unknown"}:
                unknown_roles.append(client_id)
            elif "ground" in roles:
                ground_candidates.append(client_id)
            elif roles & DYNAMIC_ROLES:
                dynamic_ids.append(client_id)
            elif roles & STATIC_ROLES:
                static_ids.append(client_id)
            else:
                unknown_roles.append(client_id)

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

    return {
        "schema": SNAPSHOT_SCHEMA,
        "client_version": observation_version,
        "otb_version": otb_version,
        "tiles": tiles,
    }


def _validate_ok_snapshot_projection(
    index: int,
    variant: list[int],
    ground_client_id: int,
    static_client_ids: list[int],
    dynamic_client_ids: list[int],
) -> None:
    static_set = set(static_client_ids)
    dynamic_set = set(dynamic_client_ids)
    if static_set & dynamic_set:
        raise ReconstructionError(f"snapshot tiles[{index}] static/dynamic client IDs overlap")
    if ground_client_id in static_set or ground_client_id in dynamic_set:
        raise ReconstructionError(f"snapshot tiles[{index}] ground overlaps another client-ID role")
    if variant.count(ground_client_id) != 1:
        raise ReconstructionError(f"snapshot tiles[{index}] OK tile requires ground exactly once in observed variant")

    accounted = [ground_client_id, *static_client_ids, *dynamic_client_ids]
    if Counter(variant) != Counter(accounted):
        raise ReconstructionError(f"snapshot tiles[{index}] OK tile fields do not account for observed variant")

    projected_static = [client_id for client_id in variant if client_id in static_set]
    projected_dynamic = [client_id for client_id in variant if client_id in dynamic_set]
    if projected_static != static_client_ids:
        raise ReconstructionError(f"snapshot tiles[{index}] static client order disagrees with observed variant")
    if projected_dynamic != dynamic_client_ids:
        raise ReconstructionError(f"snapshot tiles[{index}] dynamic client order disagrees with observed variant")


def validate_snapshot(doc: Any) -> tuple[str, str, dict[str, dict[str, Any]]]:
    if not isinstance(doc, dict) or doc.get("schema") != SNAPSHOT_SCHEMA:
        raise ReconstructionError(f"snapshot schema must be {SNAPSHOT_SCHEMA}")
    client_version = _require_nonempty_str(doc.get("client_version"), "snapshot.client_version")
    otb_version = _require_nonempty_str(doc.get("otb_version"), "snapshot.otb_version")
    tiles = doc.get("tiles")
    if not isinstance(tiles, list):
        raise ReconstructionError("snapshot tiles must be an array")

    out: dict[str, dict[str, Any]] = {}
    for index, tile in enumerate(tiles):
        if not isinstance(tile, dict):
            raise ReconstructionError(f"snapshot tiles[{index}] must be an object")
        pos = _position(tile.get("position"))
        key = _key(pos)
        if key in out:
            raise ReconstructionError(f"duplicate snapshot coordinate {key}")
        status = tile.get("status")
        if not isinstance(status, str) or status not in SNAPSHOT_STATUSES:
            raise ReconstructionError(f"snapshot tiles[{index}].status is unsupported")

        variants_raw = tile.get("observed_variants")
        if not isinstance(variants_raw, list):
            raise ReconstructionError(f"snapshot tiles[{index}].observed_variants must be an array")
        variants = [
            _require_int_list(v, f"snapshot tiles[{index}].observed_variants[{i}]")
            for i, v in enumerate(variants_raw)
        ]
        ground_client_id = _require_optional_int(
            tile.get("ground_client_id"), f"snapshot tiles[{index}].ground_client_id", maximum=0xFFFFFFFF
        )
        ground_otb_id = _require_optional_int(
            tile.get("ground_otb_id"), f"snapshot tiles[{index}].ground_otb_id", maximum=0xFFFFFFFF
        )
        static_client_ids = _require_int_list(
            tile.get("static_client_ids"), f"snapshot tiles[{index}].static_client_ids"
        )
        static_otb_ids = _require_int_list(
            tile.get("static_otb_ids"), f"snapshot tiles[{index}].static_otb_ids"
        )
        dynamic_client_ids = _require_int_list(
            tile.get("dynamic_client_ids"), f"snapshot tiles[{index}].dynamic_client_ids"
        )
        unmapped_client_ids = _require_int_list(
            tile.get("unmapped_client_ids"), f"snapshot tiles[{index}].unmapped_client_ids"
        )
        unknown_role_client_ids = _require_int_list(
            tile.get("unknown_role_client_ids"), f"snapshot tiles[{index}].unknown_role_client_ids"
        )

        if status == "OK":
            if ground_client_id is None or ground_otb_id is None:
                raise ReconstructionError(f"snapshot tiles[{index}] OK tile requires mapped ground")
            if unmapped_client_ids or unknown_role_client_ids:
                raise ReconstructionError(f"snapshot tiles[{index}] OK tile cannot contain unresolved IDs")
            if len(static_client_ids) != len(static_otb_ids):
                raise ReconstructionError(f"snapshot tiles[{index}] static client/OTB lengths differ")
            if len(variants) != 1:
                raise ReconstructionError(f"snapshot tiles[{index}] OK tile requires one observed variant")
            _validate_ok_snapshot_projection(
                index,
                variants[0],
                ground_client_id,
                static_client_ids,
                dynamic_client_ids,
            )
        elif status == "CONFLICT" and len(variants) < 2:
            raise ReconstructionError(f"snapshot tiles[{index}] CONFLICT requires multiple variants")
        elif status == "UNMAPPED_ID" and not unmapped_client_ids:
            raise ReconstructionError(f"snapshot tiles[{index}] UNMAPPED_ID requires unresolved mappings")
        elif status == "UNKNOWN_ROLE" and not unknown_role_client_ids:
            raise ReconstructionError(f"snapshot tiles[{index}] UNKNOWN_ROLE requires unknown IDs")

        out[key] = {
            "position": {"x": pos[0], "y": pos[1], "z": pos[2]},
            "status": status,
            "observed_variants": variants,
            "ground_client_id": ground_client_id,
            "ground_otb_id": ground_otb_id,
            "static_client_ids": static_client_ids,
            "static_otb_ids": static_otb_ids,
            "dynamic_client_ids": dynamic_client_ids,
            "unmapped_client_ids": unmapped_client_ids,
            "unknown_role_client_ids": unknown_role_client_ids,
        }
    return client_version, otb_version, out


def validate_reference(doc: Any) -> tuple[str, str, dict[str, dict[str, Any]]]:
    if not isinstance(doc, dict) or doc.get("schema") != REFERENCE_SCHEMA:
        raise ReconstructionError(f"reference schema must be {REFERENCE_SCHEMA}")
    source = _require_nonempty_str(doc.get("source"), "reference.source")
    otb_version = _require_nonempty_str(doc.get("otb_version"), "reference.otb_version")
    tiles = doc.get("tiles")
    if not isinstance(tiles, list):
        raise ReconstructionError("reference tiles must be an array")
    out: dict[str, dict[str, Any]] = {}
    for index, tile in enumerate(tiles):
        if not isinstance(tile, dict):
            raise ReconstructionError(f"reference tiles[{index}] must be an object")
        pos = _position(tile.get("position"))
        key = _key(pos)
        if key in out:
            raise ReconstructionError(f"duplicate reference coordinate {key}")
        ground = _require_int(
            tile.get("ground_otb_id"), f"reference tiles[{index}].ground_otb_id", maximum=0xFFFFFFFF
        )
        items = _require_int_list(tile.get("static_otb_ids"), f"reference tiles[{index}].static_otb_ids")
        out[key] = {"ground_otb_id": ground, "static_otb_ids": items}
    return source, otb_version, out


def compare(snapshot_doc: Any, reference_doc: Any) -> dict[str, Any]:
    _, snapshot_otb_version, observed = validate_snapshot(snapshot_doc)
    source, reference_otb_version, ref = validate_reference(reference_doc)
    if snapshot_otb_version != reference_otb_version:
        raise ReconstructionError("otb_version mismatch between snapshot and reference")

    coordinates = sorted(set(ref) | set(observed), key=lambda s: tuple(map(int, s.split(","))))
    diffs: list[dict[str, Any]] = []
    for coord in coordinates:
        tile = observed.get(coord)
        expected = ref.get(coord)
        if tile is None:
            status = "NOT_OBSERVED"
        elif expected is None:
            status = "REFERENCE_MISSING"
        elif tile["status"] != "OK":
            status = tile["status"]
        elif tile["ground_otb_id"] != expected["ground_otb_id"]:
            status = "GROUND_MISMATCH"
        elif tile["static_otb_ids"] == expected["static_otb_ids"]:
            status = "MATCH"
        elif sorted(tile["static_otb_ids"]) == sorted(expected["static_otb_ids"]):
            status = "STACK_ORDER_MISMATCH"
        else:
            status = "CONTENT_MISMATCH"
        diffs.append({"position": coord, "status": status, "observed": tile, "reference": expected})
    return {
        "schema": DIFF_SCHEMA,
        "reference_source": source,
        "otb_version": snapshot_otb_version,
        "diffs": diffs,
    }


def build_otbm_plan(snapshot_doc: Any) -> dict[str, Any]:
    client_version, otb_version, tiles = validate_snapshot(snapshot_doc)
    blockers: list[dict[str, Any]] = []
    export_tiles: list[dict[str, Any]] = []
    if not tiles:
        blockers.append({"position": None, "reason": "NO_TILES"})

    for key in sorted(tiles, key=lambda s: tuple(map(int, s.split(",")))):
        tile = tiles[key]
        if tile["status"] != "OK":
            blockers.append({"position": key, "reason": tile["status"]})
            continue
        export_tiles.append(
            {
                "position": dict(tile["position"]),
                "ground_otb_id": tile["ground_otb_id"],
                "static_otb_ids": list(tile["static_otb_ids"]),
            }
        )

    exportable = not blockers
    return {
        "schema": OTBM_PLAN_SCHEMA,
        "client_version": client_version,
        "otb_version": otb_version,
        "exportable": exportable,
        "blockers": blockers,
        "tiles": export_tiles if exportable else [],
    }


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(path: str, doc: Any) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(doc, handle, indent=2, sort_keys=True)
        handle.write("\n")
