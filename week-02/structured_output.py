import json
import sys
sys.path.append('week-01')
from enum import Enum
from pydantic import BaseModel, ValidationError
from api_wrapper import APIWrapper

class Priority(str,Enum):
    LOW='low'
    MEDIUM='medium'
    HIGH='high'

class Category(str,Enum):
    BILLING='billing'
    TECHNICAL='technical'
    GENERAL='general'
    ACCOUNT='account'
    COMPLAINT='complaint'

class Sentiment(str,Enum):
    POSITIVE='positive'
    NEUTRAL='neutral'
    NEGATIVE='negative'

class SupportTicket(BaseModel):
    category: Category
    priority: Priority
    sentiment: Sentiment
    needs_human: bool



def get_structured_ticket(user_message,max_retries=3):
    prompt = f"""You are a support ticket classifier.

    Classify the following customer message and return ONLY valid JSON — no explanation, no extra text before or after.

    Customer message: "{user_message}"

    Return JSON in exactly this shape:
    {{
      "category": one of ["billing", "technical", "general", "account", "complaint"],
      "priority": one of ["low", "medium", "high"],
     "sentiment": one of ["positive", "neutral", "negative"],
     "needs_human": true or false
    }}
    """

    wrapper = APIWrapper()

    for attempt in range(max_retries):
        response = wrapper.send_message(prompt)

        if response is None:
            print(f"Attempt {attempt + 1}: No response from API")
            continue

        response_text = response.choices[0].message.content

        try:
            data = json.loads(response_text)
            ticket = SupportTicket(**data)
            return ticket

        except (json.JSONDecodeError, ValidationError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")

    print("All attempts failed")
    return None

if __name__=='__main__':
    valid_data={
        'category':'billing',
        'priority':'medium',
        'sentiment':'negative',
        'needs_human':False
    }
    ticket=SupportTicket(**valid_data)
    print(ticket)

    message="My payment failed twice and I'm really frustrated, please help urgently!"
    result=get_structured_ticket(message)

    if result is not None:
        print('\nSuccess! Structured Ticket:')
        print(result)
    else:
        print('\nFailed to get structured ticket after all retries')