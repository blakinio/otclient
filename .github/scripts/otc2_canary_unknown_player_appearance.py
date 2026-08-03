import subprocess

BRANCH = "feat/OTC2-20260803-canary-unknown-player-appearance"

subprocess.run(["git", "fetch", "origin", "main"], check=True)
subprocess.run(["git", "rebase", "origin/main"], check=True)
subprocess.run(
    ["git", "push", "--force-with-lease", "origin", f"HEAD:{BRANCH}"],
    check=True,
)
