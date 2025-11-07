"""Command-line interface for diane."""

import sys
from datetime import datetime, timedelta
from typing import Optional

import click

from .config import config
from .record import Record
from .storage import Storage
from .sync import GitSync
from .encryption import GPGEncryption, setup_gpg_key
from .export import Exporter
from .stats import Statistics


@click.command()
@click.argument('text', required=False)
@click.option('--tags', help='Comma-separated tags (e.g., work/clients/acme)')
@click.option('--encrypt', is_flag=True, help='Encrypt the record with GPG')
@click.option('--verbose', '-v', is_flag=True, help='Show confirmation messages')
@click.option('--list', '-l', 'list_records', is_flag=True, help='List recent records')
@click.option('--today', is_flag=True, help='Filter to today\'s records (with --list)')
@click.option('--search', '-s', 'search_query', help='Search records by content')
@click.option('--fuzzy', is_flag=True, help='Use fuzzy search (with --search)')
@click.option('--limit', type=int, default=10, help='Limit number of results (default: 10)')
@click.option('--set-remote', 'set_remote', help='Set git remote URL for backup')
@click.option('--push', is_flag=True, help='Push records to remote')
@click.option('--pull', is_flag=True, help='Pull records from remote')
@click.option('--sync', is_flag=True, help='Sync records with remote (pull + push)')
@click.option('--remote-status', is_flag=True, help='Show git remote status')
@click.option('--tui', is_flag=True, help='Launch interactive TUI dashboard')
@click.option('--gpg-list-keys', is_flag=True, help='List available GPG keys')
@click.option('--gpg-setup', is_flag=True, help='Setup GPG encryption interactively')
@click.option('--decrypt', 'decrypt_file', help='Decrypt a specific record file')
@click.option('--export', 'export_format', type=click.Choice(['json', 'csv', 'html', 'markdown']), help='Export records to format')
@click.option('--export-file', help='Output file for export (default: stdout)')
@click.option('--stats', is_flag=True, help='Show statistics about your records')
def main(
    text: Optional[str],
    tags: Optional[str],
    encrypt: bool,
    verbose: bool,
    list_records: bool,
    today: bool,
    search_query: Optional[str],
    fuzzy: bool,
    limit: int,
    set_remote: Optional[str],
    push: bool,
    pull: bool,
    sync: bool,
    remote_status: bool,
    tui: bool,
    gpg_list_keys: bool,
    gpg_setup: bool,
    decrypt_file: Optional[str],
    export_format: Optional[str],
    export_file: Optional[str],
    stats: bool,
):
    """diane, - Externalized mental records clerk.

    Records thoughts, dictations, and reflections with minimal interruption.

    \b
    Examples:
        # Record from stdin
        echo "meeting insights" | diane,

        # Interactive input (type and press Ctrl-D to finish)
        diane,

        # Record with tags
        diane, --tags work/urgent "Remember to call client"

        # List today's records
        diane, --list --today

        # Search records
        diane, --search "meeting"
    """
    # Set verbosity globally
    if verbose:
        config.verbose = True

    # TUI mode
    if tui:
        from .tui import launch_tui
        launch_tui()
        return

    # GPG operations
    if gpg_list_keys:
        encryptor = GPGEncryption()
        keys = encryptor.list_keys()
        if not keys:
            click.echo("❌ No GPG keys found. Generate one with: gpg --gen-key")
            return

        click.echo("🔑 Available GPG keys:")
        click.echo("─" * 60)
        for key in keys:
            click.echo(f"Key ID: {key['key_id']}")
            click.echo(f"   User: {key['uid']}")
            click.echo()
        return

    if gpg_setup:
        setup_gpg_key()
        return

    if decrypt_file:
        encryptor = GPGEncryption()
        from pathlib import Path
        filepath = Path(decrypt_file)

        if not filepath.exists():
            click.echo(f"❌ File not found: {filepath}", err=True)
            sys.exit(1)

        click.echo(f"Decrypting {filepath.name}...")
        success, msg = encryptor.decrypt_file(filepath)

        if success:
            click.echo(f"✅ {msg}")
        else:
            click.echo(f"❌ {msg}", err=True)
            sys.exit(1)
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

    # Search mode
    if search_query:
        if fuzzy:
            # Fuzzy search returns (record, score) tuples
            results = storage.fuzzy_search(search_query, threshold=0.4)
            if not results:
                if config.verbose:
                    click.echo("No matching records found.")
                return

            for record, score in results[:limit]:
                _display_record(record, similarity_score=score if fuzzy else None)
        else:
            # Regular exact search
            results = storage.search(search_query)
            if not results:
                if config.verbose:
                    click.echo("No matching records found.")
                return

            for record in results[:limit]:
                _display_record(record)
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
        click.echo(f"Unique Tags: {summary['unique_tags']}")
        click.echo()

        if summary['busiest_day']:
            click.echo(f"Busiest Day: {summary['busiest_day']} ({summary['busiest_day_count']} records)")
            click.echo()

        if summary['top_tags']:
            click.echo("Top Tags:")
            for tag, count in summary['top_tags']:
                click.echo(f"  • {tag}: {count}")
            click.echo()

        # Show recent activity
        recent = statistics.recent_activity(days=7)
        if recent:
            click.echo("Last 7 Days:")
            for date_str, count in recent.items():
                bar = '█' * count
                click.echo(f"  {date_str}: {bar} {count}")

        return

    # List mode
    if list_records:
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

    # Record mode - get input
    content = None

    if text:
        # Text provided as argument
        content = text
    elif not sys.stdin.isatty():
        # Input from pipe/redirect
        content = sys.stdin.read()
    else:
        # Interactive mode
        if config.verbose:
            click.echo("Enter text (Ctrl-D to finish):")
        try:
            content = sys.stdin.read()
        except KeyboardInterrupt:
            if config.verbose:
                click.echo("\nCancelled.")
            sys.exit(1)

    if not content or not content.strip():
        if config.verbose:
            click.echo("No content provided.")
        sys.exit(0)

    # Parse tags
    tag_list = []
    if tags:
        tag_list = [t.strip() for t in tags.split(',')]

    # Create and save record
    record = Record(
        content=content,
        tags=tag_list,
        sources=["stdin"] if not sys.stdin.isatty() else ["interactive"],
    )

    filepath = storage.save(record, encrypt=encrypt)

    # Silent by default, unless verbose
    if config.verbose:
        click.echo(f"✅ Recorded: {filepath.name}")


def _display_record(record: Record, similarity_score: Optional[float] = None):
    """Display a record in a readable format.

    Args:
        record: The record to display
        similarity_score: Optional fuzzy search similarity score (0.0-1.0)
    """
    click.echo("─" * 60)
    timestamp = record.timestamp.strftime('%Y-%m-%d %H:%M')
    click.echo(f"📅 {timestamp}", nl=False)

    if similarity_score is not None:
        # Show similarity as percentage
        score_pct = int(similarity_score * 100)
        click.echo(f" | 🎯 {score_pct}%", nl=False)

    if record.tags:
        tags_str = ", ".join(record.tags)
        click.echo(f" | 🏷  {tags_str}")
    else:
        click.echo()

    click.echo()
    click.echo(record.content)
    click.echo()


if __name__ == '__main__':
    main()
