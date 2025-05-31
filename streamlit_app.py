import streamlit as st
import os
import tempfile

from extract_audio_streamlit import extract_audio_from_url
from accent_analyzer_streamlit import classify_accent

st.set_page_config(page_title="English Accent Evaluator", layout="centered")
st.title("English Accent Evaluator")

video_url = st.text_input("Enter Video URL (.mp4):")

if st.button("Process Video"):
    if not video_url:
        st.warning("Please enter a valid video URL.")
    else:
        with st.spinner("Downloading video and extracting audio..."):
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    audio_output_path = os.path.join(temp_dir, "audio.wav")
                    extract_audio_from_url(video_url, audio_output_path)

                    if not os.path.exists(audio_output_path):
                        st.error("Audio extraction failed.")
                    else:
                        st.success("Audio extracted successfully.")
                        with st.spinner("Running accent analysis..."):
                            results_dict = classify_accent(audio_output_path)
                            st.subheader("Accent Analysis Results")
                            st.metric("Predicted Accent", results_dict.get("accent_label", "N/A"))
                            st.metric("Confidence", f"{results_dict.get('score', 0.0):.2f}")

                            if "probabilities" in results_dict:
                                with st.expander("Accent Probabilities"):
                                    for i, prob in enumerate(results_dict["probabilities"]):
                                        st.write(f"Class {i}: {prob:.2f}")

            except Exception as e:
                st.error(f"An error occurred: {e}")
