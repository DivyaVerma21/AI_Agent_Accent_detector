# English Accent Evaluator

This project provides an AI-powered tool to evaluate English accents from video links (YouTube or direct MP4). It downloads the video, extracts the audio, and predicts the accent using a deep learning model.

## Features

- Accepts  .mp4 video URLs
- Downloads and extracts high-quality audio automatically
- Analyzes the accent using a SpeechBrain-based classifier
- User-friendly Streamlit web interface
- Dockerized for easy deployment

## Usage

### 1. Install Requirements

Install system dependencies (Linux/Ubuntu):

sudo apt-get update
xargs -a packages.txt sudo apt-get install -y

text

Install Python dependencies:

pip install -r requirements.txt

text

### 2. Run the Streamlit App

streamlit run app.py

text

### 3. Using the Web App

- Enter a YouTube or MP4 video link.
- Click "Process Video".
- Wait for the audio extraction and accent analysis.
- View the predicted accent and confidence score.

## File Overview

| File                | Purpose                                                      |
|---------------------|--------------------------------------------------------------|
| app.py              | Streamlit web interface                                      |
| extract_audio.py    | Downloads video and extracts audio as WAV                    |
| accent_analyzer.py  | Predicts accent from audio using SpeechBrain                 |
| requirements.txt    | Python dependencies                                          |
| packages.txt        | System dependencies (e.g., ffmpeg, cmake)                    |
| Dockerfile          | Containerizes the application                                |

## Docker

To run the app in a Docker container:

docker build -t accent-evaluator .
docker run -p 8501:8501 accent-evaluator

text

Then open `http://localhost:8501` in your browser.

## Notes

- Requires `ffmpeg` for audio/video processing.
- The SpeechBrain model is downloaded on first use and may require internet access.
- For best results, use videos with clear speech.

## License

MIT License

---