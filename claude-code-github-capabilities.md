# Claude Code — GitHub MCP Capabilities

This document describes all available and unavailable GitHub operations accessible through the GitHub MCP connection in Claude Code.

---

## Repository Management

| Action | Available |
|--------|-----------|
| Create a new repository | ✅ |
| Fork a repository | ✅ |
| Get authenticated user profile | ✅ |

---

## File Operations

| Action | Available |
|--------|-----------|
| Read a file or directory | ✅ |
| Create or update a single file | ✅ |
| Delete a file | ✅ |
| Push multiple files at once | ✅ |

---

## Branch Management

| Action | Available |
|--------|-----------|
| List branches | ✅ |
| Create a branch | ✅ |

---

## Commits & Tags

| Action | Available |
|--------|-----------|
| Get a specific commit | ✅ |
| List commits | ✅ |
| List tags | ✅ |
| Get a specific tag | ✅ |

---

## Issues

| Action | Available |
|--------|-----------|
| Read issues / get issue details | ✅ |
| List all issues | ✅ |
| Create, update, or close issues | ✅ |
| Add a comment to an issue | ✅ |
| List issue types | ✅ |
| Search issues | ✅ |
| Write sub-issues | ✅ |

---

## Pull Requests

| Action | Available |
|--------|-----------|
| List pull requests | ✅ |
| Read PR details | ✅ |
| Create a pull request | ✅ |
| Update a pull request | ✅ |
| Merge a pull request | ✅ |
| Update a PR branch | ✅ |
| Add a review / comment to a PR | ✅ |
| Add a comment to a pending review | ✅ |
| Reply to a PR comment | ✅ |
| Search pull requests | ✅ |
| Request Copilot review | ✅ |

---

## Releases

| Action | Available |
|--------|-----------|
| List releases | ✅ |
| Get the latest release | ✅ |
| Get a release by tag | ✅ |

---

## Search

| Action | Available |
|--------|-----------|
| Search code across repositories | ✅ |
| Search repositories | ✅ |
| Search users | ✅ |

---

## Teams & Collaborators

| Action | Available |
|--------|-----------|
| List repository collaborators | ✅ |
| Get teams in an organization | ✅ |
| Get team members | ✅ |

---

## Labels & Security

| Action | Available |
|--------|-----------|
| Get a label | ✅ |
| Run secret scanning | ✅ |

---

## Not Available

The following GitHub features are **not accessible** through this MCP connection:

| Feature | Notes |
|---------|-------|
| **GitHub Actions workflows** | Cannot trigger, list, cancel, or inspect workflow runs or jobs |
| **Webhooks** | Cannot create, list, update, or delete repository or org webhooks |
| **Repository settings** | No access to branch protection rules, deploy keys, secrets, or general settings pages |
| **GitHub Pages** | Cannot configure or manage Pages deployments |
| **Dependabot** | No access to Dependabot alerts or security updates |
| **Repository insights / traffic** | No access to views, clones, or contributor stats |

---

## Summary

Claude Code via GitHub MCP provides broad read/write access for day-to-day development operations: managing files, branches, commits, issues, and pull requests. It does not cover CI/CD pipeline management, repository administration, or webhook configuration.

*Generated on 2026-05-25 using Claude Code connected via GitHub MCP.*
