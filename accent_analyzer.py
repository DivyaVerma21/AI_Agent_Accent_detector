import sys
import os
import json
from speechbrain.inference.interfaces import foreign_class
from pydub import AudioSegment
import tempfile

def preprocess_audio(input_path, max_duration_ms=30000, target_sample_rate=16000):
    """
    Load audio, trim to max_duration_ms, resample to target_sample_rate,
    export to a temporary WAV file, and return its absolute path.
    """
    audio = AudioSegment.from_file(input_path)
    audio = audio[:max_duration_ms]  # Trim to max length
    audio = audio.set_frame_rate(target_sample_rate)  # Resample to 16kHz

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(temp_file.name, format="wav")
    temp_file.close()

    return os.path.abspath(temp_file.name)

def classify_accent(audio_path):
    # Normalize and avoid double prefixing by making path relative if absolute
    audio_path = os.path.normpath(audio_path)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.isabs(audio_path):
        try:
            audio_path = os.path.relpath(audio_path, script_dir)
        except ValueError:
            pass  # fallback to absolute if relpath fails

    print(f"[DEBUG] classify_file called with: {audio_path}", file=sys.stderr)
    print(f"[DEBUG] Is absolute? {os.path.isabs(audio_path)}", file=sys.stderr)

    classifier = foreign_class(
        source="Jzuluaga/accent-id-commonaccent_xlsr-en-english",
        pymodule_file="custom_interface.py",
        classname="CustomEncoderWav2vec2Classifier"
    )

    out_prob, score, index, text_lab = classifier.classify_file(audio_path)

    # Ensure proper formatting of results
    if isinstance(text_lab, (list, tuple)) and len(text_lab) > 0:
        text_lab = text_lab[0]  # Convert list like ['label'] to 'label'

    score_value = score.item() if hasattr(score, "item") else float(score)
    prob_list = out_prob.tolist()[0] if hasattr(out_prob, "tolist") else list(map(float, out_prob))

    return {
        "accent_label": text_lab,
        "score": score_value,
        "probabilities": prob_list
    }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python accent_analyzer.py <audio_path.wav>"}))
        sys.exit(1)

    input_audio = sys.argv[1]
    if not os.path.isfile(input_audio):
        print(json.dumps({"error": f"Audio file not found: {input_audio}"}))
        sys.exit(1)

    try:
        processed_audio = preprocess_audio(input_audio)
        result = classify_accent(processed_audio)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
    finally:
        try:
            if 'processed_audio' in locals() and os.path.isfile(processed_audio):
                os.remove(processed_audio)
        except Exception:
            pass

if __name__ == "__main__":
    main()
