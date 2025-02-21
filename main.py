import subprocess
from pathlib import Path

from mod.download import download_videos
from mod.merge import merge_audios
from mod.translate import translate_videos


def check_required_apps() -> bool:
    try:
        subprocess.run(["vot-cli"], check=True, capture_output=True)
        subprocess.run(["ffmpeg", "--help"], check=True, capture_output=True)
    except FileNotFoundError:
        return False

    return True


def main():
    if not check_required_apps():
        print("Без vot-cli или ffmpeg работать не будет :c")
        return

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

    if urls_file_path.stat().st_size == 0:
        print("Файл с ссылками пустой")
        return

    print("Скачивание видео:")

    if download_results := download_videos(urls_file_path, temp_dir_video):
        print("\n")
        print("Перевод  видео:")

        if translate_results := translate_videos(download_results, temp_dir_audio):
            print("\n")
            print("Объединение аудио дорожек:")
            merge_audios(translate_results, original_sound_ratio, output_dir)
        else:
            print("Нет результатов перевода")
    else:
        print("Нет результатов скачивания видео")


if __name__ == "__main__":
    main()
