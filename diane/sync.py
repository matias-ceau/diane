"""Git sync functionality for diane records."""

import subprocess
from pathlib import Path
from typing import Optional, Tuple

from .config import config


class GitSync:
    """Handles Git synchronization with remote repositories."""

    def __init__(self, records_dir: Optional[Path] = None):
        self.records_dir = records_dir or config.get_records_dir()
        self.git_dir = self.records_dir / '.git'

    def is_git_repo(self) -> bool:
        """Check if records directory is a git repository."""
        return self.git_dir.exists()

    def get_remote_url(self) -> Optional[str]:
        """Get the current remote URL."""
        if not self.is_git_repo():
            return None

        try:
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                cwd=self.records_dir,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    def set_remote(self, url: str) -> Tuple[bool, str]:
        """Set or update the remote URL.

        Args:
            url: Git remote URL (e.g., git@github.com:user/repo.git)

        Returns:
            Tuple of (success, message)
        """
        if not self.is_git_repo():
            return False, "Not a git repository"

        try:
            # Check if remote exists
            current_remote = self.get_remote_url()

            if current_remote:
                # Update existing remote
                subprocess.run(
                    ['git', 'remote', 'set-url', 'origin', url],
                    cwd=self.records_dir,
                    check=True,
                    capture_output=True
                )
                return True, f"Remote updated: {url}"
            else:
                # Add new remote
                subprocess.run(
                    ['git', 'remote', 'add', 'origin', url],
                    cwd=self.records_dir,
                    check=True,
                    capture_output=True
                )
                return True, f"Remote added: {url}"

        except subprocess.CalledProcessError as e:
            return False, f"Failed to set remote: {e.stderr.decode() if e.stderr else str(e)}"

    def push(self, force: bool = False) -> Tuple[bool, str]:
        """Push records to remote.

        Args:
            force: Whether to force push

        Returns:
            Tuple of (success, message)
        """
        if not self.is_git_repo():
            return False, "Not a git repository"

        if not self.get_remote_url():
            return False, "No remote configured. Use --set-remote first."

        try:
            cmd = ['git', 'push', '-u', 'origin']

            # Get current branch
            branch_result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.records_dir,
                capture_output=True,
                text=True,
                check=True
            )
            branch = branch_result.stdout.strip() or 'master'
            cmd.append(branch)

            if force:
                cmd.append('--force')

            result = subprocess.run(
                cmd,
                cwd=self.records_dir,
                capture_output=True,
                text=True,
                check=True
            )

            return True, f"Successfully pushed to remote"

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            return False, f"Push failed: {error_msg}"

    def pull(self, force: bool = False) -> Tuple[bool, str]:
        """Pull records from remote.

        Args:
            force: Whether to force pull (reset to remote)

        Returns:
            Tuple of (success, message)
        """
        if not self.is_git_repo():
            return False, "Not a git repository"

        if not self.get_remote_url():
            return False, "No remote configured. Use --set-remote first."

        try:
            if force:
                # Reset to remote state
                subprocess.run(
                    ['git', 'fetch', 'origin'],
                    cwd=self.records_dir,
                    check=True,
                    capture_output=True
                )

                # Get current branch
                branch_result = subprocess.run(
                    ['git', 'branch', '--show-current'],
                    cwd=self.records_dir,
                    capture_output=True,
                    text=True,
                    check=True
                )
                branch = branch_result.stdout.strip() or 'master'

                subprocess.run(
                    ['git', 'reset', '--hard', f'origin/{branch}'],
                    cwd=self.records_dir,
                    check=True,
                    capture_output=True
                )
                return True, "Successfully reset to remote state"
            else:
                # Normal pull
                result = subprocess.run(
                    ['git', 'pull', 'origin'],
                    cwd=self.records_dir,
                    capture_output=True,
                    text=True,
                    check=True
                )
                return True, "Successfully pulled from remote"

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            return False, f"Pull failed: {error_msg}"

    def sync(self) -> Tuple[bool, str]:
        """Sync with remote (pull then push).

        Returns:
            Tuple of (success, message)
        """
        # First pull
        success, msg = self.pull()
        if not success:
            return False, f"Sync failed during pull: {msg}"

        # Then push
        success, msg = self.push()
        if not success:
            return False, f"Sync failed during push: {msg}"

        return True, "Successfully synced with remote"

    def status(self) -> dict:
        """Get git status information.

        Returns:
            Dictionary with status information
        """
        if not self.is_git_repo():
            return {
                'is_repo': False,
                'has_remote': False,
                'remote_url': None,
                'branch': None,
                'has_changes': False,
                'ahead': 0,
                'behind': 0,
            }

        try:
            # Get branch
            branch_result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=self.records_dir,
                capture_output=True,
                text=True,
                check=True
            )
            branch = branch_result.stdout.strip() or 'master'

            # Check for changes
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.records_dir,
                capture_output=True,
                text=True,
                check=True
            )
            has_changes = bool(status_result.stdout.strip())

            # Check ahead/behind
            ahead = 0
            behind = 0
            remote_url = self.get_remote_url()

            if remote_url:
                try:
                    rev_result = subprocess.run(
                        ['git', 'rev-list', '--left-right', '--count', f'origin/{branch}...HEAD'],
                        cwd=self.records_dir,
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    parts = rev_result.stdout.strip().split()
                    if len(parts) == 2:
                        behind = int(parts[0])
                        ahead = int(parts[1])
                except subprocess.CalledProcessError:
                    pass

            return {
                'is_repo': True,
                'has_remote': bool(remote_url),
                'remote_url': remote_url,
                'branch': branch,
                'has_changes': has_changes,
                'ahead': ahead,
                'behind': behind,
            }

        except subprocess.CalledProcessError:
            return {
                'is_repo': True,
                'has_remote': False,
                'remote_url': None,
                'branch': None,
                'has_changes': False,
                'ahead': 0,
                'behind': 0,
            }
