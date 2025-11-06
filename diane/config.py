"""Configuration management for diane."""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Configuration for diane."""

    def __init__(self):
        # Primary storage location
        self.data_home = Path(os.environ.get(
            'DIANE_DATA_HOME',
            os.path.join(os.path.expanduser('~'), '.local', 'share', 'diane')
        ))

        # Records directory
        self.records_dir = self.data_home / 'records'

        # Git integration
        self.use_git = True

        # GPG encryption
        self.gpg_key_id: Optional[str] = os.environ.get('DIANE_GPG_KEY')

        # Default verbosity
        self.verbose = False

    def ensure_directories(self):
        """Ensure all required directories exist."""
        self.data_home.mkdir(parents=True, exist_ok=True)
        self.records_dir.mkdir(parents=True, exist_ok=True)

    def get_records_dir(self) -> Path:
        """Get the records directory path."""
        return self.records_dir


# Global config instance
config = Config()
