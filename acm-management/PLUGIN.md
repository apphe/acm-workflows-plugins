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

## Requirements

- Google credentials configured for gdoc-downloader
- Access to ACM test data document

## Author

apphe
