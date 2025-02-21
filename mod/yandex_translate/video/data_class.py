from dataclasses import dataclass


@dataclass
class TranslateResult:
    status: int
    audio_url: str
    error: str
    remaining_time_s: int
