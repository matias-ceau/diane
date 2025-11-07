"""Audio recording and transcription for diane."""

import os
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
import shutil


class AudioRecorder:
    """Handle audio recording with auto-detection of available tools."""

    def __init__(self):
        self.tool = self._detect_recording_tool()
        self.temp_dir = Path(os.environ.get('DIANE_AUDIO_TEMP', '/tmp/diane-audio'))
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def _detect_recording_tool(self) -> Optional[str]:
        """Auto-detect available audio recording tools on Linux.

        Priority order:
        1. pw-record (PipeWire) - modern, most common on recent systems
        2. arecord (ALSA) - traditional, widely available
        3. ffmpeg - fallback, usually available

        Returns:
            Tool name if found, None otherwise
        """
        tools = ['pw-record', 'arecord', 'ffmpeg']

        for tool in tools:
            if shutil.which(tool):
                return tool

        return None

    def is_available(self) -> bool:
        """Check if audio recording is available."""
        return self.tool is not None

    def get_tool_name(self) -> str:
        """Get the name of the detected recording tool."""
        return self.tool or "none"

    def list_devices(self) -> list:
        """List available audio input devices.

        Returns:
            List of device names/descriptions
        """
        if not self.is_available():
            return []

        try:
            if self.tool == 'pw-record':
                # List PipeWire sources
                result = subprocess.run(
                    ['pw-cli', 'list-objects', 'Node'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                # Parse output for audio sources (simplified)
                devices = []
                for line in result.stdout.split('\n'):
                    if 'node.description' in line:
                        # Extract description
                        desc = line.split('=')[1].strip().strip('"')
                        devices.append(desc)
                return devices

            elif self.tool == 'arecord':
                # List ALSA devices
                result = subprocess.run(
                    ['arecord', '-l'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                return [line.strip() for line in result.stdout.split('\n') if line.strip()]

        except Exception:
            pass

        return ["Default device"]

    def record(
        self,
        duration: Optional[int] = None,
        device: Optional[str] = None,
        format: str = 'wav'
    ) -> Tuple[bool, str, Optional[Path]]:
        """Record audio from microphone.

        Args:
            duration: Recording duration in seconds (None = until Ctrl-C)
            device: Audio device to use (None = default)
            format: Audio format (default: wav)

        Returns:
            Tuple of (success, message, audio_file_path)
        """
        if not self.is_available():
            return False, f"No recording tool available. Install: pw-record, arecord, or ffmpeg", None

        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        filename = f"diane-recording-{timestamp}.{format}"
        audio_path = self.temp_dir / filename

        try:
            if self.tool == 'pw-record':
                return self._record_pipewire(audio_path, duration, device)
            elif self.tool == 'arecord':
                return self._record_alsa(audio_path, duration, device)
            elif self.tool == 'ffmpeg':
                return self._record_ffmpeg(audio_path, duration, device)
            else:
                return False, "No recording tool available", None

        except KeyboardInterrupt:
            # User cancelled - still return the file if it exists
            if audio_path.exists() and audio_path.stat().st_size > 0:
                return True, "Recording stopped", audio_path
            return False, "Recording cancelled", None

        except Exception as e:
            return False, f"Recording error: {e}", None

    def _record_pipewire(
        self,
        output_path: Path,
        duration: Optional[int],
        device: Optional[str]
    ) -> Tuple[bool, str, Optional[Path]]:
        """Record using PipeWire (pw-record)."""
        cmd = ['pw-record']

        if device:
            cmd.extend(['--target', device])

        # Quality settings
        cmd.extend([
            '--rate', '16000',  # 16kHz good for speech
            '--channels', '1',   # Mono
        ])

        cmd.append(str(output_path))

        try:
            if duration:
                # Record for specific duration
                subprocess.run(cmd, timeout=duration + 2, check=True)
            else:
                # Record until Ctrl-C
                subprocess.run(cmd, check=True)

            if output_path.exists() and output_path.stat().st_size > 0:
                return True, f"Recorded to {output_path.name}", output_path
            else:
                return False, "Recording failed - empty file", None

        except subprocess.TimeoutExpired:
            # Duration reached
            if output_path.exists() and output_path.stat().st_size > 0:
                return True, f"Recorded {duration}s to {output_path.name}", output_path
            return False, "Recording timeout", None

    def _record_alsa(
        self,
        output_path: Path,
        duration: Optional[int],
        device: Optional[str]
    ) -> Tuple[bool, str, Optional[Path]]:
        """Record using ALSA (arecord)."""
        cmd = ['arecord']

        if device:
            cmd.extend(['-D', device])

        # Quality settings
        cmd.extend([
            '-f', 'cd',          # CD quality
            '-c', '1',           # Mono
            '-r', '16000',       # 16kHz
        ])

        if duration:
            cmd.extend(['-d', str(duration)])

        cmd.append(str(output_path))

        try:
            subprocess.run(cmd, check=True)

            if output_path.exists() and output_path.stat().st_size > 0:
                duration_msg = f" ({duration}s)" if duration else ""
                return True, f"Recorded{duration_msg} to {output_path.name}", output_path
            else:
                return False, "Recording failed - empty file", None

        except Exception as e:
            return False, f"arecord error: {e}", None

    def _record_ffmpeg(
        self,
        output_path: Path,
        duration: Optional[int],
        device: Optional[str]
    ) -> Tuple[bool, str, Optional[Path]]:
        """Record using ffmpeg (fallback)."""
        cmd = ['ffmpeg', '-y']  # -y to overwrite

        # Input device
        input_device = device or 'default'
        cmd.extend([
            '-f', 'alsa',
            '-i', input_device,
            '-ac', '1',          # Mono
            '-ar', '16000',      # 16kHz
        ])

        if duration:
            cmd.extend(['-t', str(duration)])

        cmd.append(str(output_path))

        try:
            subprocess.run(
                cmd,
                check=True,
                capture_output=True,  # Hide ffmpeg verbose output
                timeout=duration + 5 if duration else None
            )

            if output_path.exists() and output_path.stat().st_size > 0:
                duration_msg = f" ({duration}s)" if duration else ""
                return True, f"Recorded{duration_msg} to {output_path.name}", output_path
            else:
                return False, "Recording failed - empty file", None

        except subprocess.TimeoutExpired:
            if output_path.exists() and output_path.stat().st_size > 0:
                return True, f"Recorded {duration}s to {output_path.name}", output_path
            return False, "Recording timeout", None
        except Exception as e:
            return False, f"ffmpeg error: {e}", None


class AudioTranscriber:
    """Handle audio transcription using OpenAI Whisper API."""

    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        self.model = os.environ.get('DIANE_TRANSCRIBE_MODEL', 'gpt-4o-audio-preview')

    def is_available(self) -> bool:
        """Check if transcription is available (API key configured)."""
        return self.api_key is not None

    def transcribe(self, audio_path: Path) -> Tuple[bool, str, Optional[str]]:
        """Transcribe audio file to text.

        Args:
            audio_path: Path to audio file

        Returns:
            Tuple of (success, message, transcription_text)
        """
        if not self.is_available():
            return False, "OPENAI_API_KEY not set. Set it to enable transcription.", None

        if not audio_path.exists():
            return False, f"Audio file not found: {audio_path}", None

        try:
            import openai
        except ImportError:
            return False, "openai package not installed. Run: pip install openai", None

        try:
            client = openai.OpenAI(api_key=self.api_key)

            # Read audio file
            with open(audio_path, 'rb') as audio_file:
                # Use Whisper API for transcription
                response = client.audio.transcriptions.create(
                    model="whisper-1",  # Whisper model
                    file=audio_file,
                    response_format="text"
                )

            transcription = response.strip()

            if transcription:
                return True, "Transcription successful", transcription
            else:
                return False, "Transcription returned empty result", None

        except Exception as e:
            return False, f"Transcription error: {e}", None

    def transcribe_and_cleanup(
        self,
        audio_path: Path,
        keep_on_failure: bool = True
    ) -> Tuple[bool, str, Optional[str]]:
        """Transcribe audio and optionally clean up file.

        Args:
            audio_path: Path to audio file
            keep_on_failure: If True, keep audio file when transcription fails

        Returns:
            Tuple of (success, message, transcription_text)
        """
        success, msg, transcription = self.transcribe(audio_path)

        # Clean up audio file based on result
        if success:
            # Transcription succeeded - safe to delete audio
            try:
                audio_path.unlink()
            except Exception:
                pass  # Ignore cleanup errors
        elif not keep_on_failure:
            # Failed and user doesn't want to keep it
            try:
                audio_path.unlink()
            except Exception:
                pass

        return success, msg, transcription


def get_audio_recorder() -> AudioRecorder:
    """Get AudioRecorder instance."""
    return AudioRecorder()


def get_audio_transcriber() -> AudioTranscriber:
    """Get AudioTranscriber instance."""
    return AudioTranscriber()
