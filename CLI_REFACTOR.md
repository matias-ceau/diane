# CLI Refactor Proposal — Command-Based Structure

## Current Issues

- Too many flat flags (`--record`, `--search`, `--tui`, `--sync`, etc.)
- Unclear that these are distinct operations, not just options
- Hard to discover features
- Not scalable as features grow

## Proposed Structure

### Quick Capture (Keep Simple)

```bash
# Text capture (most common - keep ultra-fast)
diane [TEXT]                    # Direct argument
echo "text" | diane             # Pipe
diane                           # Show latest (default when no input)
```

### Viewing & Review

```bash
diane show                      # Show latest records
diane show --limit 20           # Show more
diane show --today              # Today only
diane show --since 2025-11-01   # Date range

# Alias for convenience
diane list                      # Same as 'show'
```

### Audio Recording

```bash
diane record                    # Record until Ctrl-C
diane record --duration 30      # Record 30 seconds
diane record --file audio.mp3   # Transcribe file
diane record --list-devices     # Show microphones

# Short form
diane rec                       # Alias for 'record'
```

### Search & Browse

```bash
diane search [QUERY]            # Interactive search (ripgrep+fzf)
diane search "meeting"          # Search for "meeting"

diane tui                       # Terminal UI dashboard
```

### Sync Operations

```bash
diane sync                      # Full sync (pull + push)
diane sync push                 # Push only
diane sync pull                 # Pull only
diane sync status               # Show git status

diane sync remote [URL]         # Set remote URL
diane sync remote               # Show current remote

# Short forms
diane push                      # Alias for 'sync push'
diane pull                      # Alias for 'sync pull'
```

### Export & Statistics

```bash
diane export json               # Export to JSON
diane export csv --file out.csv # Export to CSV file
diane export html               # Export to HTML
diane export markdown           # Export to Markdown

diane stats                     # Show statistics
diane stats --days 30           # Last 30 days
```

### Setup & Info

```bash
diane setup                     # First-time setup wizard
diane info                      # Show configuration
diane info --paths              # Show paths only
```

## Implementation Plan

### Phase 1: Core Refactor

1. Convert to `@click.group()` structure
2. Implement default behavior (text capture / show)
3. Create subcommands: `show`, `record`, `search`, `tui`

### Phase 2: Sync Refactor

4. Create `sync` group with subcommands
5. Add aliases for common operations (`push`, `pull`)

### Phase 3: Polish

6. Add `export` and `stats` commands
7. Update all help text
8. Add examples to each command

## Backward Compatibility

Keep these working (at least for one version):
- `diane --record` → Deprecation warning → `Use 'diane record' instead`
- `diane --search X` → Redirect to `diane search X`
- `diane --tui` → Redirect to `diane tui`

## Help Output

```bash
$ diane --help

Usage: diane [OPTIONS] [TEXT] [COMMAND]...

  diane - Minimalist thought capture CLI

Quick capture:
  diane [TEXT]          Capture text
  echo "text" | diane   Pipe text
  diane                 Show latest records

Commands:
  show      View records
  record    Record and transcribe audio
  search    Search records interactively
  tui       Terminal UI dashboard

  sync      Git sync operations
  export    Export records to various formats
  stats     Show statistics

  setup     First-time setup wizard
  info      Show configuration

Options:
  --help    Show this message and exit

Examples:
  diane "quick thought"
  diane show --today
  diane record --duration 30
  diane search "meeting"
  diane sync push
```

## Benefits

1. **Clearer intent** — `diane record` vs `diane --record`
2. **Better organization** — Related operations grouped
3. **Discoverable** — `diane --help` shows commands clearly
4. **Scalable** — Easy to add new commands
5. **Standard** — Matches modern CLI patterns (uv, docker, git)

## Next Steps

1. Implement new `cli.py` with Click groups
2. Test all commands
3. Update documentation
4. Add deprecation warnings for old flags
5. Release as v0.4.0 (breaking changes justified by improvement)
