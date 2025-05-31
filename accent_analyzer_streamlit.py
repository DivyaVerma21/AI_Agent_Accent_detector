import sys
import os
import json
from speechbrain.inference.interfaces import foreign_class
from pydub import AudioSegment
import uuid

def preprocess_audio(input_path, max_duration_ms=30000, target_sample_rate=16000):
    audio = AudioSegment.from_file(input_path)
    audio = audio[:max_duration_ms]
    audio = audio.set_frame_rate(target_sample_rate)

    # Save to same directory as script, with unique filename
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = f"temp_audio_{uuid.uuid4().hex}.wav"
    output_path = os.path.join(script_dir, filename)
    audio.export(output_path, format="wav")
    return filename, output_path  # return both

def classify_accent(filename):
    classifier = foreign_class(
        source="Jzuluaga/accent-id-commonaccent_xlsr-en-english",
        pymodule_file="custom_interface.py",
        classname="CustomEncoderWav2vec2Classifier"
    )
    out_prob, score, index, text_lab = classifier.classify_file(filename)

    if isinstance(text_lab, (list, tuple)):
        text_lab = text_lab[0]

    score_value = score.item() if hasattr(score, "item") else float(score)
    prob_list = out_prob.tolist()[0] if hasattr(out_prob, "tolist") else list(map(float, out_prob))

    return {
        "accent_label": text_lab,
        "score": score_value,
        "probabilities": prob_list
    }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python accent_analyzer_streamlit.py <audio_path.wav>"}))
        sys.exit(1)

    input_audio = sys.argv[1]
    if not os.path.isfile(input_audio):
        print(json.dumps({"error": f"Audio file not found: {input_audio}"}))
        sys.exit(1)

    try:
        filename, output_path = preprocess_audio(input_audio)
        result = classify_accent(filename)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
    finally:
        try:
            if 'output_path' in locals() and os.path.isfile(output_path):
                os.remove(output_path)
        except Exception:
            pass

if __name__ == "__main__":
    main()
