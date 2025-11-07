# Changelog

All notable changes to the **diane,** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
