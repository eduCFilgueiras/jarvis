# GitHub Workflow

This project uses GitHub for source control and can use Issues as a lightweight Kanban.

## Branch Flow

1. Create a feature branch from `main`.
2. Commit focused changes.
3. Push the branch.
4. Open a pull request.
5. Merge after tests pass.

Example:

```bash
git checkout main
git pull
git checkout -b feature/my-feature
python3 -m unittest discover
git push -u origin feature/my-feature
```

## Automation Bootstrap

After authenticating the GitHub CLI:

```bash
gh auth login
scripts/bootstrap_github.sh eduCFilgueiras/jarvis
```

The script creates or updates:

- labels
- starter issues

## Suggested Kanban Columns

- Backlog
- Ready
- In Progress
- Review
- Done

## Recommended Labels

- `type: feature`
- `type: bug`
- `type: task`
- `area: agents`
- `area: tools`
- `area: models`
- `area: memory`
- `area: security`
- `area: infra`
- `env: hml`
- `env: prd`
- `priority: high`
- `priority: medium`
- `priority: low`
