from flask import Blueprint, request, send_file, jsonify, after_this_request

import os
from backend.services.llm_client import synthesize_speech

bp = Blueprint('tts', __name__)

@bp.route('/tts/', methods=['POST'])
def tts():
    data = request.get_json()
    text = data.get('text', '')
    voice = data.get('voice', 'alloy')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        audio_path = synthesize_speech(text, voice=voice)

        @after_this_request
        def remove_file(response):
            try:
                os.remove(audio_path)
            except Exception as e:
                print(f"Error deleting temp file: {e}")
            return response

        return send_file(audio_path, mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 500