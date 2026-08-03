from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, found {count}")
    return text.replace(old, new, 1)


path = Path("oteryn-client/crates/protocol-canary/src/inbound.rs")
text = path.read_text(encoding="utf-8")

text = replace_once(
    text,
    "    if state.pending_state_entered || state.session_ended {\n"
    "        return Err(CanaryInboundError::InvalidOrder);\n"
    "    }\n\n"
    "    let mut reader = BoundedReader::new(input, CANARY_NETWORK_MESSAGE_MAX_BYTES)?;\n"
    "    let opcode = reader.read_u8()?;\n"
    "    if opcode != OPCODE_PENDING_STATE_ENTERED {\n",
    "    if state.local_player.is_none()\n"
    "        || state.pending_state_entered\n"
    "        || state.enter_world_received\n"
    "        || state.session_ended\n"
    "    {\n"
    "        return Err(CanaryInboundError::InvalidOrder);\n"
    "    }\n\n"
    "    let mut reader = BoundedReader::new(input, CANARY_NETWORK_MESSAGE_MAX_BYTES)?;\n"
    "    let opcode = reader.read_u8()?;\n"
    "    if opcode != OPCODE_PENDING_STATE_ENTERED {\n",
    "pending order guard",
)

text = replace_once(
    text,
    "    fn parse_hex_fixture(input: &str) -> Result<Vec<u8>, ParseIntError> {\n"
    "        input\n"
    "            .split_whitespace()\n"
    "            .map(|token| u8::from_str_radix(token, 16))\n"
    "            .collect()\n"
    "    }\n\n"
    "    #[test]\n"
    "    fn exact_pending_state_fixture_emits_bootstrap_started() -> Result<(), Box<dyn Error>> {\n",
    "    fn parse_hex_fixture(input: &str) -> Result<Vec<u8>, ParseIntError> {\n"
    "        input\n"
    "            .split_whitespace()\n"
    "            .map(|token| u8::from_str_radix(token, 16))\n"
    "            .collect()\n"
    "    }\n\n"
    "    fn initialize_local_player(\n"
    "        state: &mut CanaryInboundBootstrapState,\n"
    "        current: SessionGeneration,\n"
    "    ) -> Result<(), Box<dyn Error>> {\n"
    "        let input = parse_hex_fixture(LOCAL_PLAYER_INITIALIZATION_FIXTURE)?;\n"
    "        state.decode_local_player_initialization(&input, current)?;\n"
    "        Ok(())\n"
    "    }\n\n"
    "    #[test]\n"
    "    fn pending_state_requires_local_player_identity() -> Result<(), Box<dyn Error>> {\n"
    "        let (mut state, current) = state(6);\n"
    "        let input = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;\n"
    "        assert_eq!(\n"
    "            decode_current_pending_state_entered(&input, &mut state, current),\n"
    "            Err(CanaryInboundError::InvalidOrder)\n"
    "        );\n"
    "        assert_eq!(state.local_player(), None);\n"
    "        assert!(!state.pending_state_entered());\n"
    "        Ok(())\n"
    "    }\n\n"
    "    #[test]\n"
    "    fn exact_pending_state_fixture_emits_bootstrap_started() -> Result<(), Box<dyn Error>> {\n",
    "test helper",
)

text = replace_once(
    text,
    "        let input = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;\n\n"
    "        let envelope = decode_current_pending_state_entered(&input, &mut state, current)?;\n",
    "        let input = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;\n"
    "        initialize_local_player(&mut state, current)?;\n\n"
    "        let envelope = decode_current_pending_state_entered(&input, &mut state, current)?;\n",
    "exact pending initialization",
)

text = replace_once(
    text,
    "            let (mut state, _) = state(8);\n"
    "            assert_eq!(\n"
    "                decode_current_pending_state_entered(input, &mut state, current),\n",
    "            let (mut state, _) = state(8);\n"
    "            initialize_local_player(&mut state, current)?;\n"
    "            assert_eq!(\n"
    "                decode_current_pending_state_entered(input, &mut state, current),\n",
    "malformed pending initialization",
)

text = replace_once(
    text,
    "    fn oversized_pending_state_input_fails_without_advancing_order() {\n"
    "        let (mut state, current) = state(9);\n"
    "        let input = vec![OPCODE_PENDING_STATE_ENTERED; CANARY_NETWORK_MESSAGE_MAX_BYTES + 1];\n\n"
    "        assert_eq!(\n",
    "    fn oversized_pending_state_input_fails_without_advancing_order(\n"
    "    ) -> Result<(), Box<dyn Error>> {\n"
    "        let (mut state, current) = state(9);\n"
    "        let input = vec![OPCODE_PENDING_STATE_ENTERED; CANARY_NETWORK_MESSAGE_MAX_BYTES + 1];\n"
    "        initialize_local_player(&mut state, current)?;\n\n"
    "        assert_eq!(\n",
    "oversized pending signature",
)

text = replace_once(
    text,
    "        assert!(!state.pending_state_entered());\n"
    "        assert!(!state.session_ended());\n"
    "    }\n\n"
    "    #[test]\n"
    "    fn duplicate_pending_state_message_fails_closed() -> Result<(), Box<dyn Error>> {\n",
    "        assert!(!state.pending_state_entered());\n"
    "        assert!(!state.session_ended());\n"
    "        Ok(())\n"
    "    }\n\n"
    "    #[test]\n"
    "    fn duplicate_pending_state_message_fails_closed() -> Result<(), Box<dyn Error>> {\n",
    "oversized pending result",
)

text = replace_once(
    text,
    "        let input = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;\n"
    "        decode_current_pending_state_entered(&input, &mut state, current)?;\n\n"
    "        assert_eq!(\n"
    "            decode_current_pending_state_entered(&input, &mut state, current),\n",
    "        let input = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;\n"
    "        initialize_local_player(&mut state, current)?;\n"
    "        decode_current_pending_state_entered(&input, &mut state, current)?;\n\n"
    "        assert_eq!(\n"
    "            decode_current_pending_state_entered(&input, &mut state, current),\n",
    "duplicate pending initialization",
)

text = replace_once(
    text,
    "        let (mut after_pending, current) = state(25);\n"
    "        decode_current_pending_state_entered(&pending, &mut after_pending, current)?;\n",
    "        let (mut after_pending, current) = state(25);\n"
    "        initialize_local_player(&mut after_pending, current)?;\n"
    "        decode_current_pending_state_entered(&pending, &mut after_pending, current)?;\n",
    "session end after pending initialization",
)

path.write_text(text, encoding="utf-8", newline="\n")

task_path = Path("docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md")
task = task_path.read_text(encoding="utf-8")
task = replace_once(
    task,
    "repair_cycles_for_current_gate: 1\n",
    "repair_cycles_for_current_gate: 3\n",
    "repair count",
)
task = replace_once(
    task,
    "validation: focused_workflow_running\n",
    "validation: exact_source_order_fail_fast_repair_running\n",
    "validation checkpoint",
)
task_path.write_text(task, encoding="utf-8", newline="\n")
