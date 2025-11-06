#!/usr/bin/env bash
# Enable seamless auto-sync for diane,
#
# This script configures diane, to automatically sync every time you save a record.
# No more manual syncing - it just happens in the background, invisibly.

set -e

echo "🔄 diane, Seamless Auto-Sync Setup"
echo "=================================="
echo ""

# Check if diane is installed
if ! command -v diane, &> /dev/null; then
    echo "❌ diane, not found. Please install first:"
    echo "   pip install --user diane-cli[all]"
    exit 1
fi

# Check if remote is configured
if ! diane, --remote-status 2>/dev/null | grep -q "Remote:"; then
    echo "⚠️  No remote configured yet."
    echo ""
    echo "To enable auto-sync, you need a remote repository."
    echo "Would you like to set one up now? (y/n)"
    read -r response

    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo ""
        echo "Enter your remote URL (e.g., git@github.com:user/diane-records.git):"
        read -r remote_url

        if [ -n "$remote_url" ]; then
            diane, --set-remote "$remote_url"
            echo "✅ Remote configured!"
        else
            echo "❌ No URL provided. Exiting."
            exit 1
        fi
    else
        echo ""
        echo "❌ Auto-sync requires a remote. Run this script again after configuring one."
        exit 1
    fi
fi

echo ""
echo "📋 Configuring auto-sync..."

# Detect shell
if [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
    SHELL_NAME="bash"
elif [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
    SHELL_NAME="zsh"
else
    SHELL_CONFIG="$HOME/.profile"
    SHELL_NAME="shell"
fi

# Add environment variable if not already present
if ! grep -q "DIANE_AUTO_SYNC" "$SHELL_CONFIG" 2>/dev/null; then
    echo "" >> "$SHELL_CONFIG"
    echo "# diane, auto-sync configuration" >> "$SHELL_CONFIG"
    echo "export DIANE_AUTO_SYNC=true" >> "$SHELL_CONFIG"
    echo "✅ Added DIANE_AUTO_SYNC to $SHELL_CONFIG"
else
    echo "ℹ️  DIANE_AUTO_SYNC already in $SHELL_CONFIG"
fi

# Enable for current session
export DIANE_AUTO_SYNC=true

echo ""
echo "✅ Seamless auto-sync enabled!"
echo ""
echo "📝 How it works:"
echo "   • Every time you save a record with diane,"
echo "   • It automatically syncs in the background"
echo "   • Non-blocking - doesn't slow down your capture"
echo "   • Only syncs when network is available"
echo "   • Automatically resolves conflicts (keeps your local changes)"
echo ""
echo "🎯 Test it now:"
echo "   echo 'Testing auto-sync' | diane, -v"
echo "   # Watch it sync automatically in the background!"
echo ""
echo "⚙️  Configuration:"
echo "   • Auto-sync: enabled (DIANE_AUTO_SYNC=true)"
echo "   • Mode: async (non-blocking)"
echo "   • Conflict strategy: keep local changes"
echo ""
echo "🔧 To disable:"
echo "   export DIANE_AUTO_SYNC=false"
echo "   # Or remove from $SHELL_CONFIG"
echo ""
echo "💡 Tip: Combine with quick shortcuts:"
echo "   source /path/to/quick-capture.sh"
echo "   d 'ultra-fast capture with auto-sync!'"
echo ""
echo "🎉 Now reload your shell:"
echo "   source $SHELL_CONFIG"
echo ""
echo "Happy seamless capturing! ✨"
