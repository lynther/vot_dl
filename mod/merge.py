import subprocess
from concurrent.futures import Future, ProcessPoolExecutor
from pathlib import Path

from .data_class import TranslateVideoResult


def merge_audio(
    audio_download_result: TranslateVideoResult,
    volume: float,
    output_dir: Path,
):
    output_path = Path(output_dir, audio_download_result.video_file_name)

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
        f"[0:a] volume={volume} [original];[original][1:a] amix=inputs=2:duration=longest [audio_out]",
        "-map",
        "0:v",
        "-map",
        "[audio_out]",
        "-y",
        output_path,
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
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
