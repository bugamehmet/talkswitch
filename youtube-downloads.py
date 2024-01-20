import logging
import os
from pathlib import Path
from moviepy.editor import AudioFileClip
from pytube import YouTube


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_video_url(url: str, output_path: str = "output", filename: str = "test"):
    try:
        yt = YouTube(url)

        Path(output_path).mkdir(parents=True, exist_ok=True)

        audio_stream = yt.streams.filter(only_audio=True).first()
        video_stream = yt.streams.filter(only_video=True).first()

        if audio_stream is None or video_stream is None:
            logging.warning("Bulunamadı!!")
            return None

        mp3_file_path = os.path.join(output_path, filename + ".mp3")
        mp4_file_path = os.path.join(output_path, filename + ".mp4")

        logging.info(f"Downloading MP3 Started... {mp3_file_path}")
        audio_stream.download(output_path=output_path, filename=filename + ".mp3")
        logging.info(f"MP3 Download Successful!")

        logging.info(f"Downloading MP4 Started... {mp4_file_path}")
        video_stream.download(output_path=output_path, filename=filename + ".mp4")
        logging.info(f"MP4 Download Successful!")

        return str(mp3_file_path), str(mp4_file_path)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None

url = "https://www.youtube.com/watch?v=4RixMPF4xis"
get_video_url(url, "audio", "deneme")