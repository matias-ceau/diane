# Installation Guide for diane,

## Prerequisites

- Python 3.8 or higher
- Git (optional, for automatic record versioning)
- GPG (optional, for encryption support)

## Installation

### Method 1: Install from source (Development)

```bash
# Clone the repository
git clone https://github.com/matias-ceau/diane.git
cd diane

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .
```

### Method 2: Install with pip (once published)

```bash
pip install diane-cli
```

## Configuration

diane, works out of the box with sensible defaults. Records are stored in:
```
~/.local/share/diane/records/
```

### Environment Variables

You can customize diane's behavior with these environment variables:

```bash
# Set custom data directory
export DIANE_DATA_HOME="$HOME/Documents/diane"

# Set GPG key for encryption (optional)
export DIANE_GPG_KEY="your-gpg-key-id"
```

Add these to your `~/.bashrc`, `~/.zshrc`, or equivalent shell configuration file.

## Usage

### Basic Recording

```bash
# Interactive mode - type and press Ctrl-D to finish
diane,

# Record text directly
diane, "This is my thought for the day"

# Pipe from echo
echo "Remember to review the meeting notes" | diane,

# Pipe from a file
cat notes.txt | diane,
```

### Using Tags

```bash
# Single tag
diane, --tags work "Meeting with client went well"

# Multiple tags (comma-separated)
diane, --tags work/urgent,projects/acme "Need to follow up on proposal"
```

### Listing Records

```bash
# List 10 most recent records (default)
diane, --list

# List today's records only
diane, --list --today

# List more records
diane, --list --limit 20
```

### Searching Records

```bash
# Search for keyword
diane, --search "meeting"

# Search with limited results
diane, --search "client" --limit 5
```

### Verbose Mode

By default, diane, is silent (true to her character). Use `--verbose` or `-v` for confirmations:

```bash
echo "Test entry" | diane, -v
# Output: ✅ Recorded: 2024-11-06--13-30-45--test-entry.md
```

### Encryption (Planned)

```bash
# Encrypt a record with GPG
diane, --encrypt "Sensitive information here"
```

*Note: Full GPG encryption support is planned for a future release.*

## Shell Aliases

For even more convenience, add these to your shell configuration:

```bash
# Quick dictation
alias d="diane,"

# Verbose variant
alias dv="diane, -v"

# Search records
alias ds="diane, --search"

# List today's records
alias dt="diane, --list --today"
```

Then use:
```bash
echo "Quick note" | d
ds "keyword"
dt
```

## Viewing Your Records

Records are stored as plain Markdown files with YAML frontmatter. You can view them with any text editor:

```bash
# Navigate to records directory
cd ~/.local/share/diane/records

# List records
ls -lt

# View a record
cat 2024-11-06--13-30-45--meeting-insights.md
```

Example record format:
```markdown
---
timestamp: 2024-11-06 13:30
tags: [work/clients/acme]
sources: [stdin]
---

Meeting insights from today's call with client...
```

## Git Integration

If Git is available, diane, automatically:
- Initializes a Git repository in the records directory
- Commits each new record automatically
- Maintains a complete history of your thoughts

You can use standard Git commands in the records directory:
```bash
cd ~/.local/share/diane/records
git log
git show HEAD
```

## Troubleshooting

### Command not found: diane,

Make sure your Python scripts directory is in your PATH:
```bash
# For Linux/macOS
export PATH="$HOME/.local/bin:$PATH"

# For Windows (add to Environment Variables)
# Add: %APPDATA%\Python\Python3x\Scripts
```

### Permission denied

Ensure the diane data directory is writable:
```bash
mkdir -p ~/.local/share/diane
chmod 755 ~/.local/share/diane
```

### Git not initializing

Check if Git is installed and available:
```bash
git --version
```

diane, will work fine without Git, it just won't auto-version your records.

## Uninstallation

```bash
# Uninstall the package
pip uninstall diane-cli

# Optionally remove your records (⚠️ this deletes all your data!)
rm -rf ~/.local/share/diane
```

## Next Steps

- Explore your records directory to understand the storage format
- Set up shell aliases for quick access
- Configure environment variables for your preferred setup
- Check the README.md for the full vision and roadmap

---

*"Always listening, never interrupting, never forgetting."* — Diane's Law
