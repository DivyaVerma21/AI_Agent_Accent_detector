import sys

import streamlit as st
import os
import subprocess
import json
import tempfile
import requests



st.set_page_config(page_title="English Accent Evaluator", layout="centered")
st.title("English Accent Evaluator")

video_url = st.text_input("Enter Video URL ( .mp4):")

if st.button("Process Video"):
    if video_url:
        with st.spinner("Downloading video and extracting audio..."):
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    audio_output_path = os.path.join(temp_dir, "audio.wav")
                    # Run media_handler.py to download and extract audio
                    result = subprocess.run(
                        [sys.executable, "extract_audio.py", video_url, audio_output_path],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode != 0:
                        st.error(f"Error during video/audio processing: {result.stderr}")
                    elif not os.path.exists(audio_output_path):
                        st.error("Audio extraction failed.")
                    else:
                        st.info("Video downloaded and audio extracted successfully.")
                        with st.spinner("Running accent analysis..."):
                            try:
                                analysis_result = subprocess.run(
                                    [sys.executable, "accent_analyzer.py", audio_output_path],
                                    capture_output=True,
                                    text=True
                                )
                                if analysis_result.returncode != 0:
                                    st.error(f"Error during accent analysis: {analysis_result.stderr}")
                                else:
                                    try:
                                        results_dict = json.loads(analysis_result.stdout)
                                        st.subheader("Accent Analysis Results")
                                        st.metric("Predicted Accent", results_dict.get("accent_label", "N/A"))
                                        st.metric("Confidence", f"{results_dict.get('score', 0.0):.2f}")
                                        if "probabilities" in results_dict:
                                            with st.expander("Accent Probabilities"):
                                                for i, prob in enumerate(results_dict["probabilities"]):
                                                    st.write(f"Class {i}: {prob:.2f}")
                                    except json.JSONDecodeError:
                                        st.error("Error decoding accent analysis results.")
                                        st.text_area("Raw Analysis Output:", analysis_result.stdout)
                            except subprocess.CalledProcessError as e:
                                st.error(f"Error during accent analysis: {e.stderr}")
            except subprocess.CalledProcessError as e:
                st.error(f"Error during video/audio processing: {e.stderr}")
    else:
        st.warning("Please enter a valid video URL.")
