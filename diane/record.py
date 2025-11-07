"""Record model for diane entries."""

from datetime import datetime
from pathlib import Path
from typing import List, Optional
import yaml


class Record:
    """Represents a single diane record entry."""

    def __init__(
        self,
        content: str,
        timestamp: Optional[datetime] = None,
        sources: Optional[List[str]] = None,
        audio_file: Optional[str] = None,
    ):
        self.content = content.strip()
        self.timestamp = timestamp or datetime.now()
        self.sources = sources or ["stdin"]
        self.audio_file = audio_file

    def to_frontmatter(self) -> str:
        """Generate YAML frontmatter for this record."""
        metadata = {
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M'),
            'sources': self.sources,
        }

        if self.audio_file:
            metadata['audio'] = self.audio_file

        return yaml.dump(metadata, default_flow_style=False, sort_keys=False)

    def to_markdown(self) -> str:
        """Generate full markdown content with frontmatter."""
        frontmatter = self.to_frontmatter()
        return f"---\n{frontmatter}---\n\n{self.content}\n"

    def get_filename(self, records_dir: Path) -> Path:
        """Generate filename for this record."""
        # Format: YYYY-MM-DD--HH-MM-SS--first-words.txt
        timestamp_str = self.timestamp.strftime('%Y-%m-%d--%H-%M-%S')

        # Extract first few words for filename suffix
        words = self.content.split()[:3]
        suffix = '-'.join(w.lower().replace('/', '-').replace('\\', '-')
                         for w in words if w.isalnum() or w in ['-', '_'])
        suffix = suffix[:40]  # Limit length

        if suffix:
            filename = f"{timestamp_str}--{suffix}.md"
        else:
            filename = f"{timestamp_str}.md"

        return records_dir / filename

    @classmethod
    def from_file(cls, filepath: Path) -> 'Record':
        """Load a record from a file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse frontmatter
        if content.startswith('---\n'):
            parts = content.split('---\n', 2)
            if len(parts) >= 3:
                frontmatter_str = parts[1]
                body = parts[2].strip()

                metadata = yaml.safe_load(frontmatter_str)

                # Parse timestamp
                timestamp_str = metadata.get('timestamp', '')
                try:
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M')
                except ValueError:
                    timestamp = datetime.now()

                return cls(
                    content=body,
                    timestamp=timestamp,
                    sources=metadata.get('sources', ['stdin']),
                    audio_file=metadata.get('audio'),
                )

        # No frontmatter found, treat entire content as body
        return cls(content=content)
