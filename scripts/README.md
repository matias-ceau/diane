# diane, Scripts & Integrations

This directory contains scripts, integrations, and tools to make diane, seamless and available everywhere.

## 📁 Directory Structure

```
scripts/
├── completions/              # Shell completions
│   ├── diane.bash-completion
│   ├── diane.zsh-completion
│   └── diane.fish-completion
├── editors/                  # Editor integrations
│   ├── diane.vim
│   └── diane-vscode.js
├── systemd/                  # Linux service files
│   └── diane-sync.service
├── launchd/                  # macOS service files
│   └── com.diane.sync.plist
├── diane-daemon.py          # Background sync daemon
├── clipboard-monitor.py     # Clipboard monitoring tool
├── quick-capture.sh         # Ultra-fast capture shortcuts
└── install.sh               # One-line installer

```

## 🚀 Quick Start

### One-Line Install

```bash
curl -sSL https://raw.githubusercontent.com/USER/diane/main/scripts/install.sh | bash
```

This installs:
- ✅ diane, CLI tool
- ✅ Shell completions
- ✅ Quick capture shortcuts
- ✅ PATH configuration

### Manual Setup

```bash
# 1. Install completions
source completions/diane.bash-completion  # bash
source completions/diane.zsh-completion   # zsh
cp completions/diane.fish-completion ~/.config/fish/completions/  # fish

# 2. Install shortcuts
source quick-capture.sh

# 3. Install daemon (optional)
sudo cp diane-daemon.py /usr/local/bin/
chmod +x /usr/local/bin/diane-daemon.py

# 4. Setup auto-sync (Linux)
systemctl --user enable diane-sync
systemctl --user start diane-sync
```

## 📋 Shell Completions

Tab completion for all diane commands in bash, zsh, and fish.

**Features:**
- Command completion
- Option completion
- Tag suggestions from existing records
- File path completion for exports

**Install:**
See `completions/` directory READMEs.

## ⚡ Quick Capture Shortcuts

Ultra-minimal aliases for instant capture:

```bash
d "text"          # 2-char capture!
dc                # capture clipboard
dt work "note"    # tagged capture
dl                # list records
df keyword        # fuzzy search
dst               # show stats
dsync             # sync now
```

**Install:**
```bash
source quick-capture.sh
# Add to ~/.bashrc or ~/.zshrc
```

## 🔄 Background Sync Daemon

Automatically sync records to remote repository.

**Features:**
- Configurable interval (default: 5 minutes)
- Silent operation
- Logging to file
- Systemd/launchd integration

**Usage:**
```bash
# Manual
diane-daemon.py --interval 300

# As service (Linux)
systemctl --user start diane-sync

# As service (macOS)
launchctl load ~/Library/LaunchAgents/com.diane.sync.plist
```

## 📋 Clipboard Monitor

Watch clipboard and auto-capture interesting content.

**Features:**
- Auto-capture mode
- Regex filtering
- Minimum length filtering
- Custom tagging

**Usage:**
```bash
# Manual mode - prompt for each change
clipboard-monitor.py

# Auto-capture everything
clipboard-monitor.py --auto-capture

# Only URLs
clipboard-monitor.py --auto-capture --filter 'https?://' --tag bookmarks

# Only long text (100+ chars)
clipboard-monitor.py --auto-capture --min-length 100
```

## 🎨 Editor Integrations

### Vim Plugin

**Features:**
- Capture buffer: `:DianeCapture`
- Capture selection: `:DianeCaptureSelection`
- Quick capture: `:DianeQuick`
- Search records: `:DianeSearch keyword`
- Key mappings: `<leader>dc`, `<leader>ds`, etc.

**Install:**
```bash
cp editors/diane.vim ~/.vim/plugin/
# Or with vim-plug:
Plug '/path/to/diane/scripts/editors/diane.vim'
```

### VS Code Extension

**Template provided** - ready for development into full extension.

**Features (planned):**
- Capture document
- Capture selection
- Quick capture dialog
- Search interface
- Statistics view
- Status bar integration

## 🔧 System Services

### Linux (systemd)

Autostart background sync on login.

**Install:**
```bash
sudo cp diane-daemon.py /usr/local/bin/
chmod +x /usr/local/bin/diane-daemon.py
cp systemd/diane-sync.service ~/.config/systemd/user/
systemctl --user enable diane-sync
systemctl --user start diane-sync
```

**Check status:**
```bash
systemctl --user status diane-sync
journalctl --user -u diane-sync -f
```

### macOS (launchd)

Autostart background sync on login.

**Install:**
```bash
sudo cp diane-daemon.py /usr/local/bin/
chmod +x /usr/local/bin/diane-daemon.py
cp launchd/com.diane.sync.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.diane.sync.plist
```

**Check status:**
```bash
launchctl list | grep diane
tail -f /tmp/diane-daemon.log
```

## 🎯 Recommended Setup

For the ultimate seamless experience:

1. **Install completions** - Tab completion everywhere
2. **Source quick-capture.sh** - Ultra-fast shortcuts
3. **Enable background sync** - Never manually sync again
4. **Install vim plugin** - Capture from your editor
5. **Configure clipboard monitor** - Auto-capture interesting clips

See [SEAMLESS.md](../SEAMLESS.md) for detailed setup guide.

## 🔐 Security Considerations

- **Daemon**: Runs as your user, no elevated privileges needed
- **Clipboard monitor**: Only reads clipboard, never writes
- **Editor plugins**: Execute diane commands with your permissions
- **Services**: User-level services (systemd --user, ~/Library/LaunchAgents)

## 🐛 Troubleshooting

### Completions not working

```bash
# Bash
source ~/.bash_completion.d/diane

# Zsh
autoload -Uz compinit && compinit

# Fish
fish_update_completions
```

### Daemon not starting

```bash
# Check logs
journalctl --user -u diane-sync -n 50  # Linux
tail -f /tmp/diane-daemon.log          # macOS

# Test manually
/usr/local/bin/diane-daemon.py --interval 10

# Check diane is in PATH
which diane,
```

### Vim plugin not loading

```bash
# Check plugin directory
ls ~/.vim/plugin/diane.vim

# Test command
:DianeCapture

# Check for errors
:messages
```

## 📚 More Documentation

- [SEAMLESS.md](../SEAMLESS.md) - Complete seamless setup guide
- [INSTALL.md](../INSTALL.md) - Installation instructions
- [FEATURES.md](../FEATURES.md) - All features and usage
- [README.md](../README.md) - Project overview

## 🤝 Contributing

Found a bug? Have an integration idea?

- Report issues on GitHub
- Submit PRs for new integrations
- Share your custom scripts!

---

*Make diane, invisible, instant, and everywhere.* ⚡
