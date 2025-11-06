"""Command-line interface for diane."""

import sys
from datetime import datetime, timedelta
from typing import Optional

import click

from .config import config
from .record import Record
from .storage import Storage


@click.command()
@click.argument('text', required=False)
@click.option('--tags', help='Comma-separated tags (e.g., work/clients/acme)')
@click.option('--encrypt', is_flag=True, help='Encrypt the record with GPG')
@click.option('--verbose', '-v', is_flag=True, help='Show confirmation messages')
@click.option('--list', '-l', 'list_records', is_flag=True, help='List recent records')
@click.option('--today', is_flag=True, help='Filter to today\'s records (with --list)')
@click.option('--search', '-s', 'search_query', help='Search records by content')
@click.option('--limit', type=int, default=10, help='Limit number of results (default: 10)')
def main(
    text: Optional[str],
    tags: Optional[str],
    encrypt: bool,
    verbose: bool,
    list_records: bool,
    today: bool,
    search_query: Optional[str],
    limit: int,
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

    storage = Storage()

    # Search mode
    if search_query:
        results = storage.search(search_query)
        if not results:
            if config.verbose:
                click.echo("No matching records found.")
            return

        for record in results[:limit]:
            _display_record(record)
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


def _display_record(record: Record):
    """Display a record in a readable format."""
    click.echo("─" * 60)
    timestamp = record.timestamp.strftime('%Y-%m-%d %H:%M')
    click.echo(f"📅 {timestamp}", nl=False)

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
