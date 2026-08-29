from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROMPT = ROOT / "docs/agents/prompts/OTCLIENT_TIBIA_GLOBAL_LOGIN_FINAL_CONTINUE.md"
REGISTRY = ROOT / "docs/agents/SHORT_COMMANDS.md"


def require(text: str, needle: str, context: str) -> None:
    if needle not in text:
        raise AssertionError(f"{context}: missing required contract token: {needle}")


def main() -> None:
    if not PROMPT.is_file():
        raise AssertionError(f"missing canonical prompt: {PROMPT.relative_to(ROOT)}")

    prompt = PROMPT.read_text(encoding="utf-8")
    registry = REGISTRY.read_text(encoding="utf-8")

    require(registry, "OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE", "short-command registry")
    require(registry, "OTCLIENT_TIBIA_GLOBAL_LOGIN_FINAL_CONTINUE.md", "short-command registry")

    require(prompt, "PR #284", "orchestrator prompt")
    require(prompt, "BLOCKED_REQUIRED_CURRENT_NATIVE_PRE_LOGIN_OUTBOUND_SEQUENCE_EVIDENCE", "orchestrator prompt")
    require(prompt, "same invocation", "orchestrator prompt")
    require(prompt, "do not ask the owner to open a second chat/window", "orchestrator prompt")
    require(prompt, "tools/tibia-re-vision-benchmark", "orchestrator prompt")
    require(prompt, "VISION_POST_E2E=SKIPPED_NO_ACCEPTED_KEYFRAMES", "orchestrator prompt")
    require(prompt, "VISION_POST_E2E=RUN_QWEN", "orchestrator prompt")
    require(prompt, "VISION_POST_E2E=BLOCKED_LOCAL_MODEL_HOST_UNAVAILABLE", "orchestrator prompt")
    require(prompt, "visual_only", "orchestrator prompt")
    require(prompt, "structural_authority:false", "orchestrator prompt")
    require(prompt, "Never trigger or repeat an official-service E2E merely to obtain screenshots", "orchestrator prompt")
    require(prompt, "continue structural Track B work", "orchestrator prompt")

    forbidden = [
        "start TIBIA-RE-VISION-BENCHMARK in another window",
        "ask the owner to run TIBIA-RE-VISION-BENCHMARK",
        "Vision may authorize protocol mutation",
    ]
    for token in forbidden:
        if token in prompt:
            raise AssertionError(f"orchestrator prompt contains forbidden behavior: {token}")

    print("TRACK_B_VISION_ORCHESTRATOR_PROMPT_CONTRACT=PASS")


if __name__ == "__main__":
    main()
