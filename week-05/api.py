from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import json
from rag_query import generate_answer
from tavily import TavilyClient
import os

load_dotenv()
app = FastAPI()

client = OpenAI()
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_documents(query: str):
    result = generate_answer(query)
    return result["answer"]

def calculator(expression: str):
    return str(eval(expression))

def web_search(query: str):
    response = tavily_client.search(query=query, max_results=3)
    results = response["results"]
    summary = "\n\n".join([f"{r['title']}: {r['content']}" for r in results])
    return summary

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate basic math expressions like 25*37 or 100/4",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression to evaluate, e.g. \"25*37\""
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": "Search VaultX internal company PDF documents to answer questions about internship tasks, deadlines, policies, or any company-specific information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The question to search for in the documents"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the internet for current, real-time, or general knowledge information not related to VaultX internal documents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

available_functions = {
    "calculator": calculator,
    "search_documents": search_documents,
    "web_search": web_search
}

def run_agent(question: str):
    messages = [
    {"role": "system", "content": (
        "You do not reliably know today's date, the current time, or any other real-time information "
        "from your own memory — if the user asks about these, you must use the web_search tool "
        "instead of guessing or using an old date from training."
    )},
    {"role": "user", "content": question},
    {"role": "system", "content": (
        "IMPORTANT: The message above may contain earlier conversation history in one language, "
        "followed by a new/latest question in a different language. Find ONLY the newest question "
        "in that message and reply in THAT language — completely ignore the language of any earlier "
        "history lines when deciding your reply language."
    )}
]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )

    reply = response.choices[0].message
    tool_used = "none"

    if reply.tool_calls:
        tool_call = reply.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        func_name = tool_call.function.name
        tool_used = func_name

        func_to_call = available_functions[func_name]
        result = func_to_call(**args)

        messages.append(reply)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })

        final = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return final.choices[0].message.content, tool_used
    else:
        return reply.content, tool_used

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    answer, tool_used = run_agent(request.message)
    return {"response": answer, "tool_used": tool_used}