import os
import sys
import tempfile
import requests
import yt_dlp
from moviepy.editor import VideoFileClip
import shutil

def download_video(url: str, output_path: str) -> str:
    temp_video_path = os.path.join(output_path, "video.mp4")

    try:
        if "youtube.com" in url or "youtu.be" in url:
            print("[INFO] Downloading YouTube video using yt-dlp...")
            ydl_opts = {
                'outtmpl': temp_video_path,
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
                'quiet': True,
                'no_warnings': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"[INFO] Downloaded YouTube video to: {temp_video_path}")
        elif url.endswith(".mp4"):
            print("[INFO] Downloading direct MP4 video...")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(temp_video_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"[INFO] Downloaded direct MP4 to: {temp_video_path}")
        else:
            raise ValueError("Unsupported video URL format.")
    except Exception as e:
        print(f"[ERROR] Video download failed: {e}")
        raise

    return temp_video_path

def extract_audio(video_path: str, output_audio_path: str = "audio.wav") -> str:
    try:
        print(f"[INFO] Extracting audio from: {video_path}")
        clip = VideoFileClip(video_path)
        audio = clip.audio
        audio.write_audiofile(output_audio_path, codec='pcm_s16le')  # .wav format
        clip.close()
        print(f"[INFO] Audio saved to: {output_audio_path}")
        return output_audio_path
    except Exception as e:
        print(f"[ERROR] Audio extraction failed: {e}")
        raise

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_audio.py <video_url> [output_audio_path]")
        sys.exit(1)

    video_url = sys.argv[1]
    output_audio_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.getcwd(), "final_audio.wav")
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            video_path = download_video(video_url, temp_dir)
            temp_audio_path = extract_audio(video_path, os.path.join(temp_dir, "audio.wav"))
            print(f"[SUCCESS] Temporary audio file at: {temp_audio_path}")

            # Save/copy the audio file to the desired output path
            shutil.copy(temp_audio_path, output_audio_path)
            print(f"[INFO] Audio file copied to: {output_audio_path}")

        except Exception as e:
            print(f"[FAILED] {e}")
