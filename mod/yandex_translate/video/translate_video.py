from uuid import uuid4 as uuid

import httpx
from google.protobuf import message

from ...yandex_translate import yandex_proto
from ...yandex_translate.utils import build_video_req, get_signature
from ...yandex_translate.video.data_class import TranslateResult

YANDEX_URL = "https://api.browser.yandex.ru/video-translation/translate"
USER_AGENT = """
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
 Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36
""".replace("\n", "")


def translate_video(url: str, req_lang: str = "en", res_lang: str = "ru") -> TranslateResult:
    video_req = build_video_req(url, req_lang, res_lang)

    headers = {
        "Accept": "application/x-protobuf",
        "Content-Type": "application/x-protobuf",
        "Accept-Language": "en",
        "User-Agent": USER_AGENT,
        "Vtrans-Signature": get_signature(video_req),
        "Sec-Vtrans-Token": uuid().hex,
    }

    response = httpx.post(YANDEX_URL, data=video_req, headers=headers)
    translate_res = yandex_proto.VideoTranslationResponse()

    try:
        translate_res.ParseFromString(response.content)
    except message.DecodeError:
        return TranslateResult(error="Yandex video translation error")

    return TranslateResult(
        audio_url=translate_res.url,
        status=translate_res.status,
        error="",
        remaining_time_s=translate_res.remainingTime if translate_res.status else -1,
    )
