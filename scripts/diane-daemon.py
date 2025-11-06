#!/usr/bin/env python3
"""
diane, background sync daemon

Automatically syncs records to remote repository at regular intervals.
Runs silently in the background.

Usage:
    diane-daemon.py [--interval SECONDS] [--log-file PATH]

Options:
    --interval SECONDS    Sync interval in seconds (default: 300 = 5 minutes)
    --log-file PATH       Log file path (default: ~/.local/share/diane/daemon.log)
"""

import sys
import time
import signal
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
import os


class DianeDaemon:
    """Background daemon for automatic record syncing."""

    def __init__(self, interval: int = 300, log_file: Path = None):
        self.interval = interval
        self.log_file = log_file or Path.home() / '.local/share/diane/daemon.log'
        self.running = True
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(self, message: str):
        """Log a message with timestamp."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {message}\n"

        with open(self.log_file, 'a') as f:
            f.write(log_msg)

    def sync_records(self):
        """Perform a sync operation."""
        try:
            result = subprocess.run(
                ['diane,', '--sync'],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                self.log("✅ Sync successful")
                return True
            else:
                self.log(f"❌ Sync failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            self.log("⏱️  Sync timeout")
            return False
        except Exception as e:
            self.log(f"❌ Error during sync: {e}")
            return False

    def stop(self, signum, frame):
        """Handle stop signal."""
        self.log("🛑 Daemon stopping...")
        self.running = False
        sys.exit(0)

    def run(self):
        """Main daemon loop."""
        # Register signal handlers
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

        self.log(f"🚀 Daemon started (interval: {self.interval}s)")

        while self.running:
            self.sync_records()
            time.sleep(self.interval)


def main():
    parser = argparse.ArgumentParser(description='diane, background sync daemon')
    parser.add_argument(
        '--interval',
        type=int,
        default=300,
        help='Sync interval in seconds (default: 300)'
    )
    parser.add_argument(
        '--log-file',
        type=Path,
        default=None,
        help='Log file path'
    )

    args = parser.parse_args()

    daemon = DianeDaemon(interval=args.interval, log_file=args.log_file)
    daemon.run()


if __name__ == '__main__':
    main()
