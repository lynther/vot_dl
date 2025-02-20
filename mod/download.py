from concurrent.futures import Future, ProcessPoolExecutor
from pathlib import Path

from yt_dlp import YoutubeDL

from .data_class import VideoDownloadResult


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
