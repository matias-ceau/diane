# Changelog

All notable changes to the **diane** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-11-07

### 🎯 Major Refactor — Simplified & Unix-Friendly

This release represents a major refactor toward Unix philosophy and simplicity.

### Added

#### ✨ New Features
- **Default behavior shows records** — `diane` with no arguments now shows latest records (no more `--list` needed)
- **Pipe-friendly output** — Clean `timestamp|content` format when output is piped (Unix composability)
- **Rich help menus** — Beautiful, colorful help powered by `rich-click`
- **First-run setup wizard** — `diane --setup` guides initial configuration
- **Info command** — `diane --info` or `diane --path` shows configuration and paths
- **Comma easter egg** — `diane , "text"` works like `diane -- "text"` (Twin Peaks tribute)
- **Simple confirmations** — Default `✓` confirmation, detailed output with `--verbose`

#### 🔍 Enhanced Search
- **ripgrep + fzf integration** — Interactive search with live preview (replaces custom fuzzy search)
- Requires `rg` and `fzf` installed, provides much better search experience

### Changed

#### 🎨 Breaking Changes
- **Removed tags** — Simplified capture, no more `--tags` option or tag metadata
- **Removed local encryption** — No more `--encrypt` flag (encryption moved to future remote-sync layer)
- **Removed `-s` short flag** — Only `--search` (avoid conflicts with other CLI tools)
- **Changed default behavior** — `diane` now shows records instead of waiting for input
- **Removed `diane,` command** — Only `diane` command (comma is easter egg only)

#### ⚡ Improvements
- **Faster, cleaner output** — No decorative elements when piped to other tools
- **Better Unix integration** — `diane | wc -l` counts actual records, not UI elements
- **Simpler data model** — Records only have timestamp, sources, and content
- **Cleaner help** — Organized, colorful help menu with better descriptions

### Removed

- Tag functionality (`--tags`, tag display, tag statistics)
- Local GPG encryption (`--encrypt`, `--decrypt`, `--gpg-*` commands)
- Custom fuzzy search (replaced by ripgrep + fzf)
- `-s` short flag for search
- `--list` flag (default behavior now)
- `diane,` command alias

### Dependencies

- **Added**: `rich-click >= 1.7` for beautiful help menus
- **Removed**: Direct `rich` dependency (included via rich-click)

### Documentation

- **Completely rewritten README.md** — Focused on Unix philosophy and simplicity
- **New ROADMAP.md** — Vision for AI-powered processing layer (Layer 2)
- **Updated CHANGELOG.md** — This file

### Philosophy

This release refocuses **diane** on its core purpose:

> "Do one thing well: capture and retrieve thoughts"

The tool now follows Unix principles strictly:
- Clean, parseable output when piped
- Silent unless needed
- Composes with other CLI tools
- Plain text, no lock-in

### Upgrade Notes

**Breaking changes from v0.2.0:**

1. **Tags removed** — Old records with tags will still work (tags in frontmatter are ignored)
2. **Encrypted files** — Any `.gpg` files won't be read automatically (decrypt manually if needed)
3. **Command changes**:
   - `diane, --list` → `diane`
   - `diane, --search query` → `diane --search query`
   - `diane, --tags work "note"` → `diane "note"` (tags not supported)

**Migration:**
```bash
# Old way
diane, --list --today
diane, --tags work "my note"

# New way
diane --today
diane "my note"
```

---

## [0.2.0] - 2025-11-06

### Added

#### 🔐 GPG Encryption
- Full GPG encryption support for records
- `--encrypt` flag to encrypt records when saving
- `--gpg-list-keys` to list available GPG keys
- `--gpg-setup` for interactive key configuration
- `--decrypt` to decrypt encrypted record files
- Automatic encryption using `DIANE_GPG_KEY` environment variable

#### 📤 Export Functionality
- Export records to multiple formats: JSON, CSV, HTML, Markdown
- `--export <format>` flag with format selection
- `--export-file <path>` to save exports to file
- Beautiful HTML export with styling
- Works with `--today` flag to export filtered records
- Perfect for integration with other tools and agents

#### 📊 Statistics & Analytics
- `--stats` command for comprehensive record analytics
- Total record and word counts
- Average words per record
- Tag usage statistics
- Busiest day detection
- Recent activity visualization (last 7 days)
- Top tags ranking

### Enhanced
- Better error messages for GPG operations
- Improved export formatting and styling
- Enhanced CLI help text with new commands

### Technical
- New `diane/encryption.py` module for GPG operations
- New `diane/export.py` module for export functionality
- New `diane/stats.py` module for analytics
- Version bump to 0.2.0

---

## [0.1.0] - 2025-11-06

### Added

#### Core Features
- Silent-by-default recording from stdin, pipes, or interactive mode
- YAML frontmatter with timestamps and tags
- Automatic Git versioning of all records
- Plain-text Markdown storage in `~/.local/share/diane/records/`
- Tag-based organization with hierarchical tags
- Exact and fuzzy search capabilities
- List and filter records by date

#### 🔍 Fuzzy Search
- Approximate string matching with similarity scores
- `--fuzzy` flag for fuzzy search mode
- Similarity percentage display (e.g., 🎯 80%)
- Great for typos and partial matches

#### 🌐 Git Sync & Remote Backup
- Full Git remote operations (push/pull/sync)
- `--set-remote` to configure GitHub/GitLab repository
- `--push` to backup records to remote
- `--pull` to fetch records from remote
- `--sync` for full bidirectional sync
- `--remote-status` to check sync state
- Multi-device support

#### 🖥️ TUI Dashboard
- Interactive terminal UI using Textual framework
- `--tui` flag to launch dashboard
- Browsable record list with timestamps and tags
- Full record detail view
- Keyboard navigation (j/k, arrows)
- Vim-style keybindings
- Optional dependency: `pip install "diane-cli[tui]"`

#### CLI & Configuration
- Click-based CLI with comprehensive options
- Silent operation by default (true to Diane's character)
- `--verbose` / `-v` flag for confirmations
- Environment variables for configuration
- Shell alias support

#### Storage & Git Integration
- Automatic Git repository initialization
- Auto-commit on every record save
- Git config to disable GPG signing conflicts
- Plain-text Markdown files for portability
- YAML frontmatter for structured metadata

### Documentation
- Comprehensive README.md with project vision
- Detailed INSTALL.md with setup instructions
- FEATURES.md guide with use cases
- MIT License
- Test suite with pytest

### Technical
- Python 3.8+ support
- Click >= 8.0 for CLI
- PyYAML >= 6.0 for frontmatter
- python-dateutil >= 2.8 for date handling
- Optional: textual >= 0.40.0 for TUI
- Package structure with setuptools
- Both `diane` and `diane,` command aliases

---

## [Unreleased]

### Planned Features
- 🎤 Audio capture with speech-to-text integration
- 🔌 REST API for agent integration
- 🧠 Semantic search using embeddings
- 🔑 Advanced encryption key management UI
- 📱 Mobile companion app
- 🔗 Integration plugins for common tools
- 📈 Advanced analytics and insights

---

**Legend:**
- ✨ New feature
- 🐛 Bug fix
- 🔒 Security
- 📚 Documentation
- ⚡ Performance
- 🎨 UI/UX improvement
