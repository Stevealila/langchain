from datetime import datetime
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

def get_time(format: str = "%H:%M:%S") -> str:
    """Get current time in the given format"""
    return datetime.now().strftime(format)


model = init_chat_model("google_genai:gemini-2.5-flash-lite")
tooled_model = model.bind_tools([get_time])

res = tooled_model.invoke("What is the time now and 1 hour ago?")
print(res.tool_calls)
'''
[
    # for question "What is the time?"
  {
    "name": "get_time",
    "args": {
      "format": "%Y-%m-%d %H:%M:%S"
    },
    "id": "12d48591-8348-4b18-9657-9efcd7d4b51b",
    "type": "tool_call"
  },
    # for question "What was the time 1 hour ago?"
  {
    "name": "get_time",
    "args": {
      "time_shift": -3600,
      "format": "%Y-%m-%d %H:%M:%S"
    },
    "id": "f66f6689-01a3-4931-ad76-4e9871910e47",
    "type": "tool_call"
  }
]
'''