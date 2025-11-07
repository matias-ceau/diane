# diane, Quick Reference Card

> **"Diane, 11:30 a.m., February Twenty-fourth..."**

All shortcuts preserve the **comma (,)** to maintain the Twin Peaks aesthetic.

---

## 🎯 Pattern: `d,` + letter

Every shortcut starts with `d,` — maintaining diane's character!

---

## Core Capture

| Command | Description | Example |
|---------|-------------|---------|
| `d,` | Basic capture | `d, "my thought"` |
| `d,v` | Verbose (shows confirmation) | `d,v "confirmed"` |
| `echo ... \| d,` | From pipe | `echo "note" \| d,` |
| `d,` | Interactive (no args, opens editor) | `d,` |

---

## Input Sources

| Command | Description | Example |
|---------|-------------|---------|
| `d,c` | Capture clipboard | `d,c` |
| `d,t TAG` | Tagged capture | `d,t work "meeting"` |
| `d,e` | Encrypted capture | `d,e "secret"` |
| `d,s` | Capture selection (Linux) | `d,s` |
| `d,u` | Capture URL from browser (macOS) | `d,u` |

---

## Browse & Search

| Command | Description | Example |
|---------|-------------|---------|
| `d,l` | List recent records | `d,l` |
| `d,f QUERY` | Fuzzy search | `d,f keyword` |
| `d,se QUERY` | Exact search | `d,se keyword` |
| `d,st` | Statistics | `d,st` |
| `d,ui` | TUI dashboard | `d,ui` |
| `d,today` | Today's records | `d,today` |

---

## Sync Operations

| Command | Description | Example |
|---------|-------------|---------|
| `d,sync` | Full sync (pull + push) | `d,sync` |
| `d,push` | Push to remote | `d,push` |
| `d,pull` | Pull from remote | `d,pull` |
| `d,status` | Remote status | `d,status` |

---

## Export

| Command | Description | Example |
|---------|-------------|---------|
| `d,json` | Export to JSON | `d,json --export-file out.json` |
| `d,html` | Export to HTML | `d,html --export-file out.html` |
| `d,csv` | Export to CSV | `d,csv --export-file out.csv` |

---

## Help

| Command | Description |
|---------|-------------|
| `d,help` | Show all shortcuts |

---

## 💡 Common Workflows

### Quick Capture
```bash
d, "quick thought"              # 3 chars: d , space
echo "from pipe" | d,            # pipe to d,
d,v "show confirmation"          # verbose
```

### Tagged Workflows
```bash
d,t work "meeting notes"         # tag: work
d,t personal "buy milk"          # tag: personal
d,t ideas "new feature"          # tag: ideas
```

### Search & Review
```bash
d,f meeting                      # fuzzy search
d,l                              # list recent
d,today                          # just today
d,st                             # statistics
d,ui                             # TUI browser
```

### Clipboard Integration
```bash
# Copy something interesting, then:
d,c                              # instant capture

# Or tag it:
d,c --tags web/articles
```

### Multi-Device Sync
```bash
# Device 1
d, "working on feature"
d,push                           # manual push (or auto with DIANE_AUTO_SYNC=true)

# Device 2 (later)
d,pull                           # get latest
d, "continuing feature"
d,sync                           # bidirectional sync
```

---

## ⚡ With Auto-Sync Enabled

```bash
# Setup once
export DIANE_AUTO_SYNC=true

# Then just capture - syncs automatically!
d, "thought 1"                   # synced in background
d, "thought 2"                   # synced in background
d, "thought 3"                   # synced in background
# No manual sync needed ever!
```

---

## 🎨 Character Notes

The **comma (,)** is essential to diane's identity:

✅ `d,` — Preserves the Twin Peaks aesthetic
✅ `d,c` — Reads as "diane, clipboard"
✅ `d,t work` — Reads as "diane, tag work"
✅ `d,sync` — Reads as "diane, sync"

❌ `d` without comma — Loses the character
❌ `dc`, `dt`, `dl` — Generic, no personality

**Every command speaks to diane, with the pause (,) then the action.**

---

## 📝 Installation

```bash
# Source the shortcuts
source /path/to/scripts/quick-capture.sh

# Or add to your shell config
echo 'source /path/to/scripts/quick-capture.sh' >> ~/.bashrc
```

---

## 🎯 Character Count Comparison

| Action | Full Command | Shortcut | Saved |
|--------|--------------|----------|-------|
| Basic capture | `diane, "text"` (13) | `d, "text"` (8) | 38% |
| List | `diane, --list` (13) | `d,l` (3) | 77% |
| Search | `diane, --search --fuzzy` (23) | `d,f` (3) | 87% |
| Stats | `diane, --stats` (14) | `d,st` (4) | 71% |
| Sync | `diane, --sync` (13) | `d,sync` (6) | 54% |

**Average keystroke reduction: ~65%**

---

**diane, responds. Always listening, never interrupting, never forgetting.** ✨

*"Diane, sometimes the best shortcuts are the ones that preserve character."*
