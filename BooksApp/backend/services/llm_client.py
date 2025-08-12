import os
from openai import OpenAI
from backend.utils.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "ESTI UN OM SERIOS SI DIRECT, CARE NU ARE TIMP DE PIERDUT. "
    "vei raspunde concis si pe scurt."
)

def get_llm_response(question, system_prompt=SYSTEM_PROMPT, model="gpt-4o-mini", temperature=0.2):
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