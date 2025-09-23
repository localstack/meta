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
        categories: status,aws,semver,docs,notes
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

## pr-enforce-no-major
```yaml
name: Enforce no major on main

on:
  pull_request_target:
    types: [labeled, unlabeled, opened]
    # only enforce for PRs targeting the main branch
    branches:
    - main

jobs:
  enforce-no-major:
    permissions:
      issues: write
      pull-requests: write
    uses: localstack/meta/.github/workflows/pr-enforce-no-major.yml@main
    secrets:
      github-token: ${{ secrets.REPO_ACCESS_PAT }}
```

## pr-enforce-no-major-minor
```yaml
name: Enforce no major or minor on main

on:
  pull_request_target:
    types: [labeled, unlabeled, opened]
    # only enforce for PRs targeting the main branch
    branches:
    - main

jobs:
  enforce-no-major-minor:
    permissions:
      issues: write
      pull-requests: write
    uses: localstack/meta/.github/workflows/pr-enforce-no-major-minor.yml@main
    secrets:
      github-token: ${{ secrets.REPO_ACCESS_PAT }}
```

## pr-enforce-semver-labels
```yaml
name: Enforce SemVer Labels
on:
  pull_request_target:
    types: [labeled, unlabeled, opened]

jobs:
  enforce-semver-labels:
    uses: localstack/meta/.github/workflows/pr-enforce-semver-labels.yml@main
    secrets:
      github-token: ${{ secrets.REPO_ACCESS_PAT }}
```

## pr-enforce-docs-labels
```yaml
name: Enforce Docs Labels

on:
  pull_request_target:
    types: [labeled, unlabeled, opened]

jobs:
  enforce-docs-labels:
    uses: localstack/meta/.github/workflows/pr-enforce-docs-labels.yml@main
    secrets:
      github-token: ${{ secrets.REPO_ACCESS_PAT }}
```

## upgrade-python-dependencies

This reusable workflow adds an automated upgrade of dependencies in python repositories.
As a prerequisite the repository must define the make target `upgrade-pinned-dependencies` which should produce some kind of lock file checked in into the repository.

```yaml
name: Upgrade Pinned Python Dependencies

on:
  schedule:
    - cron: 0 5 * * TUE
  workflow_dispatch:

jobs:
  upgrade-dependencies:
    uses: localstack/meta/.github/workflows/upgrade-python-dependencies.yml@main
    secrets:
      github-token: ${{ secrets.PRO_ACCESS_TOKEN }}
    with:
      labels: "area: dependencies, semver: patch, docs: skip, notes: skip"
```
