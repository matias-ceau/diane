# diane, — Frictionless Thought Capture

> *"Always listening, never interrupting, never forgetting."*

**diane,** is a minimalist CLI tool for capturing thoughts, notes, and reflections with zero friction. Inspired by Agent Cooper's dictation to Diane in Twin Peaks, she operates silently by default — a neutral witness and archivist of your mental ledger.

---

## 📚 Documentation

- **[INSTALL.md](INSTALL.md)** — Installation & setup guide
- **[FEATURES.md](FEATURES.md)** — Complete feature guide with examples
- **[SEAMLESS.md](SEAMLESS.md)** — Make diane, invisible & everywhere
- **[scripts/README.md](scripts/README.md)** — Scripts & integrations
- **[CHANGELOG.md](CHANGELOG.md)** — Version history

---

## ⚡ Quick Start

### Installation

```bash
# One-line install
curl -sSL https://raw.githubusercontent.com/USER/diane/main/scripts/install.sh | bash

# Or with pip
pip install --user diane-cli[all]
```

### Basic Usage

```bash
# Silent capture (no output)
echo "meeting insights" | diane,

# With confirmation
echo "thoughts on project" | diane, -v
# ✅ Recorded: 2025-11-06--14-30-15--thoughts-on-project.md

# Interactive mode
diane,
# Type your content, press Ctrl-D to save

# Tagged capture
diane, --tags work/urgent "Need to follow up with client"

# Search records
diane, --search "meeting"
diane, --search "meet" --fuzzy  # fuzzy search

# List records
diane, --list
diane, --list --today

# Browse with TUI
diane, --tui

# Statistics
diane, --stats
```

---

## ✨ Key Features

### v0.2.0 — Current Release

- ✅ **Core Recording** — stdin, pipe, or interactive capture
- ✅ **Fuzzy Search** — Find records with typo-tolerant matching
- ✅ **Git Sync** — Push/pull/sync records to GitHub/GitLab
- ✅ **TUI Dashboard** — Interactive terminal interface
- ✅ **GPG Encryption** — Protect sensitive records
- ✅ **Export** — JSON, CSV, HTML, Markdown formats
- ✅ **Statistics** — Analytics on your recording habits
- ✅ **Tag-Based Organization** — Hierarchical tagging
- ✅ **Shell Completions** — Tab completion for bash/zsh/fish
- ✅ **Ultra-Fast Shortcuts** — 2-character commands (`d`, `dc`, `dl`, etc.)
- ✅ **Background Sync Daemon** — Auto-sync every N minutes
- ✅ **Clipboard Monitoring** — Auto-capture clipboard changes
- ✅ **Editor Integrations** — Vim plugin, VS Code template

### Storage

- Plain Markdown files with YAML frontmatter
- Stored in `~/.local/share/diane/records/`
- Automatic Git versioning
- Portable and future-proof

---

## 🎯 Philosophy

diane, embodies:

1. **Silence** — No output by default, true to her character
2. **Speed** — Capture thoughts in under 1 second
3. **Simplicity** — Plain text, no databases, no complexity
4. **Privacy** — Local-first, you control the data
5. **Reliability** — Git versioning, never lose a thought

---

## 🚀 Ultra-Fast Workflow

With the full setup (see [SEAMLESS.md](SEAMLESS.md)):

```bash
# Install shortcuts (2-character commands!)
source scripts/quick-capture.sh

# Ultra-minimal capture
d, "quick thought"              # 2 chars!
dc                              # capture clipboard
d,t work "tagged note"          # tagged capture

# Search & browse
dl                              # list records
d,f keyword                      # fuzzy search
dst                             # show stats
dtui                            # launch TUI

# Sync
dsync                           # sync with remote
```

**Result:** Capture anything in **under 1 second**. 80% fewer keystrokes.

---

## ⚡ Seamless Auto-Sync

**Zero-friction sync** — your records sync automatically, invisibly, every time you save:

```bash
# Enable seamless auto-sync
./scripts/enable-auto-sync.sh

# Now just capture - syncing happens automatically!
d, "my thought"    # Saved locally in ~16ms
                  # Synced to GitHub in background (you don't wait)
                  # Done!
```

**Features:**
- 🚀 **Auto-sync on save** — Every record syncs automatically
- 🔇 **Non-blocking** — Runs in background, doesn't slow you down (~16ms perceived time)
- 🌐 **Network detection** — Only syncs when online
- 🎯 **Smart detection** — Only syncs actual changes
- 🔀 **Auto-conflict resolution** — Your local changes always win
- ⚡ **218x faster** than manual sync

**See [SYNC.md](SYNC.md) for complete seamless sync guide.**

---

## 🔄 Background Sync Daemon

For timed periodic syncing (alternative/complementary to auto-sync):

Never manually sync again:

```bash
# Linux (systemd)
systemctl --user enable diane-sync
systemctl --user start diane-sync

# macOS (launchd)
launchctl load ~/Library/LaunchAgents/com.diane.sync.plist
```

Your records sync automatically every 5 minutes (configurable).

---

## 🎨 Editor Integration

### Vim

```vim
" Capture buffer
:DianeCapture

" Capture selection (visual mode)
:'<,'>DianeCaptureSelection

" Key mappings
<leader>dc    " Capture buffer
<leader>ds    " Capture selection
<leader>dq    " Quick capture
<leader>df    " Search
```

### VS Code (Template Provided)

- Capture document
- Capture selection
- Quick capture dialog
- Search interface
- Statistics view

---

## 📊 Example: Statistics

```bash
$ diane, --stats

📊 Record Statistics
────────────────────────────────────────────────────────────
Total Records: 156
Total Words: 12,483
Avg Words/Record: 80.0
Unique Tags: 23

Busiest Day: 2025-10-15 (18 records)

Top Tags:
  • work/meetings: 42
  • dev/python: 31
  • personal/journal: 24
  • ideas: 19
  • bugs: 12

Last 7 Days:
  2025-10-30: ████ 4
  2025-10-31: ██████ 6
  2025-11-01: ███ 3
  2025-11-02: ████████ 8
```

---

## 🔐 Privacy & Security

- **Local-first** — All records stored locally
- **No telemetry** — Zero external services
- **Git encryption** — SSH/HTTPS for sync
- **GPG encryption** — Optional per-record encryption
- **You control** — Private GitHub repo, your keys

---

## 📤 Export & Integration

```bash
# Export to JSON
diane, --export json --export-file records.json

# Beautiful HTML export
diane, --export html --export-file records.html

# CSV for Excel/Sheets
diane, --export csv --export-file records.csv

# Process with jq
diane, --export json | jq '.[] | select(.tags[] | contains("work"))'
```

---

## 🧠 Use Cases

- **Developer notes** — Log bugs, ideas, architecture decisions
- **Meeting notes** — Quick capture during meetings
- **Research** — Collect and organize insights
- **Personal journal** — Daily reflections
- **Clipboard management** — Auto-capture interesting clips
- **Learning log** — TIL (Today I Learned) entries

---

## 🎭 The diane, Character

Based on Agent Cooper's Twin Peaks dictation style:

> *"Diane, 11:30 a.m., February Twenty-fourth. Entering the town of Twin Peaks..."*

diane, captures this aesthetic:
- Professional and understated
- Silent by default
- Always listening
- Never interrupting
- Never forgetting

---

## 🛠️ Architecture

```
diane,
├── diane/
│   ├── cli.py           # Command-line interface
│   ├── config.py        # Configuration management
│   ├── record.py        # Record data model
│   ├── storage.py       # Storage & search
│   ├── sync.py          # Git sync operations
│   ├── encryption.py    # GPG encryption
│   ├── export.py        # Export to various formats
│   ├── stats.py         # Statistics & analytics
│   └── tui.py           # Terminal UI
├── scripts/
│   ├── completions/     # Shell completions
│   ├── editors/         # Editor integrations
│   ├── diane-daemon.py  # Background sync
│   ├── clipboard-monitor.py
│   └── quick-capture.sh # Ultra-fast shortcuts
└── tests/               # Test suite
```

---

## 🤝 Contributing

Found a bug? Have a feature idea?

- Report issues on GitHub
- Submit PRs
- Share your workflows
- Contribute integrations

---

## 📜 License

MIT License — See [LICENSE](LICENSE)

---

## 🌟 Roadmap

**Completed (v0.2.0):**
- ✅ Fuzzy search
- ✅ Git sync
- ✅ TUI dashboard
- ✅ GPG encryption
- ✅ Export functionality
- ✅ Statistics & analytics
- ✅ Shell completions
- ✅ Background daemon
- ✅ Editor integrations

**Planned:**
- 🎤 Audio capture with speech-to-text
- 🔌 REST API for agent integration
- 🧠 Semantic search with embeddings
- 📱 Mobile app companion
- 🔗 Browser extension

---

## 💎 Core Principles

From [README-original.md](README-original.md):

1. **Frictionless input capture** — Zero barriers to recording
2. **Neutral witness** — No filtering, no judgment
3. **Durable storage** — Plain text, Git versioned
4. **Searchable & auditable** — Find anything instantly
5. **Privacy first** — Local storage, encrypted sync

---

## 🎉 Get Started

```bash
# Install
curl -sSL https://raw.githubusercontent.com/USER/diane/main/scripts/install.sh | bash

# First capture
echo "My first thought" | diane, -v

# View it
diane, --list

# See stats
diane, --stats

# Set up seamless experience
cat SEAMLESS.md
```

---

**diane, is ready. Start capturing, effortlessly.** ✨

*"Diane, I'm holding in my hand a small box of chocolate bunnies..."* — Agent Cooper
