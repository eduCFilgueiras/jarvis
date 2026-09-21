# GitHub Workflow

This project uses GitHub for source control and can use Issues as a lightweight Kanban.

## Branch Flow

1. Create or update an issue with goal, scope, and acceptance criteria.
2. Create a feature branch from `main`, including the issue number when useful.
3. Commit focused changes.
4. Push the branch and open a pull request with `Closes #N`.
5. Run tests and review the diff.
6. Merge after checks pass; GitHub closes the linked issue automatically.

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

## Continuous Tracking

Issues are the source of truth for planned work. Each implementation branch
must link to one or more issues, and each pull request must declare its closing
issue. Use comments on the issue for progress, blockers, and validation notes.
