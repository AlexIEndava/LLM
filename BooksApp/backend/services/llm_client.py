from openai import OpenAI
from backend.utils.config import OPENAI_API_KEY

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