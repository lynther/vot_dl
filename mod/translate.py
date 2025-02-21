from concurrent.futures import Future, ProcessPoolExecutor
from pathlib import Path
from time import sleep

from mod.yandex_translate.utils import download_audio
from mod.yandex_translate.video import translate_video

from .data_class import TranslateVideoResult, VideoDownloadResult


def worker(
    video_download_result: VideoDownloadResult,
    temp_dir_audio: Path,
) -> TranslateVideoResult | None:
    audio_file_name = f"{video_download_result.video_name}.mp3"
    audio_file_path = Path(temp_dir_audio, audio_file_name)
    tr_result = translate_video(video_download_result.video_url)

    while tr_result.status == 2:
        tr_result = translate_video(video_download_result.video_url)
        sleep(tr_result.remaining_time_s)

    download_audio(tr_result.audio_url, audio_file_path)
    print(f'> "{video_download_result.video_url}"')

    return TranslateVideoResult(
        audio_file_path=Path(temp_dir_audio, audio_file_name),
        video_file_path=video_download_result.video_file_path,
        video_file_name=f"{video_download_result.video_name}.{video_download_result.video_ext}",
    )


def translate_videos(
    video_download_results: list[TranslateVideoResult],
    temp_dir_audio: Path,
) -> list[TranslateVideoResult]:
    translate_video_results: list[TranslateVideoResult] = []
    futures: list[Future] = []

    with ProcessPoolExecutor(max_workers=10) as executor:
        for video_download_result in video_download_results:
            futures.append(executor.submit(worker, video_download_result, temp_dir_audio))

    for future in futures:
        if future.result():
            translate_video_results.append(future.result())

    return translate_video_results
