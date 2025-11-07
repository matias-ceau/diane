#!/usr/bin/env bash
# Ultra-fast diane, capture shortcuts
#
# Source this in your ~/.bashrc or ~/.zshrc:
#   source /path/to/quick-capture.sh
#
# All shortcuts maintain the comma (,) to preserve the Twin Peaks aesthetic
# Pattern: d, for basic, d,X for variants

# Core capture - THE quintessential "diane," command
d,() {
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

# Verbose variant - "diane, verbose"
d,v() {
    diane, -v "$@"
}

# Clipboard - "diane, clipboard"
d,c() {
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

# Tagged capture - "diane, tag"
d,t() {
    if [ $# -eq 0 ]; then
        echo "Usage: d,t <tag> [text]"
        echo "Example: d,t work \"meeting notes\""
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

# Encrypted capture - "diane, encrypted"
d,e() {
    if [ -z "$DIANE_GPG_KEY" ]; then
        echo "⚠️  Warning: DIANE_GPG_KEY not set"
    fi
    diane, --encrypt "$@"
}

# Selection (Linux only) - "diane, selection"
d,s() {
    if command -v xclip &> /dev/null; then
        xclip -o -selection primary | diane, "$@" -v
    else
        echo "❌ xclip not found (install with: apt install xclip)"
        return 1
    fi
}

# URL from browser (macOS) - "diane, url"
d,u() {
    if command -v osascript &> /dev/null; then
        local url=$(osascript -e 'tell application "Safari" to return URL of front document')
        echo "$url" | diane, --tags web/bookmarks -v
    else
        echo "❌ macOS only"
        return 1
    fi
}

# List - "diane, list"
d,l() {
    diane, --list "$@"
}

# Fuzzy search - "diane, find"
d,f() {
    diane, --search --fuzzy "$@"
}

# Exact search - "diane, search exact"
d,se() {
    diane, --search "$@"
}

# Stats - "diane, stats"
d,st() {
    diane, --stats
}

# TUI - "diane, ui"
d,ui() {
    diane, --tui
}

# Today's records - "diane, today"
d,today() {
    diane, --list --today "$@"
}

# Sync operations - "diane, sync"
d,sync() {
    diane, --sync
}

# Push - "diane, push"
d,push() {
    diane, --push
}

# Pull - "diane, pull"
d,pull() {
    diane, --pull
}

# Remote status - "diane, status"
d,status() {
    diane, --remote-status
}

# Export shortcuts - "diane, json" etc.
d,json() {
    diane, --export json "$@"
}

d,html() {
    diane, --export html "$@"
}

d,csv() {
    diane, --export csv "$@"
}

# Watch mode - auto-sync on save (Linux with inotifywait)
d,watch() {
    echo "👁️  Watching for changes..."
    while true; do
        inotifywait -e modify,create ~/.local/share/diane/records/ 2>/dev/null && diane, --sync
        sleep 5
    done
}

# Help - show all shortcuts
d,help() {
    cat << 'EOF'
diane, Quick Capture Shortcuts
==============================

Core:
  d,              Basic capture (interactive with editor if no args)
  d,v             Verbose capture (shows confirmation)

Input Sources:
  d,c             Capture clipboard
  d,s             Capture selection (Linux)
  d,u             Capture URL from browser (macOS)
  d,t TAG [text]  Tagged capture

Special:
  d,e             Encrypted capture

Browse & Search:
  d,l             List recent records
  d,f QUERY       Fuzzy search
  d,se QUERY      Exact search
  d,st            Show statistics
  d,ui            Launch TUI dashboard
  d,today         Today's records

Sync:
  d,sync          Sync with remote
  d,push          Push to remote
  d,pull          Pull from remote
  d,status        Show remote status

Export:
  d,json          Export to JSON
  d,html          Export to HTML
  d,csv           Export to CSV

Examples:
  d, "quick thought"           # Direct capture
  echo "note" | d,             # From pipe
  d,c                          # Capture clipboard
  d,t work "meeting notes"     # Tagged capture
  d,f keyword                  # Fuzzy search
  d,st                         # View stats

Note: All shortcuts preserve the comma (,) for that Twin Peaks aesthetic!
      "Diane, 11:30 a.m., February Twenty-fourth..."
EOF
}

# Completion setup hint
alias diane-complete-setup='echo "Add to your shell config:
Bash: source /path/to/diane.bash-completion
Zsh:  source /path/to/diane.zsh-completion
Fish: cp /path/to/diane.fish-completion ~/.config/fish/completions/"'

echo "✨ diane, shortcuts loaded! Type 'd,help' for usage."
