# diane

> *"Diane, 11:30 a.m., February Twenty-fourth..."*

A minimalist CLI for capturing thoughts. Inspired by Agent Cooper's dictation practice.

---

## Quick Start

```bash
# Install
pip install diane-cli

# Install with audio support
pip install diane-cli[audio]

# Setup (first time)
diane setup

# Capture text (heredoc/pipe)
diane <<< "quick thought"           # Here-string
echo "meeting insights" | diane     # Pipe
diane << EOF                        # Heredoc (multiline)
Notes from meeting:
- Timeline discussed
- Next steps defined
EOF

# View latest records
diane                               # Default: show latest
diane show --limit 20               # Show more
diane show --today                  # Today only

# Record audio
diane record                        # Until Ctrl-C
diane record --duration 30          # 30 seconds

# Search (requires ripgrep + fzf)
diane search "meeting"

# Sync with remote
diane sync push
diane sync pull
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
- **Audio recording** — Record and transcribe
- **Git versioning** — Automatic commits
- **Smart defaults** — No args = show latest records
- **Pipe-friendly** — `timestamp|content` format when piped

### Audio

- **Voice recording** — Dictation via `--record`
- **Auto-transcription** — OpenAI Whisper API
- **Audio file support** — Transcribe existing files
- **Tool auto-detection** — PipeWire, ALSA, or ffmpeg
- **Temp storage** — Audio preserved if transcription fails

```bash
# Record until Ctrl-C
diane --record

# Record for 30 seconds
diane --record --record-duration 30

# Transcribe existing audio file
diane --audio-file meeting-recording.mp3

# List available microphones
diane --list-mics
```

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
# Capture text (heredoc - retro Unix style)
diane <<< "Remember to call client"
# ✓

# Multiline capture
diane << EOF
Project notes from meeting:
- Timeline: End of quarter
- Budget: Approved
- Next: Schedule kickoff
EOF
# ✓

# Capture with verbose output
echo "project notes" | diane -v
# ✅ Recorded: 2025-11-07--14-30-15--project-notes.md

# View records
diane show --limit 5
# ────────────────────────────────────────────────────────────
# 📅 2025-11-07 14:30
#
# Project notes from meeting
# ────────────────────────────────────────────────────────────

diane show --today
# Today's records

# Pipe to other tools (clean output)
diane show --limit 100 | wc -l
# 100

diane show --today | grep -i "meeting"
# 2025-11-07 14:30|Meeting with client about project timeline

# Search interactively
diane search "meeting"
# [Opens fzf with preview]

# Setup remote sync
diane setup
# ... interactive wizard ...

# Sync operations
diane sync push
diane sync pull
diane sync status

# Shortcuts
diane push                # Same as: diane sync push
diane pull                # Same as: diane sync pull

# Show configuration
diane info
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

**For Audio Recording**:
- One of: `pw-record` (PipeWire), `arecord` (ALSA), or `ffmpeg`
- OpenAI API key (for transcription)
- Python package: `pip install diane-cli[audio]`

**For Interactive Search**:
- `ripgrep` + `fzf` (for interactive search)
- `bat` (for search preview)

### Install Optional Tools

**macOS**:
```bash
brew install ripgrep fzf bat ffmpeg
```

**Ubuntu/Debian**:
```bash
# Audio (choose one)
apt install pipewire-bin        # PipeWire (modern, recommended)
apt install alsa-utils          # ALSA (traditional)
apt install ffmpeg              # ffmpeg (fallback)

# Search
apt install ripgrep fzf bat
```

**Audio Setup**:
```bash
# Install audio support
pip install diane-cli[audio]

# Set OpenAI API key
export OPENAI_API_KEY=sk-...

# Test audio setup
diane record --list-devices
```

---

## Help

```bash
diane --help                    # Main help
diane show --help               # Command-specific help
diane sync --help               # Group help

# Beautiful, colorful help menus powered by rich-click
```

---

## Documentation

- **[CHANGELOG.md](CHANGELOG.md)** — Version history
- **[LICENSE](LICENSE)** — MIT License

---

## What's New in v0.4.0

**Command-Based Structure** — Better organization and clarity

### New Command Structure

**Text capture** (heredoc/pipe only):
```bash
diane <<< "text"              # Here-string (retro Unix style)
diane << EOF ... EOF           # Heredoc (multiline)
echo "text" | diane            # Pipe
```

**Commands** (was: flat flags):
```bash
diane show [OPTIONS]           # Was: diane --list
diane record [OPTIONS]         # Was: diane --record
diane search [QUERY]           # Was: diane --search
diane tui                      # Was: diane --tui

diane sync [push|pull|status]  # Was: diane --sync/--push/--pull
diane export [FORMAT]          # Was: diane --export
diane stats                    # Was: diane --stats
diane setup                    # Was: diane --setup
diane info                     # Was: diane --info
```

### Benefits

- **Clear intent**: `diane show` vs `diane --list`
- **Organization**: Related operations grouped (sync)
- **Discoverable**: Commands clear in help
- **Scalable**: Easy to add new features
- **Standard**: Matches modern CLIs (uv, docker, git)

**Breaking Changes**:
- Removed `diane [TEXT]` argument (use heredoc/pipe instead)
- All flags converted to commands
- Convenience aliases provided (`diane push` still works)

---

## License

MIT — See [LICENSE](LICENSE)
