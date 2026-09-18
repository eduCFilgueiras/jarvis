#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-eduCFilgueiras/jarvis}"

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI is required. Install and authenticate with: gh auth login" >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "gh is not authenticated. Run: gh auth login" >&2
  exit 1
fi

create_label() {
  local name="$1"
  local color="$2"
  local description="$3"

  if gh label list --repo "$REPO" --search "$name" --json name --jq '.[].name' | grep -Fxq "$name"; then
    gh label edit "$name" --repo "$REPO" --color "$color" --description "$description"
  else
    gh label create "$name" --repo "$REPO" --color "$color" --description "$description"
  fi
}

create_issue() {
  local title="$1"
  local labels="$2"
  local body="$3"

  if gh issue list --repo "$REPO" --state all --search "$title in:title" --json title --jq '.[].title' | grep -Fxq "$title"; then
    echo "Issue already exists: $title"
  else
    gh issue create --repo "$REPO" --title "$title" --label "$labels" --body "$body"
  fi
}

create_label "type: feature" "1D76DB" "New capability or enhancement"
create_label "type: bug" "D73A4A" "Bug or regression"
create_label "type: task" "C5DEF5" "Implementation or maintenance task"
create_label "area: agents" "5319E7" "Agents and agent registry"
create_label "area: tools" "0E8A16" "Local tools"
create_label "area: models" "FBCA04" "Model providers and routing"
create_label "area: memory" "BFDADC" "History, persistence, and memory"
create_label "area: security" "D93F0B" "Permissions and safety"
create_label "area: infra" "6F42C1" "Project automation and infrastructure"
create_label "env: hml" "F9D0C4" "Homologation environment"
create_label "env: prd" "B60205" "Production environment"
create_label "priority: high" "B60205" "High priority"
create_label "priority: medium" "FBCA04" "Medium priority"
create_label "priority: low" "C2E0C6" "Low priority"

create_issue "[Task] Configure GitHub project board" "type: task,area: infra,priority: medium" "Create a GitHub Project board with columns: Backlog, Ready, In Progress, Review, Done."
create_issue "[Feature] Add real OpenAI activation flow" "type: feature,area: models,priority: high" "Wire the optional OpenAI provider into documented setup and validate with OPENAI_API_KEY."
create_issue "[Feature] Add permission prompts for sensitive tools" "type: feature,area: security,priority: high" "Ask for explicit confirmation before running sensitive tools or future write operations."
create_issue "[Feature] Add write-capable files tool behind confirmation" "type: feature,area: tools,area: security,priority: medium" "Add safe file write operations protected by PermissionPolicy and CLI confirmation."
create_issue "[Feature] Add voice input and output" "type: feature,priority: low" "Plan and implement microphone input and spoken responses."

echo "GitHub bootstrap complete for $REPO"
