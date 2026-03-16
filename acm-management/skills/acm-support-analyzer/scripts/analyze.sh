#!/bin/bash
# Helper script for ACM Support Exception Analysis
# This can be used standalone or called by Claude

set -e

# Configuration
GDOC_URL="https://docs.google.com/document/d/1TW_Mki_ye7d7vcII2al35BvdSiYmJl2yoK_qFlSs5QE/edit?tab=t.0"

# Usage
usage() {
    echo "Usage: $0 'support request description'"
    echo "Example: $0 'ACM 2.15 upgrade from RKE2 to OCP 4.16'"
    exit 1
}

# Check parameters
if [ -z "$1" ]; then
    usage
fi

REQUEST="$1"

echo "Analyzing ACM support request..."
echo "Request: $REQUEST"
echo "Document: $GDOC_URL"
echo ""

# Note: This script requires gdoc-downloader and Claude Code CLI
# The actual analysis logic is in SKILL.md and executed by Claude

echo "This is a helper script. Use the Claude skill for full functionality:"
echo "  /acm-management:acm-support-analyzer \"$REQUEST\""
