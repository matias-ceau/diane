"""Command-line interface for diane."""

import sys
from datetime import datetime, timedelta
from typing import Optional

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

from .config import config
from .record import Record
from .storage import Storage
from .sync import GitSync
from .encryption import GPGEncryption, setup_gpg_key
from .export import Exporter
from .stats import Statistics


@click.command()
@click.argument('text', required=False)
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
@click.option('--search', 'search_query', help='Search records with ripgrep + fzf')
@click.option('--limit', type=int, default=10, help='Limit number of results (default: 10)')
@click.option('--today', is_flag=True, help='Filter to today\'s records')
@click.option('--info', '--path', 'show_info', is_flag=True, help='Show configuration and paths')
@click.option('--record', is_flag=True, help='Record audio from microphone and transcribe')
@click.option('--record-duration', type=int, help='Recording duration in seconds (default: until Ctrl-C)')
@click.option('--audio-file', type=click.Path(exists=True), help='Transcribe audio file')
@click.option('--list-mics', is_flag=True, help='List available microphones')
@click.option('--set-remote', 'set_remote', help='Set git remote URL for backup')
@click.option('--push', is_flag=True, help='Push records to remote')
@click.option('--pull', is_flag=True, help='Pull records from remote')
@click.option('--sync', is_flag=True, help='Sync records with remote (pull + push)')
@click.option('--remote-status', is_flag=True, help='Show git remote status')
@click.option('--tui', is_flag=True, help='Launch interactive TUI dashboard')
@click.option('--setup', is_flag=True, help='Run first-time setup wizard')
@click.option('--export', 'export_format', type=click.Choice(['json', 'csv', 'html', 'markdown']), help='Export records to format')
@click.option('--export-file', help='Output file for export (default: stdout)')
@click.option('--stats', is_flag=True, help='Show statistics about your records')
def main(
    text: Optional[str],
    verbose: bool,
    search_query: Optional[str],
    limit: int,
    today: bool,
    show_info: bool,
    record: bool,
    record_duration: Optional[int],
    audio_file: Optional[str],
    list_mics: bool,
    set_remote: Optional[str],
    push: bool,
    pull: bool,
    sync: bool,
    remote_status: bool,
    tui: bool,
    setup: bool,
    export_format: Optional[str],
    export_file: Optional[str],
    stats: bool,
):
    """diane - Externalized mental records clerk.

    Records thoughts, dictations, and reflections with minimal interruption.

    \b
    Examples:
        # Show latest records (default behavior)
        diane

        # Record from stdin
        echo "meeting insights" | diane

        # Record audio
        diane --record
        diane --record --record-duration 30

        # Transcribe audio file
        diane --audio-file recording.wav

        # Search records with ripgrep + fzf
        diane --search "meeting"

        # Show today's records
        diane --today
    """
    # Set verbosity globally
    if verbose:
        config.verbose = True

    # Setup wizard
    if setup:
        _run_setup_wizard()
        return

    # Info mode
    if show_info:
        _show_info()
        return

    # List microphones
    if list_mics:
        _list_microphones()
        return

    # Audio recording mode
    if record:
        _record_and_transcribe(record_duration, verbose)
        return

    # Audio file transcription mode
    if audio_file:
        _transcribe_audio_file(audio_file, verbose)
        return

    # TUI mode
    if tui:
        from .tui import launch_tui
        launch_tui()
        return

    storage = Storage()
    git_sync = GitSync()

    # Git remote operations
    if set_remote:
        success, msg = git_sync.set_remote(set_remote)
        if success:
            click.echo(f"✅ {msg}")
        else:
            click.echo(f"❌ {msg}", err=True)
            sys.exit(1)
        return

    if remote_status:
        status = git_sync.status()
        if not status['is_repo']:
            click.echo("❌ Not a git repository")
            return

        click.echo("📡 Remote Status")
        click.echo("─" * 60)
        click.echo(f"Branch: {status['branch'] or 'unknown'}")
        click.echo(f"Remote: {status['remote_url'] or 'none configured'}")

        if status['has_remote']:
            if status['ahead'] > 0:
                click.echo(f"↑ Ahead by {status['ahead']} commit(s)")
            if status['behind'] > 0:
                click.echo(f"↓ Behind by {status['behind']} commit(s)")
            if status['ahead'] == 0 and status['behind'] == 0:
                click.echo("✅ Up to date with remote")

        if status['has_changes']:
            click.echo("⚠ Uncommitted changes")
        return

    if push:
        click.echo("Pushing to remote...")
        success, msg = git_sync.push()
        if success:
            click.echo(f"✅ {msg}")
        else:
            click.echo(f"❌ {msg}", err=True)
            sys.exit(1)
        return

    if pull:
        click.echo("Pulling from remote...")
        success, msg = git_sync.pull()
        if success:
            click.echo(f"✅ {msg}")
        else:
            click.echo(f"❌ {msg}", err=True)
            sys.exit(1)
        return

    if sync:
        click.echo("Syncing with remote...")
        success, msg = git_sync.sync()
        if success:
            click.echo(f"✅ {msg}")
        else:
            click.echo(f"❌ {msg}", err=True)
            sys.exit(1)
        return

    # Search mode - use ripgrep + fzf
    if search_query:
        _interactive_search(search_query)
        return

    # Export mode
    if export_format:
        # Get all records (or filtered)
        since = None
        if today:
            since = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        results = storage.list_records(limit=None, since=since)

        if not results:
            click.echo("No records to export.")
            return

        # Generate export
        if export_format == 'json':
            content = Exporter.to_json(results)
        elif export_format == 'csv':
            content = Exporter.to_csv(results)
        elif export_format == 'html':
            content = Exporter.to_html(results)
        elif export_format == 'markdown':
            content = Exporter.to_markdown(results)

        # Output
        if export_file:
            from pathlib import Path
            Exporter.save_export(content, Path(export_file))
            click.echo(f"✅ Exported {len(results)} records to {export_file}")
        else:
            click.echo(content)
        return

    # Statistics mode
    if stats:
        records = storage.list_records(limit=None)
        if not records:
            click.echo("No records found.")
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
        recent = statistics.recent_activity(days=7)
        if recent:
            click.echo("Last 7 Days:")
            for date_str, count in recent.items():
                bar = '█' * count
                click.echo(f"  {date_str}: {bar} {count}")

        return

    # Record mode - get input
    content = None

    if text:
        # Text provided as argument
        content = text
    elif not sys.stdin.isatty():
        # Input from pipe/redirect - read it
        content = sys.stdin.read()

    # If no content provided (no args, no stdin data), show latest records
    if not content or not content.strip():
        # Default behavior: show latest records
        since = None
        if today:
            # Get records from start of today
            since = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        results = storage.list_records(limit=limit, since=since)

        if not results:
            if config.verbose:
                click.echo("No records found.")
            return

        for record in results:
            _display_record(record)
        return

    # Create and save record
    record = Record(
        content=content,
        sources=["stdin"] if not sys.stdin.isatty() else ["interactive"],
    )

    filepath = storage.save(record)

    # Show simple confirmation by default, detailed info with --verbose
    if config.verbose:
        click.echo(f"✅ Recorded: {filepath.name}")
    else:
        click.echo("✓")


def _display_record(record: Record):
    """Display a record in a readable format.

    Args:
        record: The record to display
    """
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
        # Clean output for pipes - just content, one record per line
        # Format: timestamp|content (allows parsing with cut/awk)
        timestamp = record.timestamp.strftime('%Y-%m-%d %H:%M')
        # Escape newlines in content for single-line output
        clean_content = record.content.replace('\n', ' ')
        click.echo(f"{timestamp}|{clean_content}")


def _show_info():
    """Show configuration and paths information."""
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
    click.echo("Run 'diane --setup' to configure diane")


def _run_setup_wizard():
    """Run first-time setup wizard."""
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
    click.echo("  • diane                    # Show latest records")
    click.echo("  • echo 'note' | diane      # Capture a quick thought")
    click.echo("  • diane --search 'query'   # Search with ripgrep + fzf")
    click.echo("  • diane --sync             # Sync with remote")
    click.echo("  • diane --info             # Show configuration")
    click.echo()


def _interactive_search(query: str):
    """Launch interactive search using ripgrep + fzf."""
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
        rg_result = subprocess.run(
            ['rg', '--color=always', '--line-number', '--no-heading', '--smart-case', query],
            cwd=records_dir,
            capture_output=True,
            text=True
        )

        if not rg_result.stdout:
            click.echo("No matches found.")
            return

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

        stdout, stderr = fzf_process.communicate(input=rg_result.stdout)

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
        click.echo("\nSearch cancelled.")
    except Exception as e:
        click.echo(f"❌ Search error: {e}", err=True)


def _list_microphones():
    """List available audio input devices."""
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
    click.echo("Use default device with: diane --record")


def _record_and_transcribe(duration: Optional[int], verbose: bool):
    """Record audio and transcribe it."""
    from .audio import get_audio_recorder, get_audio_transcriber
    from pathlib import Path

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
        click.echo(f"🎤 Recording {duration_msg}...")
        click.echo(f"   Tool: {recorder.get_tool_name()}")
        if duration is None:
            click.echo("   Press Ctrl-C to stop")

    # Record audio
    success, msg, audio_path = recorder.record(duration=duration)

    if not success:
        click.echo(f"❌ {msg}", err=True)
        sys.exit(1)

    if verbose:
        click.echo(f"✅ {msg}")
        click.echo("📝 Transcribing...")

    # Transcribe audio (and clean up on success)
    success, msg, transcription = transcriber.transcribe_and_cleanup(
        audio_path,
        keep_on_failure=True  # Keep audio file if transcription fails
    )

    if not success:
        click.echo(f"❌ {msg}", err=True)
        click.echo(f"   Audio saved to: {audio_path}", err=True)
        sys.exit(1)

    if verbose:
        click.echo(f"✅ {msg}")
        click.echo()

    # Save transcription as record
    storage = Storage()
    record = Record(
        content=transcription,
        sources=["audio-recording"],
        audio_file=str(audio_path) if audio_path.exists() else None
    )

    filepath = storage.save(record)

    # Show confirmation
    if verbose:
        click.echo(f"✅ Recorded: {filepath.name}")
    else:
        click.echo("✓")


def _transcribe_audio_file(audio_file_path: str, verbose: bool):
    """Transcribe an audio file."""
    from .audio import get_audio_transcriber
    from pathlib import Path

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
        click.echo(f"📝 Transcribing {audio_path.name}...")

    # Transcribe audio (don't clean up - user provided the file)
    success, msg, transcription = transcriber.transcribe(audio_path)

    if not success:
        click.echo(f"❌ {msg}", err=True)
        sys.exit(1)

    if verbose:
        click.echo(f"✅ {msg}")
        click.echo()

    # Save transcription as record
    storage = Storage()
    record = Record(
        content=transcription,
        sources=["audio-file"],
        audio_file=str(audio_path)
    )

    filepath = storage.save(record)

    # Show confirmation
    if verbose:
        click.echo(f"✅ Recorded: {filepath.name}")
    else:
        click.echo("✓")


if __name__ == '__main__':
    main()
