"""GPG encryption support for diane records."""

import subprocess
from pathlib import Path
from typing import Optional, Tuple

from .config import config


class GPGEncryption:
    """Handles GPG encryption and decryption of records."""

    def __init__(self, key_id: Optional[str] = None):
        self.key_id = key_id or config.gpg_key_id
        self._gpg_available = self._check_gpg_available()

    def _check_gpg_available(self) -> bool:
        """Check if GPG is available on the system."""
        try:
            result = subprocess.run(
                ['gpg', '--version'],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def is_available(self) -> bool:
        """Check if GPG encryption is available."""
        return self._gpg_available and self.key_id is not None

    def list_keys(self) -> list:
        """List available GPG keys."""
        if not self._gpg_available:
            return []

        try:
            result = subprocess.run(
                ['gpg', '--list-keys', '--with-colons'],
                capture_output=True,
                text=True,
                check=True
            )

            keys = []
            current_key = {}

            for line in result.stdout.split('\n'):
                if not line:
                    continue

                parts = line.split(':')
                record_type = parts[0]

                if record_type == 'pub':
                    # Public key
                    if current_key:
                        keys.append(current_key)
                    current_key = {
                        'key_id': parts[4],
                        'created': parts[5],
                        'uid': None
                    }
                elif record_type == 'uid' and current_key:
                    # User ID
                    current_key['uid'] = parts[9]

            if current_key:
                keys.append(current_key)

            return keys

        except subprocess.CalledProcessError:
            return []

    def encrypt(self, content: str, recipient: Optional[str] = None) -> Tuple[bool, str]:
        """Encrypt content using GPG.

        Args:
            content: Plain text content to encrypt
            recipient: GPG key ID or email (defaults to configured key)

        Returns:
            Tuple of (success, encrypted_content_or_error_message)
        """
        if not self._gpg_available:
            return False, "GPG is not available on this system"

        recipient = recipient or self.key_id
        if not recipient:
            return False, "No GPG key configured. Set DIANE_GPG_KEY or use --gpg-key"

        try:
            result = subprocess.run(
                ['gpg', '--encrypt', '--armor', '--recipient', recipient, '--trust-model', 'always'],
                input=content.encode(),
                capture_output=True,
                check=True
            )

            encrypted = result.stdout.decode()
            return True, encrypted

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            return False, f"Encryption failed: {error_msg}"

    def decrypt(self, encrypted_content: str) -> Tuple[bool, str]:
        """Decrypt content using GPG.

        Args:
            encrypted_content: GPG encrypted content

        Returns:
            Tuple of (success, decrypted_content_or_error_message)
        """
        if not self._gpg_available:
            return False, "GPG is not available on this system"

        try:
            result = subprocess.run(
                ['gpg', '--decrypt', '--quiet'],
                input=encrypted_content.encode(),
                capture_output=True,
                check=True
            )

            decrypted = result.stdout.decode()
            return True, decrypted

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            return False, f"Decryption failed: {error_msg}"

    def encrypt_file(self, filepath: Path, recipient: Optional[str] = None) -> Tuple[bool, str]:
        """Encrypt a file in place.

        Args:
            filepath: Path to file to encrypt
            recipient: GPG key ID or email

        Returns:
            Tuple of (success, message)
        """
        if not filepath.exists():
            return False, f"File not found: {filepath}"

        # Read content
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return False, f"Failed to read file: {e}"

        # Encrypt
        success, result = self.encrypt(content, recipient)
        if not success:
            return False, result

        # Write encrypted content with .gpg extension
        encrypted_path = filepath.with_suffix(filepath.suffix + '.gpg')
        try:
            with open(encrypted_path, 'w', encoding='utf-8') as f:
                f.write(result)
        except Exception as e:
            return False, f"Failed to write encrypted file: {e}"

        # Remove original file
        try:
            filepath.unlink()
        except Exception as e:
            return False, f"Failed to remove original file: {e}"

        return True, f"Encrypted to {encrypted_path.name}"

    def decrypt_file(self, filepath: Path) -> Tuple[bool, str]:
        """Decrypt a file in place.

        Args:
            filepath: Path to encrypted file

        Returns:
            Tuple of (success, message)
        """
        if not filepath.exists():
            return False, f"File not found: {filepath}"

        # Read encrypted content
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                encrypted_content = f.read()
        except Exception as e:
            return False, f"Failed to read file: {e}"

        # Decrypt
        success, result = self.decrypt(encrypted_content)
        if not success:
            return False, result

        # Determine original filename (remove .gpg extension)
        if filepath.suffix == '.gpg':
            decrypted_path = filepath.with_suffix('')
        else:
            decrypted_path = filepath.with_suffix('.decrypted' + filepath.suffix)

        # Write decrypted content
        try:
            with open(decrypted_path, 'w', encoding='utf-8') as f:
                f.write(result)
        except Exception as e:
            return False, f"Failed to write decrypted file: {e}"

        # Remove encrypted file
        try:
            filepath.unlink()
        except Exception as e:
            return False, f"Failed to remove encrypted file: {e}"

        return True, f"Decrypted to {decrypted_path.name}"


def setup_gpg_key() -> Optional[str]:
    """Interactive GPG key setup.

    Returns:
        Selected key ID or None
    """
    encryptor = GPGEncryption()

    if not encryptor._gpg_available:
        print("❌ GPG is not available on this system.")
        print("Install GPG with: apt install gnupg (Debian/Ubuntu) or brew install gnupg (macOS)")
        return None

    keys = encryptor.list_keys()

    if not keys:
        print("❌ No GPG keys found.")
        print("Generate a key with: gpg --gen-key")
        return None

    print("📋 Available GPG keys:")
    print()
    for i, key in enumerate(keys, 1):
        print(f"{i}. {key['uid']}")
        print(f"   Key ID: {key['key_id']}")
        print()

    try:
        choice = input("Select a key (number): ").strip()
        idx = int(choice) - 1

        if 0 <= idx < len(keys):
            selected_key = keys[idx]['key_id']
            print(f"\n✅ Selected key: {selected_key}")
            print(f"\nTo use this key, set the environment variable:")
            print(f"export DIANE_GPG_KEY='{selected_key}'")
            return selected_key
        else:
            print("❌ Invalid selection")
            return None

    except (ValueError, KeyboardInterrupt):
        print("\n❌ Cancelled")
        return None
