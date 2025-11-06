#!/usr/bin/env bash
# Ultra-fast diane, capture shortcuts
#
# Source this in your ~/.bashrc or ~/.zshrc:
#   source /path/to/quick-capture.sh

# Quick capture - ultra minimal
d() {
    if [ -p /dev/stdin ]; then
        # Reading from pipe
        diane, "$@"
    elif [ $# -eq 0 ]; then
        # No args - interactive with editor
        local tmpfile=$(mktemp)
        ${EDITOR:-vim} "$tmpfile"
        if [ -s "$tmpfile" ]; then
            cat "$tmpfile" | diane,
            echo "✅ Captured"
        fi
        rm "$tmpfile"
    else
        # Args provided
        diane, "$@"
    fi
}

# Quick capture with verbose
dv() {
    diane, -v "$@"
}

# Capture clipboard
dc() {
    if command -v pbpaste &> /dev/null; then
        # macOS
        pbpaste | diane, "$@" -v
    elif command -v xclip &> /dev/null; then
        # Linux with xclip
        xclip -o -selection clipboard | diane, "$@" -v
    elif command -v wl-paste &> /dev/null; then
        # Wayland
        wl-paste | diane, "$@" -v
    else
        echo "❌ No clipboard tool found (install xclip or wl-paste)"
        return 1
    fi
}

# Capture with tag (fast tagging)
dt() {
    if [ $# -eq 0 ]; then
        echo "Usage: dt <tag> [text]"
        echo "Example: dt work \"meeting notes\""
        return 1
    fi

    local tag="$1"
    shift

    if [ -p /dev/stdin ]; then
        diane, --tags "$tag" "$@"
    else
        diane, --tags "$tag" "$@"
    fi
}

# Capture from selection (Linux only)
ds() {
    if command -v xclip &> /dev/null; then
        xclip -o -selection primary | diane, "$@" -v
    else
        echo "❌ xclip not found (install with: apt install xclip)"
        return 1
    fi
}

# Quick capture with encryption
de() {
    if [ -z "$DIANE_GPG_KEY" ]; then
        echo "⚠️  Warning: DIANE_GPG_KEY not set"
    fi
    diane, --encrypt "$@"
}

# Capture URL from browser (macOS only)
du() {
    if command -v osascript &> /dev/null; then
        local url=$(osascript -e 'tell application "Safari" to return URL of front document')
        echo "$url" | diane, --tags web/bookmarks -v
    else
        echo "❌ macOS only"
        return 1
    fi
}

# Quick search aliases
dl() { diane, --list "$@"; }
df() { diane, --search --fuzzy "$@"; }
dfs() { diane, --search "$@"; }
dst() { diane, --stats; }
dtui() { diane, --tui; }

# Sync shortcuts
dp() { diane, --push; }
dpl() { diane, --pull; }
dsync() { diane, --sync; }
dstatus() { diane, --remote-status; }

# Export shortcuts
djson() { diane, --export json "$@"; }
dhtml() { diane, --export html "$@"; }
dcsv() { diane, --export csv "$@"; }

# Today's records
dtoday() {
    diane, --list --today "$@"
}

# Watch mode - auto-sync on save
dwatch() {
    echo "👁️  Watching for changes..."
    while true; do
        inotifywait -e modify,create ~/.local/share/diane/records/ 2>/dev/null && diane, --sync
        sleep 5
    done
}

# Completion setup hint
alias diane-complete-setup='echo "Add to your shell config:
Bash: source /path/to/diane.bash-completion
Zsh:  source /path/to/diane.zsh-completion
Fish: cp /path/to/diane.fish-completion ~/.config/fish/completions/"'
