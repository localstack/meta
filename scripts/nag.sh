#!/usr/bin/env bash

set -euo pipefail

function merge_near() {
    milestone="$1"
jq -r -n \
--argjson localstack "$(gh pr list --search "milestone:${milestone}" --json number,author,milestone,isCrossRepository,url --repo localstack/localstack --limit 500)" \
--argjson localstack_ext "$(gh pr list --search "milestone:${milestone}" --json number,author,milestone,isCrossRepository,url --repo localstack/localstack-ext --limit 500)" \
"[\$localstack + \$localstack_ext | .[] | select (.isCrossRepository | not)] | group_by(.author.login) | map({ author: (if .[0].author.name != \"\" then .[0].author.name else .[0].author.login end), prs: [.[] | .url] }) | .[] | \">>>>>> \(.author)\nHey! I can see you have these PRs:\n\(.prs | join(\"\n\"))\nleft open for v${milestone}. Please get back to me with their state as soon as possible, so I can track it for the release.\nThanks!\n\""
}

function no_milestone() {
     jq -r -n \
--argjson localstack "$(gh pr list --search "no:milestone" --json number,author,milestone,isCrossRepository,url --repo localstack/localstack --limit 500)" \
--argjson localstack_ext "$(gh pr list --search "no:milestone" --json number,author,milestone,isCrossRepository,url --repo localstack/localstack-ext --limit 500)" \
"[\$localstack + \$localstack_ext | .[] | select (.isCrossRepository | not)] | group_by(.author.login) | map({ author: (if .[0].author.name != \"\" then .[0].author.name else .[0].author.login end), prs: [.[] | .url] }) | .[] | \">>>>>> \(.author)\nHey! I can see you have these PRs open:\n\(.prs | join(\"\n\"))\nwithout a milestone. Please add a milestone for it (either a specific version, or Playground) as soon as possible, so I can track it for the release.\nFor more information regarding the milestones, please take a look at the notion page (https://www.notion.so/localstack/v3-1-0-91633b885871426bb1e9c4ee4ed7928d) or reach out directly to me. I'm happy to help! 🙂\nThanks!🚀\n\""
}

function main() {
    if [[ -z "${1-}" ]]; then
        echo "Usage: $0 <command> [<milestone>]" >&2
        exit 1
    fi

    case "$1" in
        no-milestone)
            no_milestone
            ;;
        merge-near)
            if [[ -z "${2-}" ]]; then
                echo "Usage: $0 <command> [<milestone>]" >&2
                exit 1
            fi
            merge_near "$2"
            ;;
        *)
            echo "invalid command" >&2
            exit 1
            ;;
    esac
}

main "$@"
