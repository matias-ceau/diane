"""Tests for record module."""

from datetime import datetime
from pathlib import Path
import tempfile

from diane.record import Record


def test_record_creation():
    """Test creating a basic record."""
    content = "This is a test record"
    tags = ["test", "sample"]

    record = Record(content=content, tags=tags)

    assert record.content == content
    assert record.tags == tags
    assert isinstance(record.timestamp, datetime)
    assert record.sources == ["stdin"]


def test_record_to_markdown():
    """Test generating markdown with frontmatter."""
    record = Record(
        content="Test content",
        tags=["test"],
        timestamp=datetime(2024, 11, 6, 13, 30),
    )

    markdown = record.to_markdown()

    assert "---" in markdown
    assert "timestamp: 2024-11-06 13:30" in markdown
    assert "tags:" in markdown
    assert "test" in markdown
    assert "Test content" in markdown


def test_record_filename():
    """Test filename generation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        records_dir = Path(tmpdir)

        record = Record(
            content="Meeting insights from discussion",
            timestamp=datetime(2024, 11, 6, 13, 30, 45),
        )

        filename = record.get_filename(records_dir)

        assert filename.parent == records_dir
        assert filename.name.startswith("2024-11-06--13-30-45")
        assert "meeting" in filename.name.lower()
        assert filename.suffix == ".md"


def test_record_from_file():
    """Test loading a record from file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "test.md"

        # Create a test file
        content = """---
timestamp: 2024-11-06 13:30
tags: [work, urgent]
sources: [stdin]
---

This is the record content.
"""
        filepath.write_text(content)

        # Load the record
        record = Record.from_file(filepath)

        assert record.content == "This is the record content."
        assert record.tags == ["work", "urgent"]
        assert record.timestamp == datetime(2024, 11, 6, 13, 30)
