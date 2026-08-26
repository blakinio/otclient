#!/usr/bin/env python3
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    wf = root / '.github/workflows/tibia-official-client-re-gameserver-tcp-writer-provenance.yml'
    text = wf.read_text(encoding='utf-8')
    required = [
        'ubuntu-24.04',
        'tibiaclient-linux-current',
        'package.json',
        'tools/tibia_re_current_game_login_schema/probe.py',
        'CURRENT_GAME_LOGIN_SCHEMA_PROBE=PASS',
        'RAW_CLIENT_RETAINED=false',
    ]
    for token in required:
        assert token in text, token
    forbidden = [
        'runs-on: [otclient, synology]',
        'e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe',
        '15.32.df7b29',
    ]
    for token in forbidden:
        assert token not in text, token
    print('CURRENT_GAME_LOGIN_SCHEMA_WORKFLOW_CONTRACT=PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())