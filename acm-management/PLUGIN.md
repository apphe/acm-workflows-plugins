# ACM Management Plugin

Tools for ACM (Advanced Cluster Management) support, analysis, and management workflows.

## Skills

### acm-support-analyzer
Analyze ACM support exception requests against test data from Google Docs.

**Usage:**
```
/acm-management:acm-support-analyzer "ACM 2.15 upgrade from RKE2"
```

**Features:**
- Downloads ACM test data from Google Docs
- Analyzes platform compatibility (OCP vs Non-OCP)
- Compares versions against tested configurations
- Returns structured analysis with recommendations

**Output Format:**
- Requested: ACM version | Hub platform | Spoke platform
- Status: TESTED | PARTIALLY TESTED | NOT TESTED
- Details: Findings with Jira links
- Recommendation: APPROVE | NEEDS REVIEW

### weekly-jira-status
Generate weekly Jira status reports for Server Foundation and Maestro teams.

**Usage:**
```
/acm-management:weekly-jira-status        # last 7 days (default)
/acm-management:weekly-jira-status 14     # last 14 days
/acm-management:weekly-jira-status 30     # last 30 days
```

**Features:**
- Queries bugs (SFDC Cases > 0, Critical/Blocker), stories, and vulnerabilities
- Groups stories by parent Epic with child progress statistics
- Groups vulnerabilities by CVE with issue count
- Organizes output by Activity Type

## Requirements

- Google credentials configured for gdoc-downloader
- Access to ACM test data document

## Author

apphe
