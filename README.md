# ACM Workflows Plugins

Claude Code plugins for ACM (Advanced Cluster Management) workflows and automation.

## Plugins

### acm-management
Tools for ACM support, analysis, and management workflows.

**Skills:**
- `acm-support-analyzer` - Analyze ACM support exception requests against test data

## Installation

```bash
# Install from GitHub
claude plugins install https://github.com/apphe/acm-workflows-plugins/acm-management

# Or install locally for development
claude plugins install ~/projects/acm-workflows-plugins/acm-management
```

## Development

```bash
# Clone repository
git clone https://github.com/apphe/acm-workflows-plugins.git
cd acm-workflows-plugins

# Make changes to skills
cd acm-management/skills/your-skill/

# Test locally
claude plugins install ~/projects/acm-workflows-plugins/acm-management

# Commit and push
git add .
git commit -m "Add new skill"
git push
```

## License

MIT
