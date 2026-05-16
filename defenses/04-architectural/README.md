# Defense 04 — Architectural Patterns for Review Agents

These are configuration choices and design patterns; they don't ship as code in
this repo. The checklist below is what to verify on whatever review-agent setup
you're running (GitHub Actions, GitLab, your own runner).

## 1. Read-only review

The review agent comments. It does not approve, dismiss, or merge.

```yaml
# .github/branch-protection.yml (or equivalent)
required_approving_review_count: 1
require_human_reviews: true              # the AI's review does not count toward this
restrict_review_dismissals: true
review_dismissal_actors:
  - human-only-team
```

In GitHub specifically: the AI agent posts comments via the issues API, **not**
review approvals. If the agent has a GitHub App identity, scope its token so it
cannot submit reviews or dismiss them. The agent is advisory; humans decide.

## 2. Limited tool access

If the review agent runs in an agent runtime with tool access:

```yaml
# Review-agent runtime profile (pseudo-config)
allowed_tools:
  - read_file
  - run_static_analysis
  - search_code
denied_tools:
  - write_file
  - merge_pr
  - dismiss_review
  - run_arbitrary_shell
```

The agent cannot push to branches, modify other reviews, or run shell. It
reads, analyzes, and reports.

## 3. Independent security context

The review agent's system prompt and security rules come from a **separate
repository** that the PR cannot modify:

```
infra/                       <- the repo being reviewed (attacker can PR here)
ai-review-agent-config/      <- separate repo, CODEOWNERS = @org/security-team
  └─ system-prompts/security-reviewer.md
  └─ rules/owasp-checks.md
```

The CI workflow that invokes the review agent pulls system-prompts/ from the
config repo by SHA (not by ref) so a downstream attacker cannot redirect it.

## 4. Immutable rules source

If you must keep security rules in the same repo, put them in a directory
under tight CODEOWNERS and require **two-person review** for changes — same
posture as production secrets management.

```
# .github/CODEOWNERS
ai-review/rules/   @org/security-team @org/platform-team
```

GitHub's "require approvals from CODEOWNERS" + "require two reviewers" makes a
single compromised account insufficient.

## Why this lives as a checklist and not code

These choices are organization-specific. The code you'd write to enforce them
is your own CI workflows + your branch-protection settings + your agent
runtime's config. The pattern is the contribution; the implementation depends
on your stack.
