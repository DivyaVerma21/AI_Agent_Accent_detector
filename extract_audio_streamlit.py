import subprocess
import os

def extract_audio_from_url(video_url: str, output_path: str) -> None:
    """
    Downloads video from the URL and extracts audio as WAV to output_path.
    Requires yt-dlp and ffmpeg installed.
    """
    # Build the output template for yt-dlp
    output_template = output_path + ".%(ext)s"

    cmd = [
        "yt-dlp",
        "-x",
        "--audio-format", "wav",
        "-o", output_template,
        video_url
    ]

    subprocess.run(cmd, check=True)

    wav_file = output_path + ".wav"
    if os.path.exists(wav_file):
        os.rename(wav_file, output_path)
    else:
        raise FileNotFoundError(f"Expected audio file {wav_file} not found.")
