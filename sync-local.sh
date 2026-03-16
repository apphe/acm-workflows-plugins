#!/bin/bash
# Sync acm-management plugin to Claude cache for local testing

SOURCE="$HOME/projects/acm-workflows-plugins/acm-management"
DEST="$HOME/.claude/plugins/cache/acm-workflows-plugins/acm-management/1.0.0"

echo "Syncing plugin to Claude cache..."
rm -rf "$DEST"
mkdir -p "$DEST"
cp -r "$SOURCE"/* "$DEST"/
cp -r "$SOURCE"/.claude-plugin "$DEST"/

echo "✓ Plugin synced successfully!"
echo ""
echo "Test your skill with:"
echo "  /acm-management:acm-support-analyzer \"ACM 2.15 on OCP 4.16\""
