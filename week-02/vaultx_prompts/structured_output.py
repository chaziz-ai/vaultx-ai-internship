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
logger = get_logger("structured_output")

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
    logger.info(f"Received request to classify message: {user_message[:50]}...")
    prompt = f"""You are a support ticket classifier.

    Classify the following customer message and return ONLY valid JSON — no explanation, no extra text before or after.

    Customer message: "{user_message}"

    Classification rules:
    - category: Use "general" for simple questions or information requests with no problem being reported (e.g. "does the app support X?"). Use "billing" for payment, subscription, or charge-related actions (e.g. cancel, refund, charge dispute). Use "complaint" only when the customer expresses repeated or escalated frustration (e.g. mentions contacting support multiple times, or calls the service unacceptable). Use "technical" only when an actual bug or malfunction is being reported. Use "account" for login/credential/profile-detail issues.
    - priority: Default to "low" for routine requests and general questions with no urgency. Use "medium" when something is inconvenient but not blocking. Use "high" only when the customer explicitly signals urgency, money/access is blocked, or a service outage is affecting them.
    - needs_human: Set to false if the message is a simple informational question that can be answered from existing knowledge (like an FAQ). Set to true only if it requires an account action, a refund, or solving a non-trivial problem.
    - priority: Default to "low" for routine requests and general questions with no urgency. Use "medium" when something is inconvenient, not blocking, OR has a financial/billing consequence if delayed (e.g. unwanted subscription charges). Use "high" only when the customer explicitly signals urgency, money/access is already blocked, or a service outage is affecting them.
    
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
            logger.warning(f"Attempt {attempt + 1}: No response from API")
            continue

        response_text = response.choices[0].message.content

        try:
            data = json.loads(response_text)
            ticket = SupportTicket(**data)
            return ticket

        except (json.JSONDecodeError, ValidationError) as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")

    logger.error(f"All {max_retries} attempts failed for message: {user_message[:50]}")
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