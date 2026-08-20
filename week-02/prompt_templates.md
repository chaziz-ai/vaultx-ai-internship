# Prompt Template Library

This file explains the 5 prompt patterns built in `prompt_templates.py`.
Each pattern is a reusable function that returns a `messages` list, which can be sent to an LLM API.

---

## 1. Zero-Shot Prompt

**What it is:**
Give the model a task instruction with no examples. Model has to figure out the task directly.

**When to use:**
When the task is simple and the model can understand it without extra help.

**Function:**
```python
zero_shot_prompt(task_instruction:str, user_input:str)
```

**Example:**
```python
zero_shot_prompt("Classify sentiment of message", "My order is broken")
```

---

## 2. Few-Shot Prompt

**What it is:**
Give the model a few example input/output pairs before the actual question. This helps the model understand the pattern of the answer.

**When to use:**
When the task format is not obvious, or when we want the model to copy a specific style/format.

**Function:**
```python
few_shot_prompt(task_instruction:str, examples, user_input:str)
```

**Example:**
```python
examples = [
    ("Product broke on day 1", "Negative"),
    ("Amazing quality!", "Positive")
]
few_shot_prompt("Classify sentiment of message", examples, "My order is broken")
```

---

## 3. Role/System Prompt

**What it is:**
Give the model a role or identity before the task, instead of just an instruction. This controls the tone, behavior, and expertise level of the response.

**When to use:**
When the task needs judgment, tone-awareness, or specific expertise (e.g. customer support tone, legal tone, technical tone).

**Function:**
```python
role_based_prompt(role_description:str, user_input:str)
```

**Example:**
```python
role = "You are a senior customer support agent at a large tech company. You are calm, professional, and empathetic."
role_based_prompt(role, "My order is broken")
```

---

## 4. Chain-of-Thought (CoT) Prompt

**What it is:**
Instead of asking the model to answer directly, we ask it to think step by step before giving the final answer.

**When to use:**
When the task needs reasoning across multiple factors (e.g. deciding priority based on several details in a message).

**Function:**
```python
cot_based_prompt(task_instruction:str, user_input:str)
```

**Example:**
```python
cot_based_prompt(
    "Classify the priority of this support ticket as High, Medium, or Low",
    "I ordered 2 days ago, paid extra for express shipping, still not arrived. Third time this happened"
)
```

---

## 5. Constrained Output Prompt

**What it is:**
Force the model to respond only in a specific format (e.g. one word, or a strict JSON shape), with no extra text.

**When to use:**
When the output will be used by code (parsed, validated, stored). This is important because extra text (like "Sure! Here's the answer:") breaks parsing.

**Function:**
```python
constrained_based_prompt(task_instruction, output_format, user_input)
```

**Example:**
```python
constrained_based_prompt(
    "Classify this support message",
    'Respond ONLY with valid JSON in this format: {"category": "string", "priority": "high|medium|low", "sentiment": "positive|negative|neutral", "needs_human": true/false}',
    "My order is broken"
)
```

---

## Why this matters

These 5 patterns are the foundation for Week 2 Task 2, where we will force the model to return strict JSON that matches a Pydantic schema. Constrained Output pattern especially is directly connected to that — it teaches the model to give clean output that our code can safely parse.