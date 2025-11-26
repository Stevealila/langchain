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
response = agent.invoke({"messages":[
    {"role": "user", "content": "List all the users"},
]}, 
config
)

for message in response["messages"]:
    message.pretty_print()

print()
print("*"*100)
print()



# ======================================================CREATE (interrupted)

response = agent.invoke({"messages":[
    {"role": "user", "content": "Save Mario, email marioneto@yahoo.com, in the database."},
]}, 
config
)

for message in response["messages"]:
    message.pretty_print()

if "__interrupt__" in response:
    print(response["__interrupt__"][0].value)



print()
print("*"*100)
print()



# ======================================================DELETE

response = agent.invoke({"messages":[
    {"role": "user", "content": "Delete Ramos (ramosahmed@gmai.com)."},
]}, 
config
)

for message in response["messages"]:
    message.pretty_print()

print()
print("*"*100)
print()


# ======================================================READ

response = agent.invoke({"messages":[
    {"role": "user", "content": "List all the users"},
]}, 
config
)

for message in response["messages"]:
    message.pretty_print()

if "__interrupt__" in response:
    print(response["__interrupt__"][0].value)


'''
Using rav.yaml

Running python3 very_useful_examples/db_agent/main.py 
================================ Human Message =================================

List all the users
================================== Ai Message ==================================
Tool Calls:
  db_read_users (870d4faf-c226-4428-9242-3fc95b4dbf03)
 Call ID: 870d4faf-c226-4428-9242-3fc95b4dbf03
  Args:
================================= Tool Message =================================
Name: db_read_users

[RealDictRow({'id': 14, 'name': 'Jane', 'email': 'janedoe@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 15, 31, 33, 764797)}), RealDictRow({'id': 19, 'name': 'Ramos', 'email': 'ramosahmed@gmai.com', 'created_at': datetime.datetime(2025, 11, 25, 17, 5, 8, 733666)}), RealDictRow({'id': 31, 'name': 'Steve Alila', 'email': 'stevealila25@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 17, 23, 58, 929199)})]
================================== Ai Message ==================================

I found the following users: 
- Jane (janedoe@gmail.com)
- Ramos (ramosahmed@gmai.com)
- Steve Alila (stevealila25@gmail.com)

****************************************************************************************************

================================ Human Message =================================

List all the users
================================== Ai Message ==================================
Tool Calls:
  db_read_users (870d4faf-c226-4428-9242-3fc95b4dbf03)
 Call ID: 870d4faf-c226-4428-9242-3fc95b4dbf03
  Args:
================================= Tool Message =================================
Name: db_read_users

[RealDictRow({'id': 14, 'name': 'Jane', 'email': 'janedoe@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 15, 31, 33, 764797)}), RealDictRow({'id': 19, 'name': 'Ramos', 'email': 'ramosahmed@gmai.com', 'created_at': datetime.datetime(2025, 11, 25, 17, 5, 8, 733666)}), RealDictRow({'id': 31, 'name': 'Steve Alila', 'email': 'stevealila25@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 17, 23, 58, 929199)})]
================================== Ai Message ==================================

I found the following users: 
- Jane (janedoe@gmail.com)
- Ramos (ramosahmed@gmai.com)
- Steve Alila (stevealila25@gmail.com)
================================ Human Message =================================

Save Mario, email marioneto@yahoo.com, in the database.
================================== Ai Message ==================================
Tool Calls:
  db_insert_user (6e129e95-2151-45dd-80d6-cd5e2c1e7254)
 Call ID: 6e129e95-2151-45dd-80d6-cd5e2c1e7254
  Args:
    name: Mario
    email: marioneto@yahoo.com
{'action_requests': [{'name': 'db_insert_user', 'args': {'name': 'Mario', 'email': 'marioneto@yahoo.com'}, 'description': 'Saving user requires your approval'}], 'review_configs': [{'action_name': 'db_insert_user', 'allowed_decisions': ['approve', 'reject']}]}

****************************************************************************************************

================================ Human Message =================================

List all the users
================================== Ai Message ==================================
Tool Calls:
  db_read_users (870d4faf-c226-4428-9242-3fc95b4dbf03)
 Call ID: 870d4faf-c226-4428-9242-3fc95b4dbf03
  Args:
================================= Tool Message =================================
Name: db_read_users

[RealDictRow({'id': 14, 'name': 'Jane', 'email': 'janedoe@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 15, 31, 33, 764797)}), RealDictRow({'id': 19, 'name': 'Ramos', 'email': 'ramosahmed@gmai.com', 'created_at': datetime.datetime(2025, 11, 25, 17, 5, 8, 733666)}), RealDictRow({'id': 31, 'name': 'Steve Alila', 'email': 'stevealila25@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 17, 23, 58, 929199)})]
================================== Ai Message ==================================

I found the following users: 
- Jane (janedoe@gmail.com)
- Ramos (ramosahmed@gmai.com)
- Steve Alila (stevealila25@gmail.com)
================================ Human Message =================================

Save Mario, email marioneto@yahoo.com, in the database.
================================== Ai Message ==================================
Tool Calls:
  db_insert_user (6e129e95-2151-45dd-80d6-cd5e2c1e7254)
 Call ID: 6e129e95-2151-45dd-80d6-cd5e2c1e7254
  Args:
    name: Mario
    email: marioneto@yahoo.com
================================ Human Message =================================

Delete Ramos (ramosahmed@gmai.com).
================================== Ai Message ==================================
Tool Calls:
  db_delete_user (93669205-fdbe-4f0b-863d-1ec754dd5de7)
 Call ID: 93669205-fdbe-4f0b-863d-1ec754dd5de7
  Args:
    user_email: ramosahmed@gmai.com
================================= Tool Message =================================
Name: db_delete_user

Successfully deleted 1 record(s) with email 'ramosahmed@gmai.com'
================================== Ai Message ==================================

I have deleted Ramos from the database.

****************************************************************************************************

================================ Human Message =================================

List all the users
================================== Ai Message ==================================
Tool Calls:
  db_read_users (870d4faf-c226-4428-9242-3fc95b4dbf03)
 Call ID: 870d4faf-c226-4428-9242-3fc95b4dbf03
  Args:
================================= Tool Message =================================
Name: db_read_users

[RealDictRow({'id': 14, 'name': 'Jane', 'email': 'janedoe@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 15, 31, 33, 764797)}), RealDictRow({'id': 19, 'name': 'Ramos', 'email': 'ramosahmed@gmai.com', 'created_at': datetime.datetime(2025, 11, 25, 17, 5, 8, 733666)}), RealDictRow({'id': 31, 'name': 'Steve Alila', 'email': 'stevealila25@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 17, 23, 58, 929199)})]
================================== Ai Message ==================================

I found the following users: 
- Jane (janedoe@gmail.com)
- Ramos (ramosahmed@gmai.com)
- Steve Alila (stevealila25@gmail.com)
================================ Human Message =================================

Save Mario, email marioneto@yahoo.com, in the database.
================================== Ai Message ==================================
Tool Calls:
  db_insert_user (6e129e95-2151-45dd-80d6-cd5e2c1e7254)
 Call ID: 6e129e95-2151-45dd-80d6-cd5e2c1e7254
  Args:
    name: Mario
    email: marioneto@yahoo.com
================================ Human Message =================================

Delete Ramos (ramosahmed@gmai.com).
================================== Ai Message ==================================
Tool Calls:
  db_delete_user (93669205-fdbe-4f0b-863d-1ec754dd5de7)
 Call ID: 93669205-fdbe-4f0b-863d-1ec754dd5de7
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
  db_read_users (d1cf7749-7c19-4d25-b71f-5f2e88aa1c1d)
 Call ID: d1cf7749-7c19-4d25-b71f-5f2e88aa1c1d
  Args:
================================= Tool Message =================================
Name: db_read_users

[RealDictRow({'id': 14, 'name': 'Jane', 'email': 'janedoe@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 15, 31, 33, 764797)}), RealDictRow({'id': 31, 'name': 'Steve Alila', 'email': 'stevealila25@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 17, 23, 58, 929199)})]
================================== Ai Message ==================================

I found the following users: 
- Jane (janedoe@gmail.com)
- Steve Alila (stevealila25@gmail.com)
---------------------------------------
Status: Success!
---------------------------------------
'''