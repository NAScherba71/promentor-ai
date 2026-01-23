# Repository Maintenance Workflows

This document describes the automated workflows for maintaining repository health.

## Repo Health Check

**File:** `.github/workflows/repo-health.yml`

This workflow runs daily to check for repository health issues:

- **Schedule:** Daily at 00:00 UTC
- **Manual Trigger:** Available via workflow_dispatch

### What it checks:

1. **Branch count**: Detects if there are additional branches beyond the main branch
2. **Issue creation**: Automatically creates an issue if problems are detected

## Cleanup Merged Branches

**File:** `.github/workflows/cleanup-merged-branches.yml`

This workflow automatically deletes branches after PRs are merged:

- **Auto-trigger:** Runs when a PR is merged
- **Manual Trigger:** Can be run manually to delete a specific branch

### How it works:

1. Triggers when a PR is closed and merged
2. Deletes the PR's head branch automatically
3. Skips protected branches (main, master)

## Cleanup Stale Branches

**File:** `.github/workflows/cleanup-stale-branches.yml`

This workflow provides a one-time cleanup of all merged branches:

- **Manual Trigger Only:** Must be run manually via Actions tab

### How to use:

1. Go to **Actions** tab in GitHub
2. Select **"Cleanup Stale Branches"** workflow
3. Click **"Run workflow"** button
4. Confirms deletion by checking merged PRs
5. Automatically closes repo health issues if all stale branches are removed

### What it does:

1. Lists all branches in the repository
2. Identifies branches that have been merged via PRs
3. Deletes non-protected branches that have been merged
4. Closes the repo health issue if cleanup is complete

## Best Practices

1. **Enable automatic branch deletion:** While these workflows help, consider enabling "Automatically delete head branches" in repository settings under Pull Requests
2. **Run cleanup regularly:** If you notice stale branches, run the "Cleanup Stale Branches" workflow
3. **Monitor repo health:** The daily health check will alert you to issues automatically

## Protected Branches

The following branches are protected and will never be deleted:
- main
- master
- develop
- development
