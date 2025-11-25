from datetime import datetime
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.config import get_stream_writer

from dotenv import load_dotenv

load_dotenv()

print("Yooooooooooooooooooooooooooooooooooooooooooooooooooo")
@tool("get_time", description="Get time using the given format")
def get_time(format="%H:%M:%S") -> str:
    writer = get_stream_writer()
    writer(f"Given format is {format}")
    writer(f"Now getting in the format {format}")
    return f"The time is {datetime.now().strftime(format)}"


agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    tools=[get_time],
    system_prompt="You are a helpful assistant"
)

for chunk in agent.stream(
    {"messages":[{"role":"user", "content":"Get me time in the style date followed by full time e.g 20111219-18:00:00"}]},
    stream_mode=["custom", "updates"]
):
    print(chunk)
    print("="*80)

    '''
    Yooooooooooooooooooooooooooooooooooooooooooooooooooo
    ('updates', {'model': {'messages': [AIMessage(content='', additional_kwargs={'function_call': {'name': 'get_time', 'arguments': '{"format": "%Y%m%d-%H:%M:%S"}'}}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'model_name': 'gemini-2.5-flash-lite', 'safety_ratings': [], 'model_provider': 'google_genai'}, id='lc_run--f09c545b-b734-40cd-8fb1-151ccd45b78d-0', tool_calls=[{'name': 'get_time', 'args': {'format': '%Y%m%d-%H:%M:%S'}, 'id': '322ff2bc-0643-4729-bbc7-15becc8e0480', 'type': 'tool_call'}], usage_metadata={'input_tokens': 80, 'output_tokens': 25, 'total_tokens': 105, 'input_token_details': {'cache_read': 0}})]}})
    ================================================================================
    ('custom', 'Given format is %Y%m%d-%H:%M:%S')
    ================================================================================
    ('custom', 'Now getting in the format %Y%m%d-%H:%M:%S')
    ================================================================================
    ('updates', {'tools': {'messages': [ToolMessage(content='The time is 20251125-08:42:57', name='get_time', id='c94155c4-2f0f-42d7-b0f5-546f6098c1c4', tool_call_id='322ff2bc-0643-4729-bbc7-15becc8e0480')]}})
    ================================================================================
    ('updates', {'model': {'messages': [AIMessage(content='The time is 20251125-08:42:57', additional_kwargs={}, response_metadata={'prompt_feedback': {'block_reason': 0, 'safety_ratings': []}, 'finish_reason': 'STOP', 'model_name': 'gemini-2.5-flash-lite', 'safety_ratings': [], 'model_provider': 'google_genai'}, id='lc_run--11f2cbae-cc94-48a8-8dac-9306df5f9b71-0', usage_metadata={'input_tokens': 140, 'output_tokens': 21, 'total_tokens': 161, 'input_token_details': {'cache_read': 0}})]}})
    ================================================================================
    '''