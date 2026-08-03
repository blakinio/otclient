from pathlib import Path
import re

path = Path("oteryn-client/crates/protocol-canary/src/tile.rs")
text = path.read_text(encoding="utf-8")
replacements = [
    (
        "/// Rejects stale or pre-enter-world state, terminal sessions, truncation,\n",
        "/// Rejects stale or pre-bootstrap state, terminal sessions, truncation,\n",
        "tile docs order",
    ),
    (
        "    if !state.enter_world_received() || state.session_ended() {\n",
        "    if !state.bootstrap_completed() || state.session_ended() {\n",
        "tile bootstrap gate",
    ),
    (
        "    use crate::inbound::decode_current_pending_state_entered;\n",
        "    use crate::inbound::decode_current_pending_state_entered;\n    use crate::map::decode_current_local_player_only_map;\n",
        "tile map test import",
    ),
    (
        "    const ENTER_WORLD_FIXTURE: &str =\n        include_str!(\"../../../tests/integration/canary-world-protocol/fixtures/enter-world.hex\");\n",
        "    const ENTER_WORLD_FIXTURE: &str =\n        include_str!(\"../../../tests/integration/canary-world-protocol/fixtures/enter-world.hex\");\n    const LOCAL_PLAYER_ONLY_MAP_FIXTURE: &str = include_str!(\n        \"../../../tests/integration/canary-world-protocol/fixtures/local-player-only-map.hex\"\n    );\n",
        "tile map fixture",
    ),
]
for old, new, label in replacements:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, found {count}")
    text = text.replace(old, new, 1)

helper_pattern = re.compile(
    r"    fn ready_state\(\n        generation: u64,\n    \) -> Result<\(CanaryInboundBootstrapState, SessionGeneration\), Box<dyn Error>> \{\n.*?        Ok\(\(state, current\)\)\n    \}\n",
    re.DOTALL,
)
helper_replacement = '''    fn entered_state(
        generation: u64,
    ) -> Result<(CanaryInboundBootstrapState, SessionGeneration), Box<dyn Error>> {
        let current = SessionGeneration::new(generation);
        let mut state = CanaryInboundBootstrapState::new(SessionToken::new(current));
        let local = parse_hex_fixture(LOCAL_PLAYER_INITIALIZATION_FIXTURE)?;
        state.decode_local_player_initialization(&local, current)?;
        let permission = parse_hex_fixture(ALLOW_BUG_REPORT_FIXTURE)?;
        state.decode_allow_bug_report(&permission, current)?;
        let time = parse_hex_fixture(TIBIA_TIME_FIXTURE)?;
        state.decode_tibia_time(&time, current)?;
        let pending = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;
        decode_current_pending_state_entered(&pending, &mut state, current)?;
        let enter = parse_hex_fixture(ENTER_WORLD_FIXTURE)?;
        state.decode_enter_world(&enter, current)?;
        Ok((state, current))
    }

    fn ready_state(
        generation: u64,
    ) -> Result<(CanaryInboundBootstrapState, SessionGeneration), Box<dyn Error>> {
        let (mut state, current) = entered_state(generation)?;
        let map = parse_hex_fixture(LOCAL_PLAYER_ONLY_MAP_FIXTURE)?;
        decode_current_local_player_only_map(&map, &mut state, current)?;
        Ok((state, current))
    }
'''
text, count = helper_pattern.subn(helper_replacement, text, count=1)
if count != 1:
    raise SystemExit("tile ready-state helper anchor not found")

test_pattern = re.compile(
    r"    #\[test\]\n    fn tile_clear_requires_enter_world_and_current_session\(\) -> Result<\(\), Box<dyn Error>> \{\n.*?        Ok\(\(\)\)\n    \}\n",
    re.DOTALL,
)
test_replacement = '''    #[test]
    fn tile_clear_requires_completed_bootstrap_and_current_session() -> Result<(), Box<dyn Error>> {
        let current = SessionGeneration::new(44);
        let state = CanaryInboundBootstrapState::new(SessionToken::new(current));
        let input = parse_hex_fixture(TILE_CLEAR_FIXTURE)?;
        assert_eq!(
            decode_current_empty_tile_update(&input, &state, current),
            Err(CanaryInboundError::InvalidOrder)
        );

        let (entered, entered_current) = entered_state(45)?;
        assert_eq!(
            decode_current_empty_tile_update(&input, &entered, entered_current),
            Err(CanaryInboundError::InvalidOrder)
        );

        let (ready, actual) = ready_state(46)?;
        assert_eq!(
            decode_current_empty_tile_update(
                &input,
                &ready,
                SessionGeneration::new(actual.get() + 1),
            ),
            Err(CanaryInboundError::Domain(DomainError::StaleSession {
                expected: SessionGeneration::new(actual.get() + 1),
                actual,
            }))
        );
        Ok(())
    }
'''
text, count = test_pattern.subn(test_replacement, text, count=1)
if count != 1:
    raise SystemExit("tile order test anchor not found")
path.write_text(text, encoding="utf-8", newline="\n")

for doc_path in [
    Path("docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md"),
    Path("oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md"),
]:
    doc = doc_path.read_text(encoding="utf-8")
    if "current_session_after_enter_world" not in doc:
        raise SystemExit(f"{doc_path}: tile prerequisite anchor not found")
    doc = doc.replace(
        "current_session_after_enter_world",
        "current_session_after_bootstrap_completed",
    )
    doc_path.write_text(doc, encoding="utf-8", newline="\n")
