import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

system_prompt = """
ESTI UN OM SERIOS SI DIRECT, CARE NU ARE TIMP DE PIERDUT. vei raspunde concis si pe scurt.
"""

def get_response(question):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0.2
    )
    content = response.choices[0].message.content
    usage = response.usage
    return content, usage

def print_token_costs(usage):
    # Prețuri oficiale gpt-4o-mini (aug 2025):
    # input: $0.15 / 1M tokens, output: $0.60 / 1M tokens
    input_tokens = usage.prompt_tokens
    output_tokens = usage.completion_tokens
    input_cost = input_tokens * 0.00000015
    output_cost = output_tokens * 0.00000060
    total_cost = input_cost + output_cost
    print(f"Input tokens: {input_tokens}, Output tokens: {output_tokens}")
    print(f"Input cost: ${input_cost:.8f}, Output cost: ${output_cost:.8f}, Total cost: ${total_cost:.8f}")



# Example usage
question = "Show me how to write a Python function that adds two numbers."
markdown_response, usage = get_response(question)
print(markdown_response)
print_token_costs(usage)