from vaultx_prompts.structured_output import get_structured_ticket
from vaultx_prompts.logger_config import get_logger

logger = get_logger("classification_tool")

test_samples = [
        # (message, expected_category, expected_priority, expected_sentiment, expected_needs_human)
        ("My payment failed twice and I'm really frustrated, please help urgently!", "billing", "high", "negative", True),
        ("What are your business hours?", "general", "low", "neutral", False),
        ("The app keeps crashing every time I open the camera feature.", "technical", "high", "negative", True),
        ("Can I change my email address on my account?", "account", "low", "neutral", False),
        ("I was charged twice for the same subscription this month.", "billing", "high", "negative", True),
        ("How do I reset my password?", "account", "low", "neutral", False),
        ("This is the third time your service has failed me. I want a refund NOW.", "complaint", "high", "negative", True),
        ("Just wanted to say your support team was super helpful yesterday, thanks!", "general", "low", "positive", False),
        ("The dashboard is loading very slowly since the last update.", "technical", "medium", "negative", True),
        ("Do you offer a student discount?", "billing", "low", "neutral", False),
        ("I can't log in, it says my account is locked.", "account", "high", "negative", True),
        ("Your product is great, but the mobile app UI could be better.", "general", "low", "positive", False),
        ("I need to cancel my subscription immediately, this is unacceptable service.", "complaint", "high", "negative", True),
        ("Is there an API available for developers?", "technical", "low", "neutral", False),
        ("My invoice shows the wrong amount, please correct it.", "billing", "medium", "negative", True),
        ("How do I update my billing address?", "account", "low", "neutral", False),
        ("The export feature is completely broken, I lost important data!", "technical", "high", "negative", True),
        ("Thanks for fixing the bug so quickly, really appreciate it.", "general", "low", "positive", False),
        ("I've been on hold for 40 minutes and no one is responding.", "complaint", "high", "negative", True),
        ("Can you tell me the difference between the Pro and Basic plans?", "general", "low", "neutral", False),
    ]

correct_count=0

for message,exp_category,exp_priority,exp_sentiment,exp_needs_human in test_samples:
    result=get_structured_ticket(message)
    if result is None:
        logger.error(f"Failed to classify message: {message[:50]}")
        continue
    print(result)

    category_match=(result.category.value==exp_category)
    priority_match=(result.priority.value==exp_priority)
    sentiment_match=(result.sentiment.value==exp_sentiment)
    needs_human_match=(result.needs_human==exp_needs_human)

    overall_match=category_match and priority_match and sentiment_match and needs_human_match

    if overall_match:
        correct_count += 1

    print(message)
    print(f"Expected  -> category={exp_category}, priority={exp_priority}, sentiment={exp_sentiment}, needs_human={exp_needs_human}")
    print(f"Predicted -> category={result.category.value}, priority={result.priority.value}, sentiment={result.sentiment.value}, needs_human={result.needs_human}")
    print(f"Match: {overall_match}")
    print("-" * 40)

logger.info(f"Total correct: {correct_count} / {len(test_samples)}")
accuracy = (correct_count / len(test_samples)) * 100
logger.info(f"Final accuracy: {accuracy}%")
print(f"\nTotal correct: {correct_count} / {len(test_samples)}")
print(f"Accuracy: {accuracy}%")