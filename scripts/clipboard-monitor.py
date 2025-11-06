#!/usr/bin/env python3
"""
diane, clipboard monitor

Watches clipboard for changes and optionally auto-captures interesting content.

Usage:
    clipboard-monitor.py [--auto-capture] [--filter REGEX] [--tag TAG]

Options:
    --auto-capture        Automatically capture clipboard changes
    --filter REGEX        Only capture if clipboard matches regex
    --tag TAG            Tag to apply to captured clips (default: clipboard)
    --min-length N       Minimum length to capture (default: 10)
    --interval SECONDS   Check interval (default: 2)
"""

import sys
import time
import re
import argparse
import subprocess
from typing import Optional


class ClipboardMonitor:
    """Monitor clipboard for changes and capture to diane."""

    def __init__(
        self,
        auto_capture: bool = False,
        filter_regex: Optional[str] = None,
        tag: str = "clipboard",
        min_length: int = 10,
        interval: int = 2,
    ):
        self.auto_capture = auto_capture
        self.filter_regex = re.compile(filter_regex) if filter_regex else None
        self.tag = tag
        self.min_length = min_length
        self.interval = interval
        self.last_content = ""

    def get_clipboard(self) -> Optional[str]:
        """Get current clipboard content."""
        try:
            # Try macOS
            result = subprocess.run(
                ['pbpaste'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        try:
            # Try Linux xclip
            result = subprocess.run(
                ['xclip', '-o', '-selection', 'clipboard'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        try:
            # Try Wayland wl-paste
            result = subprocess.run(
                ['wl-paste'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        return None

    def capture_to_diane(self, content: str) -> bool:
        """Capture content to diane."""
        try:
            result = subprocess.run(
                ['diane,', '--tags', self.tag],
                input=content,
                text=True,
                capture_output=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to capture: {e}")
            return False

    def should_capture(self, content: str) -> bool:
        """Check if content should be captured."""
        # Check minimum length
        if len(content) < self.min_length:
            return False

        # Check filter regex
        if self.filter_regex and not self.filter_regex.search(content):
            return False

        return True

    def run(self):
        """Main monitoring loop."""
        print(f"👁️  Monitoring clipboard (interval: {self.interval}s)")
        if self.auto_capture:
            print(f"🤖 Auto-capture enabled (tag: {self.tag})")
        else:
            print("📋 Manual mode - press Enter to capture current clipboard")

        try:
            while True:
                content = self.get_clipboard()

                if content and content != self.last_content:
                    if self.should_capture(content):
                        preview = content[:50].replace('\n', ' ')
                        if len(content) > 50:
                            preview += "..."

                        print(f"\n📋 Clipboard changed: {preview}")

                        if self.auto_capture:
                            if self.capture_to_diane(content):
                                print("✅ Auto-captured")
                                self.last_content = content
                        else:
                            print("   Press Enter to capture, or any other key to skip...")
                            # This is tricky in Python without async, simplified version
                            self.last_content = content

                time.sleep(self.interval)

        except KeyboardInterrupt:
            print("\n👋 Clipboard monitor stopped")


def main():
    parser = argparse.ArgumentParser(description='diane, clipboard monitor')
    parser.add_argument(
        '--auto-capture',
        action='store_true',
        help='Automatically capture clipboard changes'
    )
    parser.add_argument(
        '--filter',
        help='Only capture if clipboard matches regex'
    )
    parser.add_argument(
        '--tag',
        default='clipboard',
        help='Tag for captured content (default: clipboard)'
    )
    parser.add_argument(
        '--min-length',
        type=int,
        default=10,
        help='Minimum length to capture (default: 10)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=2,
        help='Check interval in seconds (default: 2)'
    )

    args = parser.parse_args()

    monitor = ClipboardMonitor(
        auto_capture=args.auto_capture,
        filter_regex=args.filter,
        tag=args.tag,
        min_length=args.min_length,
        interval=args.interval,
    )

    monitor.run()


if __name__ == '__main__':
    main()
