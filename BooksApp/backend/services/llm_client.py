from openai import OpenAI
from backend.utils.config import OPENAI_API_KEY
import base64


client = OpenAI(api_key=OPENAI_API_KEY)

model_response = "gpt-4o-mini"
model_embedding = "text-embedding-3-small"
model_image = "dall-e-2"
model_transcribe = "whisper-1"
model_synthesize_speech = "tts-1"
voice = "alloy"


def get_llm_response(question, system_prompt, model=model_response, temperature=0.2):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=temperature
        )
        content = response.choices[0].message.content
        usage = response.usage
        return content, usage
    except Exception as e:
        raise RuntimeError(f"Failed to get LLM response: {e}")

def get_embedding(text, model=model_embedding):
    try:
        response = client.embeddings.create(
            input=[text],
            model=model
        )
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        raise RuntimeError(f"Failed to get embedding: {e}")

def generate_and_save_image(prompt: str, filename: str, model: str = model_image, size: str = "512x512") -> str:
    try:
        result = client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            response_format="b64_json"
        )
        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)
        with open(filename, "wb") as f:
            f.write(image_bytes)
        return filename
    except Exception as e:
        raise RuntimeError(f"Failed to generate and save image: {e}")

def transcribe_audio(file_obj, model=model_transcribe):
    try:
        transcript = client.audio.transcriptions.create(
            model=model,
            file=file_obj,
            response_format="text"
        )
        return transcript
    except Exception as e:
        raise RuntimeError(f"Transcription error: {e}")

def translate_to_english(text, model=model_response):
    system_prompt = "Translate the following text to English. Only return the translation, do not answer or explain."
    try:
        return get_llm_response(text, system_prompt, model=model)
    except Exception as e:
        raise RuntimeError(f"Failed to translate to English: {e}")

def synthesize_speech(text, voice=voice, model=model_synthesize_speech):
    import tempfile
    try:
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(response.content)
            return tmp.name
    except Exception as e:
        raise RuntimeError(f"Failed to synthesize speech: {e}")

