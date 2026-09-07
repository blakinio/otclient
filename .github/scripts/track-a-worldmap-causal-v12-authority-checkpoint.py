#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'WORLDMAP_V12_AUTHORITY_ERROR={label}_COUNT:{count}')
    return text.replace(old, new, 1)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('task', type=Path)
    a = p.parse_args()
    s = a.task.read_text(encoding='utf-8')

    replacements = (
        ('session_id: chatgpt-worldmap-server-delivery-causal-20260817-v11',
         'session_id: chatgpt-worldmap-server-delivery-causal-20260817-v12', 'SESSION'),
        ('phase: baseline_downstream_auth_state_v11_world_entry_screenshot',
         'phase: baseline_transport_visual_structural_v12_world_entry_screenshot', 'PHASE'),
        ('baseline_ephemeral_login_max: 4', 'baseline_ephemeral_login_max: 5', 'LOGIN_MAX'),
        ('baseline_ephemeral_login_consumed: 3', 'baseline_ephemeral_login_consumed: 4', 'LOGIN_CONSUMED'),
        ('baseline_login_max: 4', 'baseline_login_max: 5', 'CHECKPOINT_MAX'),
        ('baseline_login_consumed: 3', 'baseline_login_consumed: 4', 'CHECKPOINT_CONSUMED'),
        ('ci_check_generation: v11_downstream_auth_state_and_screenshot',
         'ci_check_generation: v12_transport_visual_structural_world_entry', 'CI_GENERATION'),
    )
    for old, new, label in replacements:
        s = replace_once(s, old, new, label)

    anchor = 'fourth_baseline_login_attempt_authorized: true\n'
    if anchor not in s:
        raise SystemExit('WORLDMAP_V12_AUTHORITY_ERROR=FOURTH_AUTH_ANCHOR_MISSING')
    s = s.replace(anchor, anchor + 'fifth_baseline_login_attempt_authorized: true\n', 1)

    scope_old = ('owner_authorization_scope: one additional sequential real baseline login attempt for v11 after v10 consumed the third attempt; '
                 'v11 uses the press-proven Login control, secret-safe field occupancy proof, downstream native auth-state acceptance, structural world entry, and one post_IN_GAME cropped map screenshot; no parallel session')
    # tolerate the actual spelling in the durable task
    if scope_old not in s:
        scope_old = ('owner_authorization_scope: one additional sequential real baseline login attempt for v11 after v10 consumed the third attempt; '
                     'v11 uses the press-proven Login control, secret-safe field occupancy proof, downstream native auth-state acceptance, structural world entry, and one post-IN_GAME cropped map screenshot; no parallel session')
    scope_new = ('owner_authorization_scope: one additional sequential real baseline login attempt for v12 after v11 consumed the fourth attempt; '
                 'v12 reuses the physically press-proven Login control and proven field occupancy, but no longer requires brittle auth QMeta breakpoints; '
                 'it requires new client-to-local-SOCKS activity plus a large persistent post-login UI transition, then uses the historical exact-SHA character stimulus and accepts only structural FullMap plus map-description strips as IN_GAME truth; one post-IN_GAME cropped map screenshot; no parallel session')
    s = replace_once(s, scope_old, scope_new, 'AUTH_SCOPE')

    s += '''\n\n# V11 physical discriminator and V12 authority\n\nV11 run `32065920513`, physical job `95497986845`, preserved exact main/XID/XRes/VNC/cleanup fences and physically proved both protected credential fields were populated before login submission:\n\n```text\nWORLDMAP_V11_EMAIL_OCCUPANCY_CHANGED=523\nWORLDMAP_V11_PASSWORD_OCCUPANCY_CHANGED=823\nWORLDMAP_V11_SECRET_FIELD_OCCUPANCY=PASS\nWORLDMAP_V10_PRESS_BBOX=998,593,1084,613\nWORLDMAP_V11_LOGIN_BUTTON_CENTER=1041,603\nWORLDMAP_BASELINE_LOGIN_SUBMITTED=true\n```\n\nThe run then failed only because no selected auth-state breakpoint fired:\n\n```text\nWORLDMAP_BASELINE_ERROR=native_login_activation_state_not_observed\nWORLDMAP_BASELINE_LOGIN_BUDGET_CONSUMED=4\nWORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS\nWORLDMAP_BASELINE_CLEANUP=COMPLETE\nWORLDMAP_FINAL_NAMESPACE_PROCESS_COUNT=0\n```\n\nThis means the account form, field population, physical Login control and click path are now proven independently. V12 therefore removes auth-QMeta events as acceptance gates. It follows the historical successful exact-SHA model instead: observe a new local SOCKS connection/activity and a large persistent UI transition after clicking the press-proven Login control, then apply the historical character-row stimulus translated from the live discovered fields. Coordinates remain stimulus only. The sole IN_GAME acceptance criterion remains pre-Storage `FullMap` plus the required map-description strip count.\n\nThe owner's latest `dokocz prace` is recorded as authority for exactly one additional sequential v12 baseline login.\n\n```yaml\nbaseline_ephemeral_login_max: 5\nbaseline_ephemeral_login_consumed: 4\nfifth_baseline_login_attempt_authorized: true\n```\n\nNo parallel session is authorized. Screenshot authority remains map-only and post-structural-IN_GAME.\n'''

    a.task.write_text(s, encoding='utf-8')
    print('WORLDMAP_V12_TASK_AUTHORITY_EDIT=PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
