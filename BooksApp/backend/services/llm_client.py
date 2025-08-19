from openai import OpenAI
from backend.utils.config import OPENAI_API_KEY
import base64


client = OpenAI(api_key=OPENAI_API_KEY)


def get_llm_response(question, system_prompt, model="gpt-4o-mini", temperature=0.2):
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

def get_embedding(text, model="text-embedding-3-small"):
    response = client.embeddings.create(
        input=[text],
        model=model
    )
    embedding = response.data[0].embedding
    # Poți returna și usage dacă există, dar la embeddings nu există usage ca la chat completions
    return embedding

def generate_and_save_image(prompt: str, filename: str, model: str = "dall-e-2", size: str = "512x512") -> str:
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

def transcribe_audio(file_obj, model="whisper-1"):
    try:
        transcript = client.audio.transcriptions.create(
            model=model,
            file=file_obj,
            response_format="text"
        )
        return transcript
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""

def translate_to_english(text, model="gpt-4o-mini"):
    system_prompt = "Translate the following text to English. Only return the translation, do not answer or explain."
    return get_llm_response(text, system_prompt, model=model)

