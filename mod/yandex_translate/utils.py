import hashlib
import hmac
from pathlib import Path

import httpx

from . import yandex_proto


def download_audio(url: str, mp3_path: Path):
    with mp3_path.open("wb") as f:
        response = httpx.get(url)
        f.write(response.content)


def build_video_req(url: str, req_lang: str = "en", res_lang: str = "ru") -> str:
    video_req = yandex_proto.VideoTranslationRequest()
    video_req.url = url
    video_req.duration = 341
    video_req.language = req_lang
    video_req.responseLanguage = res_lang
    video_req.firstRequest = True
    video_req.unknown2 = 1
    video_req.unknown3 = video_req.unknown4 = video_req.unknown5 = 0

    return video_req.SerializeToString()


def get_signature(request: str):
    return hmac.new(
        b"bt8xH3VOlb4mqf0nqAibnDOoiPlXsisf",
        msg=request,
        digestmod=hashlib.sha256,
    ).hexdigest()
