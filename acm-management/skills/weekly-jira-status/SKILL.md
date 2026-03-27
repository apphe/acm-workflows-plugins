---
name: acm-management:weekly-jira-status
description: Generate a weekly Jira status report for Server Foundation and Maestro teams. Queries bugs (customer-reported Critical/Blocker), stories, and vulnerabilities that moved to Review or Resolved. Use when the user asks for team status, weekly updates, Jira summary, or wants to know what changed this week for Server Foundation or Maestro.
---

# Weekly Jira Status Report

Generate a categorized status report by querying Jira for recent issue activity across Server Foundation and Maestro components.

## Arguments

- `$ARGUMENTS`: Optional duration in days (default: 7). Example: `/acm-management:weekly-jira-status 14` for last 14 days.

## Workflow

Parse the duration from arguments. If no argument provided, default to 7 days.

### Step 1: Query Jira

Run a single JQL query:

```
project = ACM
AND component in ('Server Foundation', 'Maestro')
AND (
  (type = Bug AND cf[10978] > 0 AND priority in (Critical, Blocker))
  OR type = Story
  OR type = Vulnerability
)
AND (status changed to Review AFTER -{DAYS}d OR status changed to Resolved AFTER -{DAYS}d)
```

Replace `{DAYS}` with the duration parameter. `cf[10978]` is the SFDC Cases Counter field.

### Step 2: Enrich each issue

For each returned issue, fetch additional fields via `jira issue view <KEY> --raw`:

- **Bugs**: Get severity (`customfield_10840`), SFDC Cases Counter (`customfield_10978`). Read description and comments for brief summary.
- **Stories**: Get parent Epic from `customfield_12311140` or `customfield_10014`. For each unique Epic, fetch its summary/description and query child story counts by status:
  ```
  jira issue list -q "project = ACM AND 'Epic Link' = <EPIC-KEY>"
  ```
  Count children by status (Closed, Review, In Progress, New, other).
- **Vulnerabilities**: Extract CVE ID from summary (pattern: `CVE-XXXX-XXXXX`). Group by CVE.

### Step 3: Format output

Organize issues by Activity Type field (`customfield_10464`). If Activity Type is not set, infer from context:
- Bugs with SFDC → "Incidents & Support"
- Vulnerabilities → "Security & Compliance"
- Stories → use their Activity Type, or "Product / Portfolio Work" as default

#### Output Template

```markdown
### Incidents & Support

- **[ACM-XXXXX](https://issues.redhat.com/browse/ACM-XXXXX) (Priority, Status, SFDC: N)** — Brief of what the bug is about, impact/root cause/fix, and current progress

### Security & Compliance

- **CVE-XXXX-XXXXX** (N issues) — Brief description of the CVE

### Product / Portfolio Work

- **[ACM-XXXXX](https://issues.redhat.com/browse/ACM-XXXXX) (N total: X Closed, X Review, X In Progress, X New)** — Epic feature description (from epic description)
  - [ACM-YYYYY](https://issues.redhat.com/browse/ACM-YYYYY) (Status) — What was done
```

If no results for a category, output:

```
- None
```

## Important Notes

- The severity field is `customfield_10840` (values like Critical, Important, Moderate, Low)
- The SFDC Cases Counter field is `cf[10978]` in JQL, `customfield_10978` in REST API
- The Activity Type field is `customfield_10464`
- The Epic Link field is `customfield_12311140` (fallback: `customfield_10014`)
- For Stories without a parent Epic, list them under "Other" at the end
- Keep bug briefs concise: one sentence for what, one for impact/fix, one for progress
- For Epic child progress, only show statuses with count > 0
