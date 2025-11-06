# diane, Features Guide

## 🎯 Core Features

### Silent Recording
diane, operates silently by default, true to her character as a neutral witness. Records are saved without any output unless you use the `--verbose` flag.

```bash
# Silent recording
echo "Quick thought" | diane,

# With confirmation
echo "Quick thought" | diane, -v
# ✅ Recorded: 2025-11-06--13-34-57--quick-thought.md
```

### Multiple Input Methods

**From stdin/pipe:**
```bash
echo "Meeting notes" | diane,
cat notes.txt | diane,
```

**Interactive mode:**
```bash
diane,
# Type your content...
# Press Ctrl-D to save
```

**Direct argument:**
```bash
diane, "Quick reminder"
```

### Tags and Organization

Organize records with hierarchical tags:

```bash
# Single tag
diane, --tags work "Client meeting went well"

# Multiple tags (comma-separated)
diane, --tags work/urgent,projects/acme "Need to follow up"

# View tags in listings
diane, --list
# 📅 2025-11-06 13:12 | 🏷  work/urgent, projects/acme
```

---

## 🔍 Search Capabilities

### Exact Search

Basic substring search through all records:

```bash
# Search for keyword
diane, --search "meeting"

# Limit results
diane, --search "client" --limit 5
```

### Fuzzy Search ✨ NEW

Find records with approximate matching and similarity scores:

```bash
# Fuzzy search with scoring
diane, --search "architec" --fuzzy

# Output shows similarity percentage:
# 📅 2025-11-06 13:34 | 🎯 80% | 🏷  tech/architecture
# Discussion with the team about implementing microservices architecture
```

Fuzzy search is perfect for:
- Typos and misspellings
- Partial word matches
- Finding related content

---

## 🌐 Git Sync & Backup ✨ NEW

diane, can sync your records to a remote Git repository for backup and multi-device access.

### Setup Remote

```bash
# Add a GitHub repository as remote
diane, --set-remote git@github.com:username/diane-records.git

# Or use HTTPS
diane, --set-remote https://github.com/username/diane-records.git
```

### Check Status

```bash
diane, --remote-status

# Output:
# 📡 Remote Status
# ────────────────────────────────────────────────────────────
# Branch: master
# Remote: git@github.com:username/diane-records.git
# ✅ Up to date with remote
```

### Sync Operations

```bash
# Push records to remote
diane, --push

# Pull records from remote
diane, --pull

# Full sync (pull + push)
diane, --sync
```

### Multi-Device Workflow

On Device 1:
```bash
# Make some records
echo "Note from laptop" | diane,

# Push to remote
diane, --push
```

On Device 2:
```bash
# Pull latest records
diane, --pull

# Make more records
echo "Note from desktop" | diane,

# Push back
diane, --push
```

---

## 🖥️ TUI Dashboard ✨ NEW

Interactive terminal interface for browsing your records.

### Launch TUI

```bash
diane, --tui
```

### Features

- **Browsable list** of all records with timestamps and tags
- **Full content view** of selected record
- **Keyboard navigation:**
  - `j/k` or arrow keys to navigate
  - `r` to refresh
  - `q` to quit

### Installation

The TUI requires the `textual` package:

```bash
pip install "diane-cli[tui]"
# or
pip install "diane-cli[all]"
```

---

## 📋 Listing & Filtering

### List Recent Records

```bash
# Show 10 most recent (default)
diane, --list

# Show more
diane, --list --limit 20
```

### Filter by Date

```bash
# Today's records only
diane, --list --today
```

---

## 🗂️ Storage Format

Records are stored as plain Markdown files with YAML frontmatter in:
```
~/.local/share/diane/records/
```

### File Format

```markdown
---
timestamp: 2025-11-06 13:34
tags:
- work/clients
- urgent
sources:
- stdin
---

Your record content here...
```

### Filename Convention

Files are named with timestamp and first few words:
```
2025-11-06--13-34-57--meeting-with-client.md
```

This makes them:
- **Sortable** by timestamp
- **Searchable** by filename
- **Readable** by any text editor
- **Version-controlled** via Git

---

## 🔒 Security & Privacy

### Local First

All records are stored locally by default. Nothing leaves your machine unless you explicitly push to a remote.

### Git Versioning

Every record is automatically committed to a local Git repository, giving you:
- Complete history of all records
- Ability to revert changes
- Audit trail of modifications

### Encryption (Planned)

Future support for GPG encryption:
```bash
# Coming soon
diane, --encrypt "Sensitive information"
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# Custom data directory
export DIANE_DATA_HOME="$HOME/Documents/diane"

# GPG key for encryption (planned)
export DIANE_GPG_KEY="your-gpg-key-id"
```

### Shell Aliases

Add to your `.bashrc` or `.zshrc`:

```bash
# Quick dictation
alias d="diane,"
alias dv="diane, -v"

# Search shortcuts
alias ds="diane, --search"
alias df="diane, --search --fuzzy"

# List shortcuts
alias dl="diane, --list"
alias dt="diane, --list --today"

# Sync shortcuts
alias dp="diane, --push"
alias dpl="diane, --pull"
alias dsync="diane, --sync"
```

---

## 🎨 Use Cases

### Developer Notes

```bash
# Log a bug finding
diane, --tags bugs/prod "Race condition in payment processor"

# Architecture decisions
diane, --tags tech/architecture "Decided on microservices approach"

# Search your dev notes
diane, --search "payment" --fuzzy
```

### Meeting Notes

```bash
# Quick meeting summary
diane, --tags meetings/weekly "Q4 planning discussion - team alignment good"

# Search meetings
diane, --search "planning"
```

### Personal Journal

```bash
# Daily reflections
diane, --tags journal/personal "Feeling productive today"

# Search journal entries
diane, --search "productive" --fuzzy
```

### Research & Learning

```bash
# Save insights
diane, --tags learning/python "TIL: asyncio.gather vs asyncio.wait"

# Browse learning notes in TUI
diane, --tui
```

---

## 🚀 Advanced Workflows

### Integration with Other Tools

**Capture clipboard:**
```bash
# macOS
pbpaste | diane, --tags clipboard

# Linux (with xclip)
xclip -o | diane, --tags clipboard
```

**From web pages:**
```bash
# Extract text and save
curl -s https://example.com | html2text | diane, --tags web/research
```

**Git commit messages:**
```bash
# Save your commit message thoughts
git log -1 --pretty=%B | diane, --tags git/commits
```

### Scheduled Backups

Add to crontab for automatic daily sync:
```cron
0 2 * * * /usr/local/bin/diane, --sync
```

---

## 📊 Statistics & Analysis

All records are plain text, making them perfect for analysis:

```bash
# Count records
ls -1 ~/.local/share/diane/records/*.md | wc -l

# Most used tags
grep -h "^- " ~/.local/share/diane/records/*.md | sort | uniq -c | sort -rn

# Records per day
ls ~/.local/share/diane/records/ | cut -d- -f1-3 | uniq -c
```

---

## 🤝 Contributing

Found a bug? Have a feature idea? Visit the [GitHub repository](https://github.com/matias-ceau/diane).

---

*"Always listening, never interrupting, never forgetting."* — Diane's Law

---

## 🔐 Encryption (v0.2.0)

### GPG Encryption

Protect sensitive records with GPG encryption:

```bash
# Setup GPG key (interactive)
diane, --gpg-setup

# Or set environment variable
export DIANE_GPG_KEY="your-key-id"

# Encrypt a record
echo "Sensitive information" | diane, --encrypt

# Result: creates an encrypted .gpg file
# ~/.local/share/diane/records/2025-11-06--13-45-12--sensitive-information.md.gpg
```

### Managing Keys

```bash
# List available GPG keys
diane, --gpg-list-keys

# Output:
# 🔑 Available GPG keys:
# ────────────────────────────────────────────────────────────
# Key ID: ABC123DEF456
#    User: Your Name <your@email.com>
```

### Decrypting Records

```bash
# Decrypt a specific file
diane, --decrypt ~/.local/share/diane/records/2025-11-06--13-45-12--sensitive.md.gpg

# Output:
# Decrypting 2025-11-06--13-45-12--sensitive.md.gpg...
# ✅ Decrypted to 2025-11-06--13-45-12--sensitive.md
```

**Note:** Encrypted records are stored with `.gpg` extension and are not searchable without decryption first.

---

## 📤 Export & Integration (v0.2.0)

Export your records for use with other tools, backup, or analysis.

### Export Formats

**JSON** - Perfect for programmatic access:
```bash
# Export all records to JSON
diane, --export json

# Save to file
diane, --export json --export-file records.json

# Export only today's records
diane, --export json --today --export-file today.json
```

**CSV** - Great for spreadsheet analysis:
```bash
# Export to CSV
diane, --export csv --export-file records.csv

# Import into Excel, Google Sheets, etc.
```

**HTML** - Beautiful web-ready format:
```bash
# Generate styled HTML page
diane, --export html --export-file records.html

# Open in browser:
# open records.html  # macOS
# xdg-open records.html  # Linux
```

**Markdown** - Single consolidated document:
```bash
# Export all records to one markdown file
diane, --export markdown --export-file all-records.md
```

### Integration Examples

**Share records via email:**
```bash
# Export and email
diane, --export html --export-file /tmp/records.html
echo "Here are my notes" | mail -s "My Records" -a /tmp/records.html friend@example.com
```

**Backup to cloud:**
```bash
# Export and upload to cloud storage
diane, --export json --export-file ~/Dropbox/diane-backup-$(date +%Y%m%d).json
```

**Import into other tools:**
```bash
# Export JSON for processing
diane, --export json | jq '.[] | select(.tags[] | contains("work"))'
```

---

## 📊 Statistics & Analytics (v0.2.0)

Get insights into your recording habits and content.

### View Statistics

```bash
diane, --stats
```

**Output:**
```
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
  2025-11-03: █████ 5
  2025-11-04: ██ 2
  2025-11-05: ███████ 7
```

### Use Cases for Statistics

**Track productivity:**
- Monitor daily recording habits
- Identify productive periods
- See which topics you focus on most

**Analyze content:**
- Track word count trends
- Identify most-used tags
- Spot patterns in your thinking

**Set goals:**
- Aim for consistent daily records
- Balance different topic areas
- Build recording habits

---

## 🔗 Advanced Workflows (v0.2.0)

### Encrypted Backup Workflow

```bash
# Encrypt all sensitive records
export DIANE_GPG_KEY="your-key-id"
echo "Confidential meeting notes" | diane, --encrypt --tags work/confidential

# Sync to remote (encrypted files go to GitHub)
diane, --sync

# On another device, pull and decrypt
diane, --pull
diane, --decrypt ~/.local/share/diane/records/2025-11-06--14-20-30--confidential.md.gpg
```

### Export and Analyze Workflow

```bash
# Export all work notes to JSON
diane, --export json --export-file work-notes.json

# Analyze with jq
cat work-notes.json | jq '[.[] | select(.tags[] | contains("work"))] | length'

# Find most common words in work notes
cat work-notes.json | jq -r '.[] | select(.tags[] | contains("work")) | .content' | \
  tr ' ' '\n' | sort | uniq -c | sort -rn | head -20
```

### Daily Summary Workflow

```bash
# Create daily summaries
alias daily-summary='diane, --list --today --export html --export-file ~/summaries/$(date +%Y-%m-%d).html'

# Run at end of day
daily-summary

# Build a searchable archive of daily summaries
```

### Statistics-Driven Review

```bash
# Weekly review script
#!/bin/bash
echo "=== Weekly diane, Review ===" > /tmp/weekly-review.txt
diane, --stats >> /tmp/weekly-review.txt
diane, --list --limit 50 >> /tmp/weekly-review.txt
cat /tmp/weekly-review.txt | less
```

---

## 🎯 Complete Feature Matrix

| Feature | Command | Since |
|---------|---------|-------|
| **Recording** |
| Silent recording | `echo "text" \| diane,` | v0.1.0 |
| Interactive mode | `diane,` | v0.1.0 |
| With tags | `--tags work,urgent` | v0.1.0 |
| Encrypted | `--encrypt` | v0.2.0 |
| **Search & Browse** |
| Exact search | `--search "keyword"` | v0.1.0 |
| Fuzzy search | `--search "keyword" --fuzzy` | v0.1.0 |
| List records | `--list` | v0.1.0 |
| Today's records | `--list --today` | v0.1.0 |
| TUI browser | `--tui` | v0.1.0 |
| **Sync & Backup** |
| Set remote | `--set-remote <url>` | v0.1.0 |
| Push to remote | `--push` | v0.1.0 |
| Pull from remote | `--pull` | v0.1.0 |
| Full sync | `--sync` | v0.1.0 |
| Remote status | `--remote-status` | v0.1.0 |
| **Export** |
| Export JSON | `--export json` | v0.2.0 |
| Export CSV | `--export csv` | v0.2.0 |
| Export HTML | `--export html` | v0.2.0 |
| Export Markdown | `--export markdown` | v0.2.0 |
| **Encryption** |
| List GPG keys | `--gpg-list-keys` | v0.2.0 |
| Setup GPG | `--gpg-setup` | v0.2.0 |
| Decrypt file | `--decrypt <file>` | v0.2.0 |
| **Analytics** |
| Statistics | `--stats` | v0.2.0 |

---

*"Always listening, never interrupting, never forgetting."* — Diane's Law
