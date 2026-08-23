import json
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
week01_path = os.path.join(current_dir, '..', '..', 'week-01')
sys.path.append(week01_path)
from enum import Enum
from pydantic import BaseModel, ValidationError
from api_wrapper import APIWrapper
from vaultx_prompts.logger_config import get_logger
logger = get_logger("extractor")
from typing import Optional

class EmailExtraction(BaseModel):
    sender_name: Optional[str] = None
    subject: Optional[str] = None
    request_type: Optional[str] = None
    reference_number: Optional[str] = None
    amount: Optional[float] = None

def get_email_extraction(user_email,max_retries=3):
    prompt = f"""You are an information extraction assistant.

    Extract the information from following email and return ONLY valid JSON — no explanation, no extra text before or after.

    email: "{user_email}"

    Return JSON in exactly this shape:
    {{
      "sender_name":"string or null",
      "subject":"string or null",
      "request_type":"string or null",
      "reference_number":"string or null",
      "amount": number or null
    }}
    If any field is not mentioned in the email, set its value to null instead of guessing.
    """

    wrapper=APIWrapper()

    for attempt in range(max_retries):
        response=wrapper.send_message(prompt)

        if response is None:
            logger.warning(f'Attempt {attempt+1}: No response from API')
            continue

        response_text=response.choices[0].message.content

        try:
            data=json.loads(response_text)
            email=EmailExtraction(**data)
            return email

        except(json.JSONDecodeError,ValidationError) as e:
            logger.warning(f'Attempt {attempt + 1} failed: {e}')

    logger.error('All attempts failed')
    return None

if __name__=='__main__':
    sample_email="""
    Hi Support Team,

    My name is Ahmed Raza. I recently ordered a laptop stand but it arrived damaged.
    I would like to request a replacement as soon as possible.

    Thanks,
    Ahmed
    """

    result=get_email_extraction(sample_email)
    print(result)

    if result is not None:
        print('\nSuccesss')
        print(result)
    else:
        print('\nFailed to get output after all retries')