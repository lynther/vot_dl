from dataclasses import dataclass
from pathlib import Path


@dataclass
class VideoDownloadResult:
    video_url: str
    video_name: str
    video_ext: str
    video_file_path: Path


@dataclass
class TranslateVideoResult:
    audio_file_path: Path
    video_file_path: Path
    video_file_name: str
