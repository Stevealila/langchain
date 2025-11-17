from datetime import datetime
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

def get_time(format: str = "%H:%M:%S") -> str:
    """Get current time in the given format"""
    return datetime.now().strftime(format)

agent = create_agent(
    model=model,
    tools=[get_time], 
    system_prompt='You are a helpful assistant.'
)

res = agent.invoke({"messages":[{"role": "user", "content": "What is the time?"}]})

print(res)
'''
{
    'messages': [
        HumanMessage(
            content='What is the time?', 
            additional_kwargs={}, 
            response_metadata={}, 
            id='239772d1-c70d-4355-877a-9628d7bf2c0d'
        ), 
        
        AIMessage(
            content='', 
            additional_kwargs={'function_call': {'name': 'get_time', 'arguments': '{}'}}, 
            response_metadata={
                'prompt_feedback': {
                    'block_reason': 0, 
                    'safety_ratings': []
                }, 
                'finish_reason': 'STOP', 
                'model_name': 'gemini-2.5-flash', 
                'safety_ratings': [], 
                'model_provider': 'google_genai'}, 
            id='lc_run--b91f04ca-f3fd-4392-9372-9c322a5599a4-0', 
            tool_calls=[{
                'name': 'get_time', 
                'args': {}, 
                'id': 'eb082b1f-7695-4d2c-a47a-f126737f71b0', 
                'type': 'tool_call'
            }], 
            usage_metadata={
                'input_tokens': 55, 
                'output_tokens': 70, 
                'total_tokens': 125, 
                'input_token_details': {
                    'cache_read': 0}, 
                    'output_token_details': {
                        'reasoning': 60
                    }
            }
        ), 
        ToolMessage(
            content='08:23:59', 
            name='get_time', 
            id='bc459169-40a0-4076-832a-f6090bc64027', 
            tool_call_id='eb082b1f-7695-4d2c-a47a-f126737f71b0'
        ), 
        AIMessage(
            content='The time is 08:23:59.', 
            additional_kwargs={}, 
            response_metadata={
                'prompt_feedback': {'block_reason': 0, 'safety_ratings': [] }, 
                'finish_reason': 'STOP', 
                'model_name': 'gemini-2.5-flash', 
                'safety_ratings': [], 
                'model_provider': 'google_genai'
            }, 
            id='lc_run--0dd88893-b841-4072-a9fc-5916a84c2d23-0', 
            usage_metadata={
                'input_tokens': 87, 
                'output_tokens': 13, 
                'total_tokens': 100, 
                'input_token_details': {
                    'cache_read': 0
                }
        })
    ]
}'''