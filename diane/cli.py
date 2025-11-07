"""Command-line interface for diane."""

import sys
from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path

# Easter egg: replace comma with -- (Twin Peaks tribute)
# Usage: diane , "some text" == diane -- "some text"
if len(sys.argv) > 1 and sys.argv[1] == ',':
    sys.argv[1] = '--'

import rich_click as click

# Configure rich-click for beautiful help
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.USE_MARKDOWN = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.STYLE_ERRORS_SUGGESTION = "yellow italic"
click.rich_click.SHOW_METAVARS_COLUMN = False
click.rich_click.APPEND_METAVARS_HELP = True

from .config import config
from .record import Record
from .storage import Storage
from .sync import GitSync


@click.group(invoke_without_command=True)
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
@click.pass_context
def cli(ctx, verbose):
    """diane - Minimalist thought capture CLI

    \b
    Quick capture:
      diane <<< "text"          Here-string
      echo "text" | diane       Pipe
      diane << EOF              Heredoc (multiline)
      diane                     Show latest records

    \b
    Commands:
      show      View records
      record    Audio dictation
      search    Interactive search
      tui       Terminal UI
      sync      Git operations
      export    Export records
      stats     Statistics
      setup     First-time setup
      info      Show configuration
    """
    if verbose:
        config.verbose = True

    # If no command specified, handle stdin or show records
    if ctx.invoked_subcommand is None:
        if not sys.stdin.isatty():
            # Input from pipe/redirect/heredoc
            content = sys.stdin.read()
            if content and content.strip():
                _capture_text(content, verbose)
            else:
                # Empty stdin - show records
                _show_records(limit=10, today=False, since=None, verbose=verbose)
        else:
            # Interactive terminal, no command - show records
            _show_records(limit=10, today=False, since=None, verbose=verbose)


@cli.command()
@click.option('--limit', '-n', type=int, default=10, help='Number of records to show')
@click.option('--today', is_flag=True, help='Show only today\'s records')
@click.option('--since', help='Show records since date (YYYY-MM-DD)')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
def show(limit, today, since, verbose):
    """View recent records"""
    if verbose:
        config.verbose = True

    since_date = None
    if today:
        since_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    elif since:
        try:
            since_date = datetime.strptime(since, '%Y-%m-%d')
        except ValueError:
            click.echo(f"❌ Invalid date format: {since}. Use YYYY-MM-DD", err=True)
            sys.exit(1)

    _show_records(limit=limit, today=today, since=since_date, verbose=verbose)


@cli.command()
@click.option('--duration', '-d', type=int, help='Recording duration in seconds')
@click.option('--file', '-f', 'audio_file', type=click.Path(exists=True), help='Transcribe audio file')
@click.option('--list-devices', is_flag=True, help='List available microphones')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
def record(duration, audio_file, list_devices, verbose):
    """Record and transcribe audio"""
    if verbose:
        config.verbose = True

    if list_devices:
        _list_microphones()
        return

    if audio_file:
        _transcribe_audio_file(audio_file, verbose)
    else:
        _record_and_transcribe(duration, verbose)


@cli.command()
@click.argument('query', required=False)
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
def search(query, verbose):
    """Search records interactively (requires ripgrep + fzf)

    If no query provided, opens fzf to browse all records.
    """
    if verbose:
        config.verbose = True

    _interactive_search(query or "")


@cli.command()
def tui():
    """Launch terminal UI dashboard"""
    try:
        from .tui import launch_tui
        launch_tui()
    except ImportError:
        click.echo("❌ TUI not available. Install with: pip install diane-cli[tui]", err=True)
        sys.exit(1)


@cli.group()
def sync():
    """Git sync operations"""
    pass


@sync.command('push')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
def sync_push(verbose):
    """Push records to remote"""
    if verbose:
        config.verbose = True

    git_sync = GitSync()

    if verbose:
        click.echo("Pushing to remote...")

    success, msg = git_sync.push()
    if success:
        click.echo(f"✅ {msg}" if verbose else "✓")
    else:
        click.echo(f"❌ {msg}", err=True)
        sys.exit(1)


@sync.command('pull')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
def sync_pull(verbose):
    """Pull records from remote"""
    if verbose:
        config.verbose = True

    git_sync = GitSync()

    if verbose:
        click.echo("Pulling from remote...")

    success, msg = git_sync.pull()
    if success:
        click.echo(f"✅ {msg}" if verbose else "✓")
    else:
        click.echo(f"❌ {msg}", err=True)
        sys.exit(1)


@sync.command('status')
def sync_status():
    """Show git sync status"""
    git_sync = GitSync()
    status = git_sync.status()

    if not status['is_repo']:
        click.echo("❌ Not a git repository")
        return

    click.echo("📡 Sync Status")
    click.echo("─" * 60)
    click.echo(f"Branch: {status['branch'] or 'unknown'}")
    click.echo(f"Remote: {status['remote_url'] or 'none configured'}")

    if status['has_remote']:
        if status['ahead'] > 0:
            click.echo(f"↑ Ahead by {status['ahead']} commit(s)")
        if status['behind'] > 0:
            click.echo(f"↓ Behind by {status['behind']} commit(s)")
        if status['ahead'] == 0 and status['behind'] == 0:
            click.echo("✅ Up to date")

    if status['has_changes']:
        click.echo("⚠ Uncommitted changes")


@sync.command('remote')
@click.argument('url', required=False)
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
def sync_remote(url, verbose):
    """Set or show git remote URL"""
    if verbose:
        config.verbose = True

    git_sync = GitSync()

    if url:
        # Set remote
        success, msg = git_sync.set_remote(url)
        if success:
            click.echo(f"✅ {msg}" if verbose else "✓")
        else:
            click.echo(f"❌ {msg}", err=True)
            sys.exit(1)
    else:
        # Show current remote
        current = git_sync.get_remote_url()
        if current:
            click.echo(current)
        else:
            click.echo("No remote configured")


# Convenience aliases at top level
@cli.command('push', hidden=True)
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
@click.pass_context
def push_alias(ctx, verbose):
    """Alias for 'diane sync push'"""
    ctx.invoke(sync_push, verbose=verbose)


@cli.command('pull', hidden=True)
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
@click.pass_context
def pull_alias(ctx, verbose):
    """Alias for 'diane sync pull'"""
    ctx.invoke(sync_pull, verbose=verbose)


@cli.command()
@click.argument('format', type=click.Choice(['json', 'csv', 'html', 'markdown']))
@click.option('--file', '-f', 'output_file', help='Output file (default: stdout)')
@click.option('--today', is_flag=True, help='Export only today\'s records')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
def export(format, output_file, today, verbose):
    """Export records to various formats"""
    if verbose:
        config.verbose = True

    from .export import Exporter

    storage = Storage()

    since = None
    if today:
        since = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    results = storage.list_records(limit=None, since=since)

    if not results:
        click.echo("No records to export")
        return

    # Generate export
    if format == 'json':
        content = Exporter.to_json(results)
    elif format == 'csv':
        content = Exporter.to_csv(results)
    elif format == 'html':
        content = Exporter.to_html(results)
    elif format == 'markdown':
        content = Exporter.to_markdown(results)

    # Output
    if output_file:
        Exporter.save_export(content, Path(output_file))
        if verbose:
            click.echo(f"✅ Exported {len(results)} records to {output_file}")
        else:
            click.echo("✓")
    else:
        click.echo(content)


@cli.command()
@click.option('--days', type=int, default=7, help='Number of days for recent activity')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
def stats(days, verbose):
    """Show statistics about your records"""
    if verbose:
        config.verbose = True

    from .stats import Statistics

    storage = Storage()
    records = storage.list_records(limit=None)

    if not records:
        click.echo("No records found")
        return

    statistics = Statistics(records)
    summary = statistics.summary()

    click.echo("📊 Record Statistics")
    click.echo("─" * 60)
    click.echo(f"Total Records: {summary['total_records']}")
    click.echo(f"Total Words: {summary['total_words']}")
    click.echo(f"Avg Words/Record: {summary['avg_words_per_record']}")
    click.echo()

    if summary['busiest_day']:
        click.echo(f"Busiest Day: {summary['busiest_day']} ({summary['busiest_day_count']} records)")
        click.echo()

    # Show recent activity
    recent = statistics.recent_activity(days=days)
    if recent:
        click.echo(f"Last {days} Days:")
        for date_str, count in recent.items():
            bar = '█' * count
            click.echo(f"  {date_str}: {bar} {count}")


@cli.command()
def setup():
    """Run first-time setup wizard"""
    _run_setup_wizard()


@cli.command()
@click.option('--paths', is_flag=True, help='Show only paths')
def info(paths):
    """Show configuration and paths"""
    if paths:
        click.echo(config.get_records_dir())
        return

    _show_info()


# Helper functions

def _capture_text(content: str, verbose: bool):
    """Capture text and save as record"""
    storage = Storage()

    record = Record(
        content=content,
        sources=["stdin"],
    )

    filepath = storage.save(record)

    if verbose:
        click.echo(f"✅ Recorded: {filepath.name}")
    else:
        click.echo("✓")


def _show_records(limit: int, today: bool, since: Optional[datetime], verbose: bool):
    """Display records"""
    storage = Storage()

    since_date = since
    if today:
        since_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    results = storage.list_records(limit=limit, since=since_date)

    if not results:
        if verbose:
            click.echo("No records found")
        return

    for record in results:
        _display_record(record)


def _display_record(record: Record):
    """Display a record in a readable format"""
    # Unix philosophy: clean output when piped, pretty when interactive
    is_tty = sys.stdout.isatty()

    if is_tty:
        # Pretty formatting for terminal
        click.echo("─" * 60)
        timestamp = record.timestamp.strftime('%Y-%m-%d %H:%M')
        click.echo(f"📅 {timestamp}")
        click.echo()
        click.echo(record.content)
        click.echo()
    else:
        # Clean output for pipes
        timestamp = record.timestamp.strftime('%Y-%m-%d %H:%M')
        clean_content = record.content.replace('\n', ' ')
        click.echo(f"{timestamp}|{clean_content}")


def _show_info():
    """Show configuration and paths information"""
    click.echo("📍 diane Configuration")
    click.echo("─" * 60)
    click.echo(f"Records Directory: {config.get_records_dir()}")
    click.echo(f"Data Home:         {config.data_home}")
    click.echo(f"Git Enabled:       {config.use_git}")
    click.echo(f"Auto-sync:         {config.auto_sync}")
    click.echo()

    # Show git remote if configured
    try:
        git_sync = GitSync()
        remote_url = git_sync.get_remote_url()
        if remote_url:
            click.echo(f"Git Remote:        {remote_url}")
        else:
            click.echo("Git Remote:        (not configured)")
    except Exception:
        pass

    click.echo()
    click.echo("Run 'diane setup' to configure diane")


def _run_setup_wizard():
    """Run first-time setup wizard"""
    click.echo("╔════════════════════════════════════════════════════════════╗")
    click.echo("║           diane Setup Wizard                              ║")
    click.echo("╚════════════════════════════════════════════════════════════╝")
    click.echo()

    # Show what will be created
    records_dir = config.get_records_dir()
    click.echo("diane will create the following structure:")
    click.echo()
    click.echo(f"  📁 {records_dir}/")
    click.echo("     └── Your records will be stored here as .md files")
    click.echo()
    click.echo("  📁 Each record contains:")
    click.echo("     • Timestamp")
    click.echo("     • Content (your thoughts/notes)")
    click.echo("     • Git version history (automatic)")
    click.echo()

    # Create directories
    config.ensure_directories()
    storage = Storage()

    click.echo("✅ Directories created")
    click.echo()

    # Ask about remote sync
    if click.confirm("Would you like to set up remote sync (e.g., GitHub, GitLab)?"):
        click.echo()
        click.echo("Remote sync allows you to:")
        click.echo("  • Backup your records to a remote git repository")
        click.echo("  • Sync across multiple devices")
        click.echo("  • Have encrypted backups in the cloud")
        click.echo()

        remote_url = click.prompt("Enter git remote URL (e.g., git@github.com:user/diane-records.git)")

        git_sync = GitSync()
        success, msg = git_sync.set_remote(remote_url)

        if success:
            click.echo(f"✅ {msg}")
            click.echo()

            # Ask about initial push
            if click.confirm("Push any existing records to remote now?"):
                click.echo("Pushing...")
                success, msg = git_sync.push()
                if success:
                    click.echo(f"✅ {msg}")
                else:
                    click.echo(f"⚠ {msg}")
        else:
            click.echo(f"❌ {msg}")

    click.echo()
    click.echo("╔════════════════════════════════════════════════════════════╗")
    click.echo("║  Setup Complete!                                          ║")
    click.echo("╚════════════════════════════════════════════════════════════╝")
    click.echo()
    click.echo("Quick start:")
    click.echo("  • diane <<< \"thought\"         # Quick capture")
    click.echo("  • diane                       # Show latest")
    click.echo("  • diane search \"query\"        # Search")
    click.echo("  • diane sync push             # Sync to remote")
    click.echo("  • diane info                  # Show config")
    click.echo()


def _interactive_search(query: str):
    """Launch interactive search using ripgrep + fzf"""
    import subprocess

    records_dir = config.get_records_dir()

    # Check if rg and fzf are available
    try:
        subprocess.run(['which', 'rg'], capture_output=True, check=True)
        subprocess.run(['which', 'fzf'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        click.echo("❌ This feature requires 'ripgrep' and 'fzf' to be installed.", err=True)
        click.echo("   Install with: brew install ripgrep fzf  (macOS)", err=True)
        click.echo("              or: apt install ripgrep fzf   (Ubuntu/Debian)", err=True)
        sys.exit(1)

    # Build the ripgrep + fzf pipeline
    try:
        # First run ripgrep to find matches
        if query:
            rg_result = subprocess.run(
                ['rg', '--color=always', '--line-number', '--no-heading', '--smart-case', query],
                cwd=records_dir,
                capture_output=True,
                text=True
            )

            if not rg_result.stdout:
                click.echo("No matches found")
                return

            initial_input = rg_result.stdout
        else:
            # No query - browse all files
            rg_result = subprocess.run(
                ['rg', '--color=always', '--line-number', '--no-heading', '.'],
                cwd=records_dir,
                capture_output=True,
                text=True
            )
            initial_input = rg_result.stdout

        # Pipe to fzf for interactive selection
        fzf_process = subprocess.Popen(
            [
                'fzf',
                '--ansi',
                '--color', 'hl:-1:underline,hl+:-1:underline:reverse',
                '--delimiter', ':',
                '--preview', f'bat --color=always --style=plain {{1}} || cat {{1}}',
                '--preview-window', 'up,60%,border-bottom,+{{2}}+3/3,~3'
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = fzf_process.communicate(input=initial_input)

        if fzf_process.returncode == 0 and stdout:
            # User selected a file, extract filename and display
            parts = stdout.strip().split(':', 1)
            if parts:
                filename = parts[0]
                filepath = records_dir / filename
                if filepath.exists():
                    record = Record.from_file(filepath)
                    _display_record(record)

    except KeyboardInterrupt:
        click.echo("\nSearch cancelled")
    except Exception as e:
        click.echo(f"❌ Search error: {e}", err=True)


def _list_microphones():
    """List available audio input devices"""
    from .audio import get_audio_recorder

    recorder = get_audio_recorder()

    if not recorder.is_available():
        click.echo("❌ No audio recording tool found", err=True)
        click.echo("   Install one of: pw-record (PipeWire), arecord (ALSA), or ffmpeg", err=True)
        sys.exit(1)

    click.echo(f"🎤 Audio Recording Tool: {recorder.get_tool_name()}")
    click.echo("─" * 60)

    devices = recorder.list_devices()
    if devices:
        click.echo("Available devices:")
        for i, device in enumerate(devices, 1):
            click.echo(f"  {i}. {device}")
    else:
        click.echo("Default device available")

    click.echo()
    click.echo("Use with: diane record")


def _record_and_transcribe(duration: Optional[int], verbose: bool):
    """Record audio and transcribe it"""
    from .audio import get_audio_recorder, get_audio_transcriber

    recorder = get_audio_recorder()
    transcriber = get_audio_transcriber()

    # Check recording availability
    if not recorder.is_available():
        click.echo("❌ No audio recording tool found", err=True)
        click.echo("   Install one of: pw-record (PipeWire), arecord (ALSA), or ffmpeg", err=True)
        sys.exit(1)

    # Check transcription availability
    if not transcriber.is_available():
        click.echo("❌ OPENAI_API_KEY not set", err=True)
        click.echo("   Set it to enable transcription: export OPENAI_API_KEY=sk-...", err=True)
        sys.exit(1)

    # Show recording info
    if verbose or duration is None:
        duration_msg = f"for {duration} seconds" if duration else "until Ctrl-C"
        click.echo(f"Recording {duration_msg}...")
        click.echo(f"Tool: {recorder.get_tool_name()}")
        if duration is None:
            click.echo("Press Ctrl-C to stop")

    # Record audio
    success, msg, audio_path = recorder.record(duration=duration)

    if not success:
        click.echo(f"❌ {msg}", err=True)
        sys.exit(1)

    if verbose:
        click.echo(f"✅ {msg}")
        click.echo("Transcribing...")

    # Transcribe audio (and clean up on success)
    success, msg, transcription = transcriber.transcribe_and_cleanup(
        audio_path,
        keep_on_failure=True
    )

    if not success:
        click.echo(f"❌ {msg}", err=True)
        click.echo(f"   Audio saved to: {audio_path}", err=True)
        sys.exit(1)

    if verbose:
        click.echo(f"✅ {msg}")

    # Save transcription as record
    storage = Storage()
    record = Record(
        content=transcription,
        sources=["audio-recording"],
        audio_file=str(audio_path) if audio_path.exists() else None
    )

    filepath = storage.save(record)

    if verbose:
        click.echo(f"✅ Recorded: {filepath.name}")
    else:
        click.echo("✓")


def _transcribe_audio_file(audio_file_path: str, verbose: bool):
    """Transcribe an audio file"""
    from .audio import get_audio_transcriber

    transcriber = get_audio_transcriber()

    # Check transcription availability
    if not transcriber.is_available():
        click.echo("❌ OPENAI_API_KEY not set", err=True)
        click.echo("   Set it to enable transcription: export OPENAI_API_KEY=sk-...", err=True)
        sys.exit(1)

    audio_path = Path(audio_file_path)

    if not audio_path.exists():
        click.echo(f"❌ Audio file not found: {audio_file_path}", err=True)
        sys.exit(1)

    if verbose:
        click.echo(f"Transcribing {audio_path.name}...")

    # Transcribe audio (don't clean up - user provided the file)
    success, msg, transcription = transcriber.transcribe(audio_path)

    if not success:
        click.echo(f"❌ {msg}", err=True)
        sys.exit(1)

    if verbose:
        click.echo(f"✅ {msg}")

    # Save transcription as record
    storage = Storage()
    record = Record(
        content=transcription,
        sources=["audio-file"],
        audio_file=str(audio_path)
    )

    filepath = storage.save(record)

    if verbose:
        click.echo(f"✅ Recorded: {filepath.name}")
    else:
        click.echo("✓")


def main():
    """Entry point for CLI"""
    cli()


if __name__ == '__main__':
    main()
