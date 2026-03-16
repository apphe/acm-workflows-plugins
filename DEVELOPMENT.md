# Development Guide

## Plugin Structure

```
acm-workflows-plugins/
├── README.md                          # Repository overview
├── .gitignore                         # Git ignore patterns
├── DEVELOPMENT.md                     # This file
└── acm-management/                    # Plugin directory
    ├── .claude-plugin/
    │   └── plugin.json                # Plugin metadata
    ├── PLUGIN.md                      # Plugin documentation
    └── skills/
        └── acm-support-analyzer/      # Skill directory
            ├── SKILL.md               # Skill instructions (main logic)
            └── scripts/               # Helper scripts (optional)
                └── analyze.sh
```

## How Skills Work

### SKILL.md
This is the **core file** that Claude reads to execute the skill. It contains:
- **Trigger Condition**: When to use this skill
- **Parameters**: What inputs the skill accepts
- **Instructions**: Step-by-step logic for Claude to follow
- **Examples**: Usage examples
- **Error Handling**: How to handle failures

**Important:** Claude reads and executes the instructions in SKILL.md. Write clear, detailed steps.

### Scripts Directory (Optional)
- Helper scripts for complex operations
- Standalone utilities
- Can be called from SKILL.md if needed

## Creating a New Skill

### 1. Create Skill Directory

```bash
cd ~/projects/acm-workflows-plugins/acm-management/skills/
mkdir -p my-new-skill/scripts
```

### 2. Create SKILL.md

```bash
cat > my-new-skill/SKILL.md << 'EOF'
# My New Skill

Brief description of what this skill does.

## Trigger Condition

Use this skill when...

## Parameters

- `param1` (required): Description
- `--flag` (optional): Description

## Instructions

Step-by-step instructions for Claude to execute...

## Example Usage

Example commands and outputs...
EOF
```

### 3. Update plugin.json

```bash
# Edit acm-management/.claude-plugin/plugin.json
# Add your skill name to the "skills" array:
{
  "skills": [
    "acm-support-analyzer",
    "my-new-skill"
  ]
}
```

### 4. Test Locally

```bash
# Install plugin locally
claude plugins install ~/projects/acm-workflows-plugins/acm-management

# Test the skill
/acm-management:my-new-skill "test input"
```

### 5. Commit and Push

```bash
cd ~/projects/acm-workflows-plugins
git add .
git commit -m "Add my-new-skill"
git push
```

## Development Workflow

### Initial Setup

```bash
# Clone your repo (already done)
git clone https://github.com/apphe/acm-workflows-plugins.git ~/projects/acm-workflows-plugins

# Install for development
claude plugins install ~/projects/acm-workflows-plugins/acm-management
```

### Making Changes

```bash
# 1. Edit skill files
cd ~/projects/acm-workflows-plugins/acm-management/skills/acm-support-analyzer/
# Make your changes to SKILL.md or scripts

# 2. Reinstall to test
claude plugins update acm-management

# 3. Test the skill
/acm-management:acm-support-analyzer "test request"

# 4. Commit when satisfied
cd ~/projects/acm-workflows-plugins
git add .
git commit -m "Update acm-support-analyzer skill"
git push
```

### Publishing Updates

Once you push to GitHub, users can update via:

```bash
claude plugins update acm-management
```

## Best Practices

### SKILL.md Writing Tips

1. **Be Specific**: Write clear, actionable steps
2. **Handle Errors**: Include error handling instructions
3. **Provide Examples**: Show multiple usage scenarios
4. **Use Tools**: Leverage other skills (e.g., gdoc-downloader)
5. **Structure Output**: Define exact output format

### Skill Design

1. **Single Purpose**: Each skill should do one thing well
2. **Composable**: Skills can call other skills
3. **Clear Triggers**: Define when to use the skill
4. **Well Documented**: Include usage examples

### Testing

1. **Test Locally First**: Use local install before pushing
2. **Try Edge Cases**: Test error conditions
3. **Verify Output**: Check output format matches spec
4. **Test Dependencies**: Ensure required tools/skills are available

## Converting Shell Scripts to Skills

When converting existing shell scripts (like automated-gdoc-analysis.sh):

1. **Extract Logic**: Understand what the script does
2. **Identify Steps**: Break down into clear steps
3. **Write Instructions**: Convert steps to SKILL.md instructions
4. **Handle I/O**: Define input parameters and output format
5. **Error Cases**: Add error handling
6. **Test**: Verify behavior matches original script

## Troubleshooting

### Skill Not Found
```bash
# Reinstall plugin
claude plugins install ~/projects/acm-workflows-plugins/acm-management --force
```

### Skill Not Working
- Check SKILL.md syntax
- Verify plugin.json includes skill name
- Check Claude logs for errors

### Changes Not Reflected
```bash
# Force update
claude plugins update acm-management --force
```

## Resources

- [Claude Code Plugin Documentation](https://docs.anthropic.com/claude/docs/plugins)
- Your installed plugins: `~/.claude/plugins/cache/`
- Example skills: `~/.claude/plugins/cache/acm-workflows-plugins/jira-tools/`
