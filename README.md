# LocalStack Meta Repository

This repo aims at unifying certain processes and tools across our repositories.

## sync-labels
This reusable workflow ensures that a set of labels are present in the repository.
The workflow can be used like this:
```yaml
name: Sync Labels

on:
  schedule:
  - cron: "0 0 * * *"
  workflow_dispatch:

jobs:
  sync-with-project:
    uses: localstack/meta/.github/workflows/sync-labels.yml@main
    with:
        categories: status,aws,semver
    secrets:
      github-token: ${{ secrets.REPO_ACCESS_PAT }}
```

- You can define the set of categories of labels which should be synced.
  - By default the `labels-status` are synced.
  - These labels are necessary for the `add-to-project`` workflow (see below).

- Make sure to use a PAT which has write access to the project.
  - f.e. the `localstack-bot` PAT we use in most of the repos
  - Don't forget to add it as a collaborator with write permissions in your repo!

## add-to-project
This reusable workflow performs two actions:
- It adds every newly created issue to a specified project (by default it uses https://github.com/orgs/localstack/projects/17).
- It sets the column in the project depending on the `status: ...` label on the issue.
  - If no or multiple status labels are set, it moves it to the "triage needed" column!

The workflow can be used like this:
```yaml
name: Sync Project Cards

on:
  issues:
    types:
    - labeled
    - unlabeled
    - opened

jobs:
  sync-with-project:
    uses: localstack/meta/.github/workflows/add-to-project.yml@main
    secrets:
      github-token: ${{ secrets.REPO_ACCESS_PAT }}
```

## stale-bot
This reusable workflow defines the default usage of our stale bot in public repos of LocalStack.

The workflow can be used like this:
```yaml
name: Triage Stale Issues

on:
  schedule:
  - cron: "0 * * * *"
  workflow_dispatch:

jobs:
  sync-with-project:
    uses: localstack/meta/.github/workflows/stale-bot.yml@main
    secrets:
      github-token: ${{ secrets.REPO_ACCESS_PAT }}
```