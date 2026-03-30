# ACM Support Exception Analyzer

Analyze ACM support exception requests against tested configurations from Google Docs.

## Trigger Condition

Use this skill when the user asks to:
- Analyze ACM support exception requests
- Check if ACM configurations are tested
- Validate ACM platform/version combinations against test data
- Review support requests for approval

## Parameters

- `request` (required): The support exception request description
  - Example: "ACM 2.15 upgrade from RKE2 to OCP 4.16"
  - Can include: ACM version, platform types, upgrade scenarios

- `--issue-title` (optional): Jira issue title for context
- `--product-version` (optional): Product version being requested

## Instructions

When this skill is invoked:

### Step 1: Download Test Data

Use the gdoc-export skill (sibling skill in this plugin) to fetch the latest ACM test data:

```bash
cd /tmp && python3 <skill-base-directory>/../gdoc-export/scripts/export.py "https://docs.google.com/document/d/1TW_Mki_ye7d7vcII2al35BvdSiYmJl2yoK_qFlSs5QE/edit?tab=t.0" --format markdown
```

This document contains the tested ACM configurations.

### Step 2: Extract Request Details

From the user's request, identify:

1. **Platform Type:**
   - Non-OCP: RKE2, Sylva, K8s, EKS, AKS, GKE, etc.
   - OCP: OpenShift

2. **Versions:**
   - ACM/MCE version
   - Hub platform version
   - Spoke platform version
   - **Important:** If both current AND target versions mentioned (e.g., "using 2.11 upgrading to 2.15"), USE THE TARGET VERSION for analysis

3. **Version Priority Rules:**
   - Look for keywords: "upgrade to", "plan to", "moving to", "target version", "upgrading to"
   - Target/planned version takes precedence over current version
   - Example: "using ACM 2.11 upgrading to 2.15" → analyze 2.15

### Step 3: Match Against Test Data

Compare the extracted configuration against the test data:

1. **Non-OCP Platforms:**
   - Test data only covers OCP configurations
   - Non-OCP → Status: NOT TESTED
   - Recommendation: NEEDS REVIEW

2. **OCP Platforms:**
   - Exact match → Status: TESTED, Recommendation: APPROVE
   - Similar configuration → Status: PARTIALLY TESTED, Recommendation: NEEDS REVIEW
   - No match → Status: NOT TESTED, Recommendation: NEEDS REVIEW

3. **Look for Jira tickets** in test data that match the configuration

### Step 4: Format Output

Return EXACTLY 4 lines in this format:

```
Requested: [ACM ver] | [Hub platform] | [Spoke platform]
Status: [TESTED|PARTIALLY TESTED|NOT TESTED]
Details: [findings + Jira link if available]
Recommendation: [APPROVE|NEEDS REVIEW - reason]
```

**Formatting Rules:**
- Omit hub platform from output if not mentioned in request
- Format Jira tickets as: `[ACM-XXXXX](https://issues.redhat.com/browse/ACM-XXXXX)`
- Keep each line concise and structured
- No additional commentary outside the 4 lines

## Example Usage

### Example 1: Simple Request
**Input:** `/acm-management:acm-support-analyzer "ACM 2.15 on OCP 4.16"`

**Output:**
```
Requested: ACM 2.15 | OCP 4.16 hub | OCP 4.16 spokes
Status: TESTED
Details: Exact match found in regression testing - [ACM-12345](https://issues.redhat.com/browse/ACM-12345)
Recommendation: APPROVE
```

### Example 2: Upgrade Scenario
**Input:** `/acm-management:acm-support-analyzer "Customer using ACM 2.11 on OCP 4.14, upgrading to ACM 2.15 on OCP 4.16"`

**Output:**
```
Requested: ACM 2.15 | OCP 4.16 hub | OCP 4.16 spokes
Status: TESTED
Details: Target version 2.15 on OCP 4.16 tested - [ACM-12345](https://issues.redhat.com/browse/ACM-12345)
Recommendation: APPROVE
```

### Example 3: Non-OCP Platform
**Input:** `/acm-management:acm-support-analyzer "ACM 2.15 on RKE2 cluster"`

**Output:**
```
Requested: ACM 2.15 | RKE2 hub | RKE2 spokes
Status: NOT TESTED
Details: RKE2 platform not covered in OCP-only regression testing
Recommendation: NEEDS REVIEW - Non-OCP platform requires additional validation
```

## Error Handling

- If gdoc-export fails: Inform user and suggest checking Google credentials
- If test data is empty: Report error and suggest checking document access
- If request is unclear: Ask user to clarify the ACM version and platform details

## Notes

- This skill depends on the gdoc-export skill (sibling skill in acm-management plugin)
- Test data document URL is hardcoded but can be updated if needed
- Always prioritize target/planned versions over current versions in upgrade scenarios
