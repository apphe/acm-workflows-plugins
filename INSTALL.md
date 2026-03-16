# Installation Guide

## For Local Development (You)

1. **Make changes to your plugin:**
   ```bash
   cd ~/projects/acm-workflows-plugins/acm-management
   # Edit SKILL.md or add new skills
   ```

2. **Sync to Claude:**
   ```bash
   ~/projects/acm-workflows-plugins/sync-local.sh
   ```

3. **Reload Claude** (restart the CLI or reload the session)

4. **Test your skill:**
   ```
   /acm-management:acm-support-analyzer "ACM 2.15 on OCP 4.16"
   ```

## For Others to Install

### Option 1: Contribute to stolostron/acm-workflows (Recommended)

1. Fork https://github.com/stolostron/acm-workflows
2. Add your `acm-management` plugin to `Claude/plugins/`
3. Update `Claude/.claude-plugin/marketplace.json` to include your plugin
4. Submit a Pull Request
5. Once merged, users can install:
   ```bash
   claude plugins install acm-management@acm-workflows-plugins
   ```

### Option 2: Direct GitHub Install (When supported)

Users should be able to install directly from your repo:
```bash
# Future: When Claude supports this
claude plugins install github:apphe/acm-workflows-plugins/acm-management
```

**Note:** This feature appears to have limitations in current Claude Code version.

### Option 3: Manual Installation

Users can manually copy the plugin:
```bash
# Clone your repo
git clone https://github.com/apphe/acm-workflows-plugins.git

# Copy plugin files (requires existing acm-workflows-plugins marketplace)
mkdir -p ~/.claude/plugins/cache/acm-workflows-plugins/acm-management/1.0.0
cp -r acm-workflows-plugins/acm-management/* \
  ~/.claude/plugins/cache/acm-workflows-plugins/acm-management/1.0.0/
```

## Recommendation

**Best path forward:**
1. Develop locally using `sync-local.sh`
2. Once stable, contribute to stolostron/acm-workflows marketplace
3. This makes your skills available to the entire ACM QE team!
