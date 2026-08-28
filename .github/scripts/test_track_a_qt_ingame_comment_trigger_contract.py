#!/usr/bin/env python3
from pathlib import Path

TRIGGER = Path('.github/workflows/track-a-qt-ingame-comment-trigger.yml').read_text(encoding='utf-8')
LIVE = Path('.github/workflows/track-a-qt-ingame-live-correlation.yml').read_text(encoding='utf-8')


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


require('issue_comment:' in TRIGGER, 'owner comment trigger must remain issue_comment based')
require("github.actor == 'blakinio'" in TRIGGER, 'owner identity guard missing')
require("github.event.comment.body == 'ONE_SHOT_QT_INGAME_CORRELATION'" in TRIGGER, 'exact owner command guard missing')
require('uses: ./.github/workflows/track-a-qt-ingame-live-correlation.yml' in TRIGGER, 'comment trigger must call the reusable correlation workflow directly')
require('authorization: ONE_SHOT_QT_INGAME_CORRELATION' in TRIGGER, 'reusable call must bind exact authorization input')
require("duration_seconds: '900'" in TRIGGER, 'reusable call must bind the bounded 900-second window')
require('actions: write' not in TRIGGER, 'direct reusable call must not require actions:write')
require('/dispatches' not in TRIGGER, 'GITHUB_TOKEN API dispatch must not be used because it loses the owner actor')
require('GH_TOKEN' not in TRIGGER, 'comment trigger must not dispatch through a token-bearing shell step')
require('workflow_call:' in LIVE, 'correlation workflow must expose workflow_call for actor-preserving owner comments')
require("github.actor == 'blakinio'" in LIVE, 'correlation workflow must retain its owner actor gate')
require("inputs.authorization == 'ONE_SHOT_QT_INGAME_CORRELATION'" in LIVE, 'correlation workflow must retain exact authorization input gate')
print('TRACK_A_QT_INGAME_COMMENT_TRIGGER_CONTRACT=PASS')
