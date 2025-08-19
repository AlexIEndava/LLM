from flask import Blueprint, request, jsonify
import tempfile
import os
from backend.services.llm_client import transcribe_audio, translate_to_english

bp = Blueprint('speech_to_text', __name__)

@bp.route('/speech-to-text/', methods=['POST'])
def speech_to_text():
    audio = request.files.get('audio')
    if not audio:
        return jsonify({'text': ''}), 400

    print(f"Received audio: {audio.filename if audio else 'None'}")

    # Save audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_audio:
        audio.save(temp_audio)
        temp_audio_path = temp_audio.name

    try:
        with open(temp_audio_path, "rb") as f:
            original_text = transcribe_audio(f)
            translated_text, _ = translate_to_english(original_text)
    except Exception as e:
        print(f"Speech-to-text error: {e}")
        translated_text = ""
    finally:
        os.remove(temp_audio_path)

    print(f"Transcribed text: {original_text}")
    print(f"Transcribed text: {translated_text}")

    return jsonify({'text': translated_text})