---
name: gdoc-export
description: Export Google Docs, Sheets, and Slides to various formats (markdown, txt, csv, pdf, docx, xlsx) using authenticated Google API access. Use this skill whenever the user provides a Google Drive URL (docs.google.com/document, docs.google.com/spreadsheets, docs.google.com/presentation) and wants to read, analyze, or process its content. Also use when a task requires fetching data from Google Drive documents, even if the user doesn't explicitly say "export" — any reference to a Google Doc/Sheet/Slides URL should trigger this skill.
---

# Google Drive Document Exporter

Export content from Google Docs, Sheets, and Slides via the Google Drive API with OAuth authentication.

## Usage

```
/acm-management:gdoc-export <URL> [--format <format>]
```

## Arguments

- `URL` (required): A Google Docs, Sheets, or Slides URL
- `--format` (optional): Output format. Defaults vary by document type.

### Supported Formats

| Document Type | Formats | Default |
|---|---|---|
| Google Docs | markdown, txt, pdf, docx | markdown |
| Google Sheets | csv, xlsx, pdf | csv |
| Google Slides | txt, pdf | txt |

**Note:** Google Slides does not support HTML/markdown export. Use `txt` for text content or `pdf` for visual layout.

## Workflow

### Step 1: Run the export script

```bash
cd /tmp && python3 <skill-directory>/scripts/export.py "<URL>" --format <format>
```

The script outputs document content to stdout and saves a copy to the working directory.

### Step 2: Use the content

- For text formats (markdown, txt, csv): the content is printed to stdout and can be used directly
- For binary formats (pdf, docx, xlsx): a file is saved to `/tmp/document_<id>.<ext>`

## First-Time Setup

If the script fails with "Run: python3 export.py --setup", the user needs to authenticate:

1. Ensure Google OAuth credentials exist at `~/.config/google-credentials.json` or `~/.google/google-credentials.json`
2. Run setup interactively (the user must do this themselves as it opens a browser):
   ```
   ! python3 <skill-directory>/scripts/export.py --setup
   ```
3. Tokens are saved to `~/.config/google-tokens.json` and auto-refresh on subsequent uses

## Dependencies

Required Python packages: `google-auth`, `google-auth-oauthlib`, `google-api-python-client`, `markdownify`

Install if missing:
```bash
pip install google-auth google-auth-oauthlib google-api-python-client markdownify
```

## Examples

Export a Google Doc as markdown:
```
/acm-management:gdoc-export https://docs.google.com/document/d/1abc.../edit
```

Export a spreadsheet as CSV:
```
/acm-management:gdoc-export https://docs.google.com/spreadsheets/d/1xyz.../edit --format csv
```

Export slides as text:
```
/acm-management:gdoc-export https://docs.google.com/presentation/d/1def.../edit
```
