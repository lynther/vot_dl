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


def worker(url: str, temp_dir_video: Path) -> VideoDownloadResult | None:
    with YoutubeDL(params={"logger": NoLogger()}) as dl:
        info = dl.extract_info(url, download=False)

    if info["title"].endswith(info["ext"]):
        video_name = info["title"]
        outtmpl = f"{temp_dir_video}/%(title)s"
    else:
        video_name = f"{info['title']}.{info['ext']}"
        outtmpl = f"{temp_dir_video}/%(title)s.%(ext)s"

    yt_dlp_params = {
        "outtmpl": outtmpl,
        "logger": NoLogger(),
    }

    with YoutubeDL(params=yt_dlp_params) as dl:
        dl.download(url)

    print(f'> "{url}"')

    return VideoDownloadResult(
        video_url=url,
        video_name=video_name,
        video_file_path=Path(temp_dir_video, video_name),
    )


def download_videos(urls_file_path: Path, temp_dir_video: Path, workers: int = 1) -> list[VideoDownloadResult]:
    video_download_results: list[VideoDownloadResult] = []
    futures: list[Future] = []

    with (
        ProcessPoolExecutor(max_workers=workers) as executor,
        urls_file_path.open() as urls_file,
    ):
        for url in urls_file:
            futures.append(executor.submit(worker, url.rstrip(), temp_dir_video))

    for future in futures:
        if future.result():
            video_download_results.append(future.result())

    return video_download_results
