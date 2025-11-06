"""Storage management for diane records."""

from pathlib import Path
from typing import List, Optional, Tuple
from datetime import datetime, timedelta
from difflib import SequenceMatcher
import subprocess

from .config import config
from .record import Record
from .encryption import GPGEncryption


class Storage:
    """Handles saving and retrieving records."""

    def __init__(self):
        self.records_dir = config.get_records_dir()
        self._ensure_initialized()

    def _ensure_initialized(self):
        """Ensure storage directories and git repo are initialized."""
        config.ensure_directories()

        # Initialize git repo if enabled and not already present
        if config.use_git:
            git_dir = self.records_dir / '.git'
            if not git_dir.exists():
                try:
                    subprocess.run(
                        ['git', 'init'],
                        cwd=self.records_dir,
                        check=True,
                        capture_output=True
                    )
                    # Disable GPG signing for this repo
                    subprocess.run(
                        ['git', 'config', 'commit.gpgsign', 'false'],
                        cwd=self.records_dir,
                        check=True,
                        capture_output=True
                    )
                    # Create initial .gitignore
                    gitignore = self.records_dir / '.gitignore'
                    if not gitignore.exists():
                        gitignore.write_text('*.tmp\n*.swp\n')
                        subprocess.run(
                            ['git', 'add', '.gitignore'],
                            cwd=self.records_dir,
                            check=True,
                            capture_output=True
                        )
                        subprocess.run(
                            ['git', 'commit', '-m', 'Initialize diane records'],
                            cwd=self.records_dir,
                            check=True,
                            capture_output=True
                        )
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Git not available or failed, continue without it
                    config.use_git = False

    def save(self, record: Record, encrypt: bool = False) -> Path:
        """Save a record to storage.

        Args:
            record: The record to save
            encrypt: Whether to encrypt the file with GPG

        Returns:
            Path to the saved file
        """
        filepath = record.get_filename(self.records_dir)

        # Write the record
        content = record.to_markdown()

        if encrypt:
            # Encrypt with GPG
            encryptor = GPGEncryption()
            if not encryptor.is_available():
                # Fall back to unencrypted if GPG not available
                filepath.write_text(content, encoding='utf-8')
            else:
                # Write unencrypted first, then encrypt in place
                filepath.write_text(content, encoding='utf-8')
                success, msg = encryptor.encrypt_file(filepath)
                if success:
                    # Update filepath to encrypted version
                    filepath = filepath.with_suffix(filepath.suffix + '.gpg')
        else:
            filepath.write_text(content, encoding='utf-8')

        # Git commit if enabled
        if config.use_git:
            self._git_commit(filepath)

        return filepath

    def _git_commit(self, filepath: Path):
        """Commit a file to git."""
        try:
            subprocess.run(
                ['git', 'add', filepath.name],
                cwd=self.records_dir,
                check=True,
                capture_output=True
            )
            commit_msg = f"Record: {filepath.name}"
            subprocess.run(
                ['git', 'commit', '-m', commit_msg],
                cwd=self.records_dir,
                check=True,
                capture_output=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Git operation failed, silently continue
            pass

    def list_records(
        self,
        limit: Optional[int] = None,
        since: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
    ) -> List[Record]:
        """List records from storage.

        Args:
            limit: Maximum number of records to return
            since: Only return records after this time
            tags: Only return records with these tags

        Returns:
            List of Record objects
        """
        records = []

        # Get all markdown files
        for filepath in sorted(self.records_dir.glob('*.md'), reverse=True):
            try:
                record = Record.from_file(filepath)

                # Apply filters
                if since and record.timestamp < since:
                    continue

                if tags:
                    if not any(tag in record.tags for tag in tags):
                        continue

                records.append(record)

                if limit and len(records) >= limit:
                    break

            except Exception:
                # Skip files that can't be parsed
                continue

        return records

    def search(self, query: str, case_sensitive: bool = False) -> List[Record]:
        """Search records by content.

        Args:
            query: Search query string
            case_sensitive: Whether search should be case-sensitive

        Returns:
            List of matching Record objects
        """
        results = []

        if not case_sensitive:
            query = query.lower()

        for filepath in self.records_dir.glob('*.md'):
            try:
                record = Record.from_file(filepath)
                search_text = record.content if case_sensitive else record.content.lower()

                if query in search_text:
                    results.append(record)

            except Exception:
                # Skip files that can't be parsed
                continue

        # Sort by timestamp, most recent first
        results.sort(key=lambda r: r.timestamp, reverse=True)
        return results

    def fuzzy_search(
        self,
        query: str,
        threshold: float = 0.6,
        case_sensitive: bool = False
    ) -> List[Tuple[Record, float]]:
        """Fuzzy search records by content with similarity scores.

        Args:
            query: Search query string
            threshold: Minimum similarity score (0.0 to 1.0)
            case_sensitive: Whether search should be case-sensitive

        Returns:
            List of tuples (Record, similarity_score), sorted by score descending
        """
        results = []

        if not case_sensitive:
            query = query.lower()

        for filepath in self.records_dir.glob('*.md'):
            try:
                record = Record.from_file(filepath)
                search_text = record.content if case_sensitive else record.content.lower()

                # Calculate similarity using SequenceMatcher
                similarity = SequenceMatcher(None, query, search_text).ratio()

                # Also check for partial matches in words
                words = search_text.split()
                word_similarities = [
                    SequenceMatcher(None, query, word).ratio()
                    for word in words
                ]
                max_word_sim = max(word_similarities) if word_similarities else 0

                # Use the better of the two scores
                final_score = max(similarity, max_word_sim)

                if final_score >= threshold:
                    results.append((record, final_score))

            except Exception:
                # Skip files that can't be parsed
                continue

        # Sort by similarity score (descending), then by timestamp (descending)
        results.sort(key=lambda x: (x[1], x[0].timestamp), reverse=True)
        return results
