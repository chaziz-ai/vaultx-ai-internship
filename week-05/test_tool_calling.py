from openai import OpenAI
from dotenv import load_dotenv
import json
from rag_query import generate_answer
from tavily import TavilyClient
import os

load_dotenv()
client = OpenAI()
tavily_client=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

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

message = [{"role": "user", "content": "Who won the Men's T20 World Cup 2024?"}]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=message,
    tools=tools
)

reply = response.choices[0].message
print("Model's response:", reply)

if reply.tool_calls:
    tool_call = reply.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    func_name = tool_call.function.name
    print("\nModel requested tool:", func_name)
    print("Arguments given:", args)

    func_to_call = available_functions[func_name]
    result = func_to_call(**args)
    print("Tool's actual result:", result)

    message.append(reply)
    message.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result
    })

    final = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message
    )
    print("\nFinal answer:", final.choices[0].message.content)
else:
    print("Model answered directly without using a tool:", reply.content)