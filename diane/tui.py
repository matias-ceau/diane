"""Terminal User Interface for diane."""

try:
    from textual.app import App, ComposeResult
    from textual.containers import Container, Vertical, Horizontal
    from textual.widgets import Header, Footer, Static, ListView, ListItem, Label
    from textual.binding import Binding
    from textual.reactive import reactive
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False

from datetime import datetime
from typing import List
from .storage import Storage
from .record import Record


if TEXTUAL_AVAILABLE:
    class RecordItem(ListItem):
        """A list item representing a single record."""

        def __init__(self, record: Record, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.record = record

        def compose(self) -> ComposeResult:
            """Create child widgets."""
            timestamp = self.record.timestamp.strftime('%Y-%m-%d %H:%M')
            tags = ", ".join(self.record.tags) if self.record.tags else "no tags"

            # Show first line of content
            first_line = self.record.content.split('\n')[0][:60]
            if len(self.record.content) > 60:
                first_line += "..."

            yield Label(f"[bold cyan]{timestamp}[/] [dim]|[/] [yellow]{tags}[/]")
            yield Label(first_line)


    class RecordDetail(Static):
        """Widget to display full record details."""

        record = reactive(None)

        def watch_record(self, record: Record) -> None:
            """Called when the record changes."""
            if record:
                timestamp = record.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                tags = ", ".join(record.tags) if record.tags else "no tags"

                content = f"""[bold cyan]📅 {timestamp}[/bold cyan]
[yellow]🏷  {tags}[/yellow]

{record.content}
"""
                self.update(content)
            else:
                self.update("[dim]Select a record to view details[/dim]")


    class DianeTUI(App):
        """A Textual app for browsing diane records."""

        CSS = """
        Screen {
            layout: horizontal;
        }

        #sidebar {
            width: 45;
            border-right: solid $primary;
        }

        #detail {
            width: 1fr;
            padding: 1 2;
        }

        ListView {
            height: 1fr;
        }

        RecordItem {
            padding: 1;
            border-bottom: solid $surface;
        }

        RecordItem:hover {
            background: $surface;
        }

        RecordItem.-selected {
            background: $primary 20%;
        }
        """

        BINDINGS = [
            Binding("q", "quit", "Quit"),
            Binding("r", "refresh", "Refresh"),
            ("j", "cursor_down", "Down"),
            ("k", "cursor_up", "Up"),
        ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.storage = Storage()
            self.records: List[Record] = []

        def compose(self) -> ComposeResult:
            """Create child widgets for the app."""
            yield Header()

            with Horizontal():
                with Vertical(id="sidebar"):
                    yield Static("[bold]diane, records[/bold]", id="title")
                    yield ListView(id="records-list")

                yield RecordDetail(id="detail")

            yield Footer()

        def on_mount(self) -> None:
            """Called when app starts."""
            self.title = "diane, - Records Browser"
            self.refresh_records()

        def refresh_records(self) -> None:
            """Load and display all records."""
            self.records = self.storage.list_records(limit=None)

            list_view = self.query_one("#records-list", ListView)
            list_view.clear()

            for record in self.records:
                list_view.append(RecordItem(record))

            # Auto-select first item if available
            if self.records:
                list_view.index = 0

        def on_list_view_selected(self, event: ListView.Selected) -> None:
            """Called when a record is selected."""
            item = event.item
            if isinstance(item, RecordItem):
                detail = self.query_one("#detail", RecordDetail)
                detail.record = item.record

        def action_refresh(self) -> None:
            """Refresh the record list."""
            self.refresh_records()
            self.notify("Records refreshed")


def launch_tui() -> None:
    """Launch the TUI application."""
    if not TEXTUAL_AVAILABLE:
        print("❌ TUI requires 'textual' package. Install with: pip install textual")
        return

    app = DianeTUI()
    app.run()
