#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/configure-github-repository.sh [--repo OWNER/REPO] [--dry-run | --apply]

Inspect and optionally apply the approved repository merge settings. The default
mode is --dry-run. This script never changes visibility, the default branch,
branches, branch protection, or rulesets.
EOF
}

mode="dry-run"
mode_was_set="false"
repository=""

while (( $# > 0 )); do
  case "$1" in
    --apply|--dry-run)
      requested_mode="${1#--}"
      if [[ "${mode_was_set}" == "true" && "${mode}" != "${requested_mode}" ]]; then
        echo "error: --apply and --dry-run are mutually exclusive" >&2
        exit 2
      fi
      mode="${requested_mode}"
      mode_was_set="true"
      shift
      ;;
    --repo)
      if (( $# < 2 )); then
        echo "error: --repo requires OWNER/REPO" >&2
        exit 2
      fi
      repository="$2"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if ! command -v gh >/dev/null 2>&1; then
  echo "error: GitHub CLI (gh) is required" >&2
  exit 127
fi

if ! gh auth status --hostname github.com >/dev/null 2>&1; then
  echo "error: GitHub CLI is not authenticated for github.com; run 'gh auth login'" >&2
  exit 1
fi

if [[ -z "${repository}" ]]; then
  if ! repository="$(gh repo view --json nameWithOwner --jq '.nameWithOwner')"; then
    echo "error: could not determine the repository; pass --repo OWNER/REPO" >&2
    exit 1
  fi
fi

if [[ ! "${repository}" =~ ^[^/[:space:]]+/[^/[:space:]]+$ ]]; then
  echo "error: invalid repository '${repository}'; expected OWNER/REPO" >&2
  exit 2
fi

setting_names=(
  allow_auto_merge
  allow_update_branch
  allow_squash_merge
  allow_merge_commit
  allow_rebase_merge
  delete_branch_on_merge
)
desired_values=(true true true false false true)

current_values_line="$(
  gh api "repos/${repository}" \
    --jq '[.allow_auto_merge, .allow_update_branch, .allow_squash_merge, .allow_merge_commit, .allow_rebase_merge, .delete_branch_on_merge] | map(tostring) | @tsv'
)"
IFS=$'\t' read -r -a current_values <<< "${current_values_line}"

if (( ${#current_values[@]} != ${#desired_values[@]} )); then
  echo "error: GitHub API returned an unexpected repository settings payload" >&2
  exit 1
fi

drift="false"
printf 'Repository: %s\nMode: %s\n\nRepository merge settings:\n' "${repository}" "${mode}"
for index in "${!setting_names[@]}"; do
  printf '  %-24s current=%-5s desired=%s\n' \
    "${setting_names[index]}" "${current_values[index]}" "${desired_values[index]}"
  if [[ "${current_values[index]}" != "${desired_values[index]}" ]]; then
    drift="true"
  fi
done

if [[ "${drift}" == "false" ]]; then
  echo
  echo "Repository merge settings already match the desired state."
elif [[ "${mode}" == "dry-run" ]]; then
  echo
  echo "Dry-run only: repository settings were not changed. Re-run with --apply after approval."
else
  echo
  echo "Applying repository merge settings..."
  gh api --method PATCH "repos/${repository}" \
    -F allow_auto_merge=true \
    -F allow_update_branch=true \
    -F allow_squash_merge=true \
    -F allow_merge_commit=false \
    -F allow_rebase_merge=false \
    -F delete_branch_on_merge=true \
    --silent
  echo "Repository merge settings applied."
fi

cat <<'EOF'

Ruleset recommendation (output only; this script does not apply it):
  1. Wait until the first successful `CI / Required` check is registered.
  2. Obtain explicit maintainer approval before changing live protection.
  3. In Settings > Rules > Rulesets, create an active branch ruleset for `main`:
     - require a pull request before merging;
     - required approvals: 0 initially;
     - require conversation resolution;
     - require status check: CI / Required;
     - require branches to be up to date before merging;
     - require linear history;
     - block force pushes and branch deletion;
     - do not require Code Owner review initially;
     - do not require signed commits initially;
     - retain an emergency administrator bypass.

No ruleset or branch-protection API request was made.
EOF
