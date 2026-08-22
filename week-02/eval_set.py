eval_set = [
    {
        "input": "My payment failed twice and I'm really frustrated, please help urgently!",
        "expected": {
            "category": "billing",
            "priority": "high",
            "sentiment": "negative",
            "needs_human": True
        }
    },
    {
        "input": "Hi, just wondering what your business hours are on weekends.",
        "expected": {
            "category": "general",
            "priority": "low",
            "sentiment": "neutral",
            "needs_human": False
        }
    },
    {
        "input": "The app keeps crashing every time I try to upload a file. This is really annoying.",
        "expected": {
            "category": "technical",
            "priority": "medium",
            "sentiment": "negative",
            "needs_human": True
        }
    },
    {
        "input": "I can't log into my account, it says my password is wrong even though I just reset it.",
        "expected": {
            "category": "account",
            "priority": "high",
            "sentiment": "negative",
            "needs_human": True
        }
    },
    {
        "input": "Thank you so much for fixing my issue so quickly, really appreciate the support team!",
        "expected": {
            "category": "general",
            "priority": "low",
            "sentiment": "positive",
            "needs_human": False
        }
    },
    {
        "input": "You charged me twice for the same subscription this month, please refund immediately.",
        "expected": {
            "category": "billing",
            "priority": "high",
            "sentiment": "negative",
            "needs_human": True
        }
    },
    {
        "input": "Is there a dark mode option in the settings? Couldn't find it.",
        "expected": {
            "category": "general",
            "priority": "low",
            "sentiment": "neutral",
            "needs_human": False
        }
    },
    {
        "input": "This is the third time I'm contacting support about the same billing error and nobody has fixed it. Absolutely unacceptable service.",
        "expected": {
            "category": "complaint",
            "priority": "high",
            "sentiment": "negative",
            "needs_human": True
        }
    },
    {
        "input": "Can you please update the email address linked to my account?",
        "expected": {
            "category": "account",
            "priority": "low",
            "sentiment": "neutral",
            "needs_human": True
        }
    },
    {
        "input": "The export button doesn't do anything when I click it on Chrome.",
        "expected": {
            "category": "technical",
            "priority": "medium",
            "sentiment": "negative",
            "needs_human": True
        }
    },
    {
        "input": "Just wanted to say I love the new update, everything feels so much faster!",
        "expected": {
            "category": "general",
            "priority": "low",
            "sentiment": "positive",
            "needs_human": False
        }
    },
    {
        "input": "I was charged for a plan I never subscribed to, this feels like fraud honestly.",
        "expected": {
            "category": "billing",
            "priority": "high",
            "sentiment": "negative",
            "needs_human": True
        }
    },
    {
        "input": "How do I cancel my subscription? I don't need it anymore.",
        "expected": {
            "category": "billing",
            "priority": "medium",
            "sentiment": "neutral",
            "needs_human": True
        }
    },
    {
        "input": "Your service has been down for 2 hours now and it's costing my business money. Fix this now.",
        "expected": {
            "category": "technical",
            "priority": "high",
            "sentiment": "negative",
            "needs_human": True
        }
    },
    {
        "input": "Quick question — does the mobile app support offline mode?",
        "expected": {
            "category": "general",
            "priority": "low",
            "sentiment": "neutral",
            "needs_human": False
        }
    },
]