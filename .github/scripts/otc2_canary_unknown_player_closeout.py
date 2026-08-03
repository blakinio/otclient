from pathlib import Path
import re
import subprocess

paths = [
    Path("docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md"),
    Path("oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md"),
]
for path in paths:
    text = path.read_text(encoding="utf-8")
    text = text.replace("review_id: 4848922295", "review_id: 4848927049")
    text = text.replace("run: 30857235344\n  job: 91830964717", "run: 30857020465\n  job: 91830290527")
    path.write_text(text, encoding="utf-8", newline="\n")

task = paths[0].read_text(encoding="utf-8")
task, count = re.subn(
    r"related_prs: \[([^\]]*)\]",
    lambda match: "related_prs: [" + match.group(1).rstrip() + ", 250, 251]",
    task,
    count=1,
)
if count != 1:
    raise SystemExit("task related_prs anchor not found")
paths[0].write_text(task, encoding="utf-8", newline="\n")

subprocess.run(
    ["git", "rm", ".github/workflows/otc2-canary-unknown-player-closeout.yml"],
    check=True,
)
