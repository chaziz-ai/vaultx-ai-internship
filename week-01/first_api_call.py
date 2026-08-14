import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

Model_Name='gpt-5.6-luna'

client=OpenAI()

response=client.chat.completions.create(
    model=Model_Name,
    messages=[
        {'role':'user',
         'content':'What is an API in one sentence'}
    ]
)

print(response.choices[0].message.content)

input_tokens=response.usage.prompt_tokens
output_tokens=response.usage.completion_tokens

input_cost=(input_tokens/1_000_000)*0.20
output_cost=(output_tokens/1_000_000)*1.20
total_cost=input_cost+output_cost

print(f'Input Tokens: {input_tokens}')
print(f'Output Tokens: {output_tokens}')
print(f'Total Cost: {total_cost:.6f}')