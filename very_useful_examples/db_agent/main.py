from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
from tools import db_insert_user_tool, db_read_users_tool, db_delete_user_tool

load_dotenv()


agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    system_prompt="You are a helpful assistant",
    tools=[db_insert_user_tool, db_read_users_tool, db_delete_user_tool],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "db_insert_user": {
                    "allowed_decisions": ["approve", "reject"], 
                    "description": "Saving user requires your approval"
                },
            }
        )
    ],
    checkpointer=InMemorySaver()
)


config = {"configurable": {"thread_id":"79"}}


# ======================================================READ
agent.invoke({"messages":[{"role": "user", "content": "List all the users"},]}, config)

# ======================================================CREATE (interrupted)
save_response = agent.invoke({"messages":[{"role": "user", "content": "Save Mario, email marioneto@yahoo.com, in the database."},]},config)
if "__interrupt__" in save_response:
    print(f"INTERRUPTED: {save_response["__interrupt__"][0].value}")

# ======================================================DELETE
agent.invoke({"messages":[{"role": "user", "content": "Delete Ramos (ramosahmed@gmai.com)."},]}, config)

# ======================================================READ again
response = agent.invoke({"messages":[
    {"role": "user", "content": "List all the users"},
]}, config)

for message in response["messages"]:
    message.pretty_print()


'''
INTERRUPTED: {'action_requests': [{'name': 'db_insert_user', 'args': {'name': 'Mario', 'email': 'marioneto@yahoo.com'}, 'description': 'Saving user requires your approval'}], 'review_configs': [{'action_name': 'db_insert_user', 'allowed_decisions': ['approve', 'reject']}]}
================================ Human Message =================================

List all the users
================================== Ai Message ==================================
Tool Calls:
  db_read_users (e4919a33-8ff8-414f-a30d-0d623ab15acf)
 Call ID: e4919a33-8ff8-414f-a30d-0d623ab15acf
  Args:
================================= Tool Message =================================
Name: db_read_users

[RealDictRow({'id': 14, 'name': 'Jane', 'email': 'janedoe@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 15, 31, 33, 764797)}), RealDictRow({'id': 31, 'name': 'Steve Alila', 'email': 'stevealila25@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 17, 23, 58, 929199)}), RealDictRow({'id': 40, 'name': 'Ramos', 'email': 'ramosahmed@gmai.com', 'created_at': datetime.datetime(2025, 11, 26, 11, 9, 46, 138106)})]
================================== Ai Message ==================================

Here are the users I have:

* Jane (janedoe@gmail.com)
* Steve Alila (stevealila25@gmail.com)
* Ramos (ramosahmed@gmai.com)
================================ Human Message =================================

Save Mario, email marioneto@yahoo.com, in the database.
================================== Ai Message ==================================
Tool Calls:
  db_insert_user (19f04a90-79da-409b-8124-be85124763f2)
 Call ID: 19f04a90-79da-409b-8124-be85124763f2
  Args:
    name: Mario
    email: marioneto@yahoo.com
================================ Human Message =================================

Delete Ramos (ramosahmed@gmai.com).
================================== Ai Message ==================================
Tool Calls:
  db_delete_user (aeb98188-ef41-46df-b48c-d3fdda27e094)
 Call ID: aeb98188-ef41-46df-b48c-d3fdda27e094
  Args:
    user_email: ramosahmed@gmai.com
================================= Tool Message =================================
Name: db_delete_user

Successfully deleted 1 record(s) with email 'ramosahmed@gmai.com'
================================== Ai Message ==================================

I have deleted Ramos from the database.
================================ Human Message =================================

List all the users
================================== Ai Message ==================================
Tool Calls:
  db_read_users (03a4c274-91a4-493d-bc79-84630a6f14a1)
 Call ID: 03a4c274-91a4-493d-bc79-84630a6f14a1
  Args:
================================= Tool Message =================================
Name: db_read_users

[RealDictRow({'id': 14, 'name': 'Jane', 'email': 'janedoe@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 15, 31, 33, 764797)}), RealDictRow({'id': 31, 'name': 'Steve Alila', 'email': 'stevealila25@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 17, 23, 58, 929199)})]
================================== Ai Message ==================================

Here are the users I have:

* Jane (janedoe@gmail.com)
* Steve Alila (stevealila25@gmail.com)
'''