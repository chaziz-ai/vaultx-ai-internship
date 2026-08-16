import os
import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class APIWrapper:
    def __init__(self,model='gpt-4o-mini'):
        self.client=OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model=model

    def send_message(self,prompt,max_tokens=500):
        attempt=1
        max_attempts=3
        while attempt <= max_attempts:
            try:
                response=self.client.chat.completions.create(
                 model=self.model,
                    messages=[{'role':'user','content':prompt}],
                    timeout=10,
                    max_tokens=max_tokens
                )
                print(f'Tokens used \n:Input Tokens: {response.usage.prompt_tokens} ,\nOutput Tokens: {response.usage.completion_tokens} ,\nTotal tokens: {response.usage.total_tokens}')
                return response
            except openai.AuthenticationError:
                print('Invalid API key,check your API key')
                return None
            except openai.RateLimitError:
                print(f'Rate limit hit on attempt {attempt}, retrying...')
                attempt+=1
            except Exception as e:
                print(f'Attempt {attempt} failed: {e}')
                attempt+=1

        print('All attempts failed')
        return None

if __name__=='__main__':
    wrapper=APIWrapper()
    result= wrapper.send_message('Tell me about most famous food in Bahawalpur in one sentence.')
    if result is not None:  
        print(result.choices[0].message.content)
    else:
        print('No response recieved')