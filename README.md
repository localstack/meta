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

## pr-enforce-no-breaking-changes
```yaml
name: Enforce no breaking changes

on:
  pull_request_target:
    types: [labeled, unlabeled, opened]
    # only enforce for PRs targeting the main branch
    branches:
    - main

jobs:
  enforce-no-breaking-changes:
    permissions:
      issues: write
      pull-requests: write
    uses: localstack/meta/.github/workflows/pr-enforce-no-breaking-changes.yml@main
    secrets:
      github-token: ${{ secrets.REPO_ACCESS_PAT }}
```

## pr-enforce-patch-only
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
    uses: localstack/meta/.github/workflows/pr-enforce-patch-only.yml@main
    secrets:
      github-token: ${{ secrets.REPO_ACCESS_PAT }}
```

## pr-enforce-label-groups
```yaml
name: Enforce Labels

on:
  pull_request_target:
    types: [labeled, unlabeled, opened]

jobs:
  labels:
    uses: localstack/meta/.github/workflows/pr-enforce-label-groups.yml@main
    secrets:
      github-token: ${{ secrets.REPO_ACCESS_PAT }}
