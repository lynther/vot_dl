import subprocess
from concurrent.futures import Future, ProcessPoolExecutor
from pathlib import Path

from .data_class import TranslateVideoResult, VideoDownloadResult


def translate_video(
    video_download_result: VideoDownloadResult,
    temp_dir_audio: Path,
) -> TranslateVideoResult | None:
    audio_file_name = f"{video_download_result.video_name}.mp3"

    try:
        result = subprocess.run(
            [
                "vot-cli",
                video_download_result.video_url,
                "--output",
                temp_dir_audio,
                "--output-file",
                audio_file_name,
            ],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except FileNotFoundError:
        print('Установите "vot-cli"!')
        return None

    if result.stderr:
        print("Возникла ошибка при переводе видео")
        print(result.stderr)
        return None

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
            futures.append(executor.submit(translate_video, video_download_result, temp_dir_audio))

    for future in futures:
        if future.result():
            translate_video_results.append(future.result())

    return translate_video_results
