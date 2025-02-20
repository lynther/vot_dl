import subprocess
from concurrent.futures import Future, ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from yt_dlp import YoutubeDL


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


class NoLogger:
    def debug(self, msg: str):
        pass

    def info(self, msg: str):
        pass

    def warning(self, msg: str):
        pass

    def error(self, msg: str):
        pass

    def critical(self, msg: str):
        pass


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


def download_video(url: str, temp_dir_video: Path) -> VideoDownloadResult | None:
    yt_dlp_params = {
        "noprogress": True,
        "outtmpl": f"{temp_dir_video}/%(id)s.%(ext)s",
        "logger": NoLogger(),
    }

    with YoutubeDL(params=yt_dlp_params) as dl:
        info = dl.extract_info(url, download=False)

    video_file_name = f"{info['id']}.{info['ext']}"

    with YoutubeDL(params=yt_dlp_params) as dl:
        dl.download(url)

    print(f'> "{url}"')

    return VideoDownloadResult(
        video_url=url,
        video_name=info["id"],
        video_ext=info["ext"],
        video_file_path=Path(temp_dir_video, video_file_name),
    )


def download_videos(urls_file_path: Path, temp_dir_video: Path) -> list[VideoDownloadResult]:
    video_download_results: list[VideoDownloadResult] = []
    futures: list[Future] = []

    with (
        ProcessPoolExecutor(max_workers=5) as executor,
        urls_file_path.open() as urls_file,
    ):
        for url in urls_file:
            futures.append(executor.submit(download_video, url.rstrip(), temp_dir_video))

    for future in futures:
        if future.result():
            video_download_results.append(future.result())

    return video_download_results


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


def merge_audio(
    audio_download_result: TranslateVideoResult,
    original_sound_ratio: float,
    output_dir: Path,
):
    output_path = Path(output_dir, audio_download_result.video_file_name)
    filter_complex = [
        f"[0:a] volume={original_sound_ratio} [original];[original][1:a]",
        " amix=inputs=2:duration=longest [audio_out]",
    ]

    cmd = [
        "ffmpeg",
        "-i",
        audio_download_result.video_file_path,
        "-i",
        audio_download_result.audio_file_path,
        "-c:v",
        "copy",
        "-b:a",
        "128k",
        "-filter_complex",
        "".join(filter_complex),
        "-map",
        "0:v",
        "-map",
        "[audio_out]",
        "-y",
        output_path,
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        print("Для объединения дорожки требуется ffmpeg!")
        return
    except subprocess.CalledProcessError as e:
        print(f"{audio_download_result.video_file_path} - {e.stderr}")
        return

    print(f"> {output_path}")


def merge_audios(
    translate_video_results: list[TranslateVideoResult],
    original_sound_ratio: float,
    output_dir: Path,
):
    futures: list[Future] = []

    with ProcessPoolExecutor(max_workers=5) as executor:
        for audio_download_result in translate_video_results:
            futures.append(
                executor.submit(
                    merge_audio,
                    audio_download_result,
                    original_sound_ratio,
                    output_dir,
                ),
            )
    for future in futures:
        if future.result():
            print(future.result())


def main():
    original_sound_ratio = 0.7
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)

    temp_dir_audio = Path(temp_dir, "audio")
    temp_dir_audio.mkdir(exist_ok=True)

    temp_dir_video = Path(temp_dir, "video")
    temp_dir_video.mkdir(exist_ok=True)

    urls_file_path = Path("urls.txt")

    if not urls_file_path.exists():
        print("Файл с ссылками не существует")
        return

    print("Скачивание видео:")

    video_download_results = download_videos(urls_file_path, temp_dir_video)
    print("\n")
    print("Перевод  видео:")

    translate_video_results = translate_videos(video_download_results, temp_dir_audio)
    print("\n")
    print("Объединение аудио дорожек:")
    merge_audios(translate_video_results, original_sound_ratio, output_dir)


if __name__ == "__main__":
    main()
