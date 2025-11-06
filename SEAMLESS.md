# diane, - Seamless Setup Guide

Make diane, **invisible, instant, and everywhere**. This guide will help you set up diane, for maximum efficiency and minimal friction.

## 🎯 Goal: Zero-Friction Capture

By the end of this setup, you'll be able to:
- Capture thoughts in **under 1 second**
- Access diane from **anywhere** (terminal, editor, clipboard)
- **Auto-sync** in the background
- Use **2-3 character** shortcuts instead of full commands

---

## 📦 Installation

### Quick Install (Recommended)

```bash
# One-line install
curl -sSL https://raw.githubusercontent.com/USER/diane/main/scripts/install.sh | bash

# Reload shell
source ~/.bashrc  # or ~/.zshrc
```

### Manual Install

```bash
# Install package
pip install --user diane-cli[all]

# Add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Install completions and shortcuts
git clone https://github.com/USER/diane
cd diane
./scripts/install.sh
```

---

## ⚡ Ultra-Fast Shortcuts

The quick-capture.sh script provides **ultra-minimal** aliases:

### Basic Shortcuts

```bash
# d - Fastest capture (2 characters!)
d, "meeting notes"                # Direct capture
echo "thoughts" | d,              # From pipe
d                                # Opens editor

# dv - Verbose capture
dv "show confirmation"

# dc - Capture clipboard
dc                               # Capture what's in clipboard

# dt - Tagged capture
d,t work "meeting with client"    # Capture with tag

# de - Encrypted capture
de "sensitive information"
```

### Search & Browse

```bash
dl                               # List records
d,f keyword                       # Fuzzy search
dfs keyword                      # Exact search
dst                              # Statistics
dtui                             # TUI browser
dtoday                           # Today's records
```

### Sync Shortcuts

```bash
dp                               # Push to remote
dpl                              # Pull from remote
dsync                            # Full sync
dstatus                          # Check remote status
```

### Export Shortcuts

```bash
djson                            # Export to JSON
dhtml                            # Export to HTML
dcsv                             # Export to CSV
```

---

## 🔄 Background Auto-Sync

Never lose your records - set up automatic background syncing:

### Linux (systemd)

```bash
# Copy daemon script
sudo cp scripts/diane-daemon.py /usr/local/bin/
sudo chmod +x /usr/local/bin/diane-daemon.py

# Copy service file
sudo cp scripts/systemd/diane-sync.service /etc/systemd/user/

# Enable and start
systemctl --user enable diane-sync
systemctl --user start diane-sync

# Check status
systemctl --user status diane-sync
```

### macOS (launchd)

```bash
# Copy daemon script
sudo cp scripts/diane-daemon.py /usr/local/bin/
sudo chmod +x /usr/local/bin/diane-daemon.py

# Copy plist
cp scripts/launchd/com.diane.sync.plist ~/Library/LaunchAgents/

# Load service
launchctl load ~/Library/LaunchAgents/com.diane.sync.plist

# Check if running
launchctl list | grep diane
```

### Manual Background Mode

```bash
# Start daemon manually
nohup diane-daemon.py --interval 300 &

# Or use screen/tmux
screen -dmS diane diane-daemon.py
```

---

## 📋 Clipboard Integration

### Auto-Monitor Clipboard

```bash
# Watch clipboard and prompt for each change
clipboard-monitor.py

# Auto-capture everything
clipboard-monitor.py --auto-capture

# Only capture URLs
clipboard-monitor.py --auto-capture --filter 'https?://' --tag web/bookmarks

# Only capture long text (min 100 chars)
clipboard-monitor.py --auto-capture --min-length 100 --tag clipboard/long
```

### Clipboard Shortcuts

Already set up with quick-capture.sh:

```bash
# Capture current clipboard
d,c

# Capture selection (Linux only)
ds
```

---

## 🎨 Editor Integration

### Vim

```bash
# Install plugin
cp scripts/editors/diane.vim ~/.vim/plugin/

# Or with vim-plug (add to .vimrc)
Plug '~/path/to/diane/scripts/editors/diane.vim'
```

**Vim Commands:**
- `:DianeCapture` - Capture current buffer
- `:DianeCaptureSelection` - Capture visual selection
- `:DianeCaptureWithTags` - Capture with tag prompt
- `:DianeQuick` - Quick capture from command
- `:DianeSearch keyword` - Search records

**Vim Key Mappings:**
- `<leader>dc` - Capture buffer
- `<leader>ds` - Capture selection (visual mode)
- `<leader>dt` - Capture with tags
- `<leader>dq` - Quick capture
- `<leader>df` - Search

### VS Code

```bash
# Copy extension template
cp scripts/editors/diane-vscode.js ~/diane-vscode-extension/

# Develop and package with:
cd ~/diane-vscode-extension
npm init
npm install vscode
vsce package
```

**VS Code Commands (when extension is ready):**
- `Diane: Capture Document`
- `Diane: Capture Selection`
- `Diane: Quick Capture`
- `Diane: Search`
- `Diane: Show Statistics`

---

## 🔑 Shell Completions

Completions are auto-installed by install.sh, but you can install manually:

### Bash

```bash
cp scripts/completions/diane.bash-completion ~/.bash_completion.d/diane
source ~/.bash_completion.d/diane
```

### Zsh

```bash
mkdir -p ~/.zsh/completion
cp scripts/completions/diane.zsh-completion ~/.zsh/completion/_diane

# Add to ~/.zshrc
fpath=(~/.zsh/completion $fpath)
autoload -Uz compinit && compinit
```

### Fish

```bash
cp scripts/completions/diane.fish-completion ~/.config/fish/completions/diane.fish
```

Now you get **tab completion** for all diane commands!

---

## 🎪 Global Hotkeys (Advanced)

### Linux (with xbindkeys)

```bash
# Install xbindkeys
sudo apt install xbindkeys

# Create config
cat > ~/.xbindkeysrc << 'EOF'
# Ctrl+Alt+D - Quick capture
"gnome-terminal --window --command='bash -c \"read -p \\\"Quick capture: \\\" text && echo \$text | diane, -v; read -p \\\"Press enter...\\\"\"'"
  Control+Alt + d

# Ctrl+Alt+C - Capture clipboard
"xclip -o -selection clipboard | diane, --tags clipboard -v && notify-send 'diane,' 'Clipboard captured'"
  Control+Alt + c
EOF

# Reload
xbindkeys --poll-rc
```

### macOS (with Hammerspoon or Karabiner-Elements)

```lua
-- Hammerspoon config (~/.hammerspoon/init.lua)
hs.hotkey.bind({"cmd", "alt"}, "D", function()
  local text = hs.dialog.textPrompt("diane, quick capture", "Enter your thought:")
  if text then
    os.execute('echo "' .. text .. '" | diane, -v')
    hs.alert.show("✅ Captured")
  end
end)

hs.hotkey.bind({"cmd", "alt"}, "C", function()
  os.execute('pbpaste | diane, --tags clipboard -v')
  hs.alert.show("✅ Clipboard captured")
end)
```

---

## 🚀 Recommended Complete Setup

Here's the ultimate seamless setup:

### 1. Install Everything

```bash
# Install diane with all features
pip install --user diane-cli[all]

# Run setup script
./scripts/install.sh

# Source shell config
source ~/.bashrc  # or ~/.zshrc
```

### 2. Configure Git Sync

```bash
# Create a private GitHub repo for your records
gh repo create diane-records --private

# Set remote
diane, --set-remote git@github.com:username/diane-records.git

# Initial push
diane, --push
```

### 3. Enable Background Sync

```bash
# Linux
systemctl --user enable diane-sync
systemctl --user start diane-sync

# macOS
launchctl load ~/Library/LaunchAgents/com.diane.sync.plist
```

### 4. Set Up GPG (Optional)

```bash
# Generate GPG key if needed
gpg --gen-key

# Configure diane
diane, --gpg-setup

# Set in environment
echo 'export DIANE_GPG_KEY="your-key-id"' >> ~/.bashrc
```

### 5. Configure Vim (Optional)

```bash
# Install vim plugin
cp scripts/editors/diane.vim ~/.vim/plugin/

# Or add to .vimrc with vim-plug
echo "Plug '~/diane/scripts/editors/diane.vim'" >> ~/.vimrc
```

### 6. Test Everything

```bash
# Quick capture
d, "testing ultra-fast capture"

# Clipboard capture
echo "test" | xclip -selection clipboard
d,c

# Search
d,f test

# Stats
d,st

# Verify sync is running
systemctl --user status diane-sync  # Linux
launchctl list | grep diane         # macOS
```

---

## 📱 Workflow Examples

### Morning Routine

```bash
# Start day - check what's new
dtoday

# See stats
d,st

# Check sync status
d,status
```

### Throughout the Day

```bash
# Ultra-fast captures
d, "idea for new feature"
d, "meeting note: client wants API"
d,t work "follow up with design team"

# Clipboard capture interesting things
# (Ctrl+Alt+C or just: dc)
```

### Evening Review

```bash
# View today's records
dtoday

# Export for processing
dhtml --export-file ~/daily-review.html
open ~/daily-review.html

# Stats check
d,st
```

### Weekly Review

```bash
# Get last week of records
diane, --list --limit 100 > weekly.txt

# Export for analysis
djson --export-file weekly.json

# Stats overview
d,st
```

---

## 🎯 Efficiency Metrics

With this setup, you've achieved:

| Action | Before | After | Improvement |
|--------|--------|-------|-------------|
| Basic capture | `diane, "text"` (10 chars) | `d "text"` (2 chars) | **80% faster** |
| Clipboard capture | `pbpaste \| diane,` (17 chars) | `dc` (2 chars) | **88% faster** |
| Tagged capture | `diane, --tags work "text"` | `dt work "text"` | **50% faster** |
| List records | `diane, --list` | `dl` | **80% faster** |
| Search | `diane, --search` | `df` | **75% faster** |
| Sync | `diane, --sync` | `dsync` | **60% faster** |
| Access from vim | Manual command | `<leader>dc` | **Instant** |
| Background sync | Manual | **Automatic** | **100% automated** |

---

## 🔒 Privacy & Security

Even with seamless access, your data stays secure:

- ✅ All records stored locally first
- ✅ Encrypted git sync (SSH/HTTPS)
- ✅ Optional GPG encryption for sensitive records
- ✅ No telemetry or external services
- ✅ You control the remote (private GitHub repo)
- ✅ Background sync only if you enable it

---

## 🎵 The Ultimate diane, Experience

After this setup, diane, becomes:

1. **Invisible** - Background sync, silent captures, no interruptions
2. **Instant** - 2-3 character commands, global hotkeys, editor integration
3. **Everywhere** - Terminal, vim, clipboard, selection, any application
4. **Reliable** - Auto-sync, Git versioning, encrypted backups
5. **Efficient** - Tab completion, smart shortcuts, fuzzy search

You've transformed diane, from a CLI tool into a **transparent extension of your mind**.

---

*"Always listening, never interrupting, never forgetting."* — Diane's Law

**Now go capture everything, effortlessly.** 🎉
