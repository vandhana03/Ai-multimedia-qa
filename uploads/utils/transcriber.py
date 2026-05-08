import os
import shutil
from pathlib import Path

import whisper

_model = None


class TranscriptionSetupError(RuntimeError):
    """Raised when local transcription prerequisites are missing."""


class TranscriptionProcessingError(RuntimeError):
    """Raised when a media file cannot be transcribed."""


def _format_mmss(seconds_value):
    try:
        total_seconds = max(0, int(float(seconds_value)))
    except (TypeError, ValueError):
        total_seconds = 0
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"


def _build_timestamped_text(segments):
    lines = []
    for segment in segments or []:
        if not isinstance(segment, dict):
            continue
        text = str(segment.get("text", "")).strip()
        if not text:
            continue
        start = _format_mmss(segment.get("start", 0))
        lines.append(f"[{start}] {text}")
    return "\n".join(lines)


def get_model():
    global _model
    if _model is None:
        _model = whisper.load_model("base")
    return _model


def _ensure_ffmpeg_installed():
    # Prefer system ffmpeg, but fall back to the binary provided by imageio-ffmpeg.
    if shutil.which("ffmpeg") is not None:
        return

    try:
        from imageio_ffmpeg import get_ffmpeg_exe
    except Exception as exc:
        raise TranscriptionSetupError(
            "ffmpeg is missing. Install ffmpeg system-wide or add imageio-ffmpeg."
        ) from exc

    ffmpeg_exe = Path(get_ffmpeg_exe())
    if not ffmpeg_exe.exists():
        raise TranscriptionSetupError(
            "imageio-ffmpeg is installed, but ffmpeg executable was not found."
        )

    # On Windows the bundled executable may not be named exactly `ffmpeg.exe`.
    # Whisper invokes `ffmpeg` by name, so create a local alias if needed.
    expected_name = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
    ffmpeg_alias = ffmpeg_exe.with_name(expected_name)
    if ffmpeg_exe.name.lower() != expected_name.lower() and not ffmpeg_alias.exists():
        try:
            shutil.copy2(ffmpeg_exe, ffmpeg_alias)
        except OSError as exc:
            raise TranscriptionSetupError(
                "Found bundled ffmpeg, but could not create ffmpeg alias."
            ) from exc

    ffmpeg_target = ffmpeg_alias if ffmpeg_alias.exists() else ffmpeg_exe
    ffmpeg_dir = str(ffmpeg_target.parent)
    current_path = os.environ.get("PATH", "")

    # Make whisper's subprocess('ffmpeg', ...) resolve the bundled binary.
    if ffmpeg_dir not in current_path:
        os.environ["PATH"] = f"{ffmpeg_dir}{os.pathsep}{current_path}"

    if shutil.which("ffmpeg") is None:
        raise TranscriptionSetupError(
            "ffmpeg binary could not be resolved. Restart server after installing ffmpeg."
        )


def transcribe_file(path):
    _ensure_ffmpeg_installed()
    model = get_model()
    try:
        result = model.transcribe(path)
    except RuntimeError as exc:
        error_text = str(exc)
        if "Output file does not contain any stream" in error_text:
            raise TranscriptionProcessingError(
                "The uploaded video has no audio track. Upload a video with audio."
            ) from exc
        raise TranscriptionProcessingError(
            "Transcription failed for this media file."
        ) from exc
    if isinstance(result, dict):
        result["timestamped_text"] = _build_timestamped_text(result.get("segments"))
    return result