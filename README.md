# diane — Thought Clerk

> *"Diane, 11:30 a.m., February Twenty-fourth..."*

A minimalist CLI for capturing thoughts with zero friction. Inspired by Agent Cooper's dictation to Diane in Twin Peaks.

---

## Quick Start

```bash
# Install
pip install diane-cli

# Setup (first time)
diane --setup

# Record a thought
echo "meeting insights" | diane
# ✓

# View latest records
diane

# Search (requires ripgrep + fzf)
diane --search "meeting"

# Show today's records
diane --today
```

---

## Philosophy

**diane** follows Unix principles:

- **Do one thing well**: Capture and retrieve thoughts
- **Compose with other tools**: Clean output when piped (`diane | wc -l`)
- **Silent unless needed**: Simple `✓` confirmation, detailed with `--verbose`
- **Plain text storage**: Markdown files with Git versioning

---

## Features

### Core

- **Frictionless capture** — Pipe, args, or interactive
- **Git versioning** — Automatic commits
- **Smart defaults** — No args = show latest records
- **Pipe-friendly** — `timestamp|content` format when piped

### Search & Browse

- **Interactive search** — ripgrep + fzf integration
- **Date filtering** — `--today` flag
- **TUI dashboard** — `--tui` for terminal UI

### Sync & Export

- **Git remote sync** — Push/pull to GitHub/GitLab
- **Auto-sync** — Background sync (configurable)
- **Export** — JSON, CSV, HTML, Markdown

### Statistics

```bash
diane --stats
# 📊 Record Statistics
# Total Records: 156
# Total Words: 12,847
# Avg Words/Record: 82.3
# Busiest Day: 2025-11-03 (23 records)
```

---

## Usage Examples

```bash
# Record from argument
diane "Remember to call client"
# ✓

# Record from pipe
pbpaste | diane
# ✓

# Record with verbose output
echo "project notes" | diane --verbose
# ✅ Recorded: 2025-11-07--14-30-15--project-notes.md

# View latest 5 records
diane --limit 5
# ────────────────────────────────────────────────────────────
# 📅 2025-11-07 14:30
#
# Project notes from meeting
# ────────────────────────────────────────────────────────────
# ...

# Pipe to other tools (clean output)
diane --limit 100 | wc -l
# 100

diane --today | grep -i "meeting"
# 2025-11-07 14:30|Meeting with client about project timeline

# Search interactively
diane --search "meeting"
# [Opens fzf with preview]

# Setup remote sync
diane --setup
# ... interactive wizard ...

# Sync operations
diane --sync   # pull + push
diane --push   # push only
diane --pull   # pull only

# Show configuration
diane --info
# 📍 diane Configuration
# Records Directory: /Users/you/.local/share/diane/records
# Git Enabled:       True
# Auto-sync:         False
```

---

## Easter Egg

The comma is a tribute to Twin Peaks. Use it to bypass option parsing:

```bash
diane , "some text --that --looks like options"
# Equivalent to: diane -- "some text --that --looks like options"
```

---

## Storage

Records are stored as plain Markdown files:

```markdown
---
timestamp: 2025-11-07 14:30
sources:
- stdin
---

Your thought here
```

**Location**: `~/.local/share/diane/records/` (or `$DIANE_DATA_HOME/records`)

---

## Dependencies

**Required**:
- Python ≥ 3.8
- Git (for versioning)

**Optional**:
- `ripgrep` + `fzf` (for interactive search)
- `bat` (for search preview)

Install on macOS:
```bash
brew install ripgrep fzf bat
```

Install on Ubuntu/Debian:
```bash
apt install ripgrep fzf bat
```

---

## Help

```bash
diane --help
# Beautiful, colorful help menu powered by rich-click
```

---

## Documentation

- **[CHANGELOG.md](CHANGELOG.md)** — Version history
- **[LICENSE](LICENSE)** — MIT License

---

## What's New in v0.3.0

**Major Refactor** — Simplified & Unix-friendly

- ✅ **Removed tags** — Focus on simple, fast capture
- ✅ **Default shows records** — `diane` with no args = latest records
- ✅ **Pipe-friendly output** — Clean `timestamp|content` format
- ✅ **Rich help menus** — Colorful, organized help
- ✅ **First-run wizard** — `--setup` guides configuration
- ✅ **--info command** — Show paths and config
- ✅ **Comma easter egg** — `diane , "text"` = `diane -- "text"`
- ✅ **Simple confirmations** — `✓` by default, detailed with `-v`

**Breaking Changes**:
- Removed `--tags` option (simplification)
- Removed `--encrypt` flag (local encryption removed)
- Removed `-s` short flag for search (avoid conflicts)
- Changed default behavior (shows records instead of waiting for input)

---

## License

MIT — See [LICENSE](LICENSE)
