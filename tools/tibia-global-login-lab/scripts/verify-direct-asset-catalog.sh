#!/usr/bin/env bash
set -Eeuo pipefail
set +x

BASE=https://static.tibia.com/launcher/assets-current
tmp=$(mktemp -d)
cleanup() { rm -rf "$tmp"; }
trap cleanup EXIT

curl -A 'Mozilla/5.0' -fsSL --retry 3 --retry-all-errors \
  --connect-timeout 15 --max-time 180 "$BASE/assets.json" -o "$tmp/assets.json"
curl -A 'Mozilla/5.0' -fsSL --retry 3 --retry-all-errors \
  --connect-timeout 15 --max-time 60 "$BASE/assets.json.sha256" -o "$tmp/assets.json.sha256"

expected=$(awk 'NR==1{print $1}' "$tmp/assets.json.sha256")
actual=$(sha256sum "$tmp/assets.json" | awk '{print $1}')
[[ "$expected" =~ ^[0-9a-fA-F]{64}$ ]]
[[ "$actual" == "$expected" ]]
python3 - "$tmp/assets.json" <<'PY'
import json, sys
with open(sys.argv[1], 'r', encoding='utf-8') as handle:
    doc = json.load(handle)
if not isinstance(doc, (dict, list)):
    raise SystemExit('asset catalog root is not JSON object/list')
PY

echo LAB_PUBLIC_ASSET_CATALOG_DIRECT_VERIFIED=true
