from langchain.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv
from db import User


load_dotenv()


# .............................tools

# CREATE
@tool(
    name_or_callable="db_insert_user", 
    description="Save user in postgres database", 
    return_direct=True
)
def db_insert_user_tool(name: str, email: str):
    return User().insert_record(name=name, email=email)


# READ 
@tool(
    name_or_callable="db_read_user", 
    description="Get users already saved in postgres database", 
)
def db_read_users_tool():
    return User().read_records()





# .............................agent


agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    tools=[db_insert_user_tool, db_read_users_tool],
    system_prompt="You are a helpful assistant"
)


# .............................Natural language testing


# ..........First create-read

# CREATE
res = agent.invoke({"messages":[
    {"role":"user", "content":"Save user Ramos of email ramosahmed@gmai.com."}
]})

for message in res["messages"]:
    message.pretty_print()
    print()
print("-"*100)

# READ
res = agent.invoke({"messages":[
    {"role":"user", "content":"List all the users. Give me name and email only"}
]})

for message in res["messages"]:
    message.pretty_print()
    print()
print("-"*100)


# ..........Second create-read


# CREATE
res = agent.invoke({"messages":[
    {"role":"user", "content":"Save user Steve Alila of email stevealila25@gmail.com."}
]})

for message in res["messages"]:
    message.pretty_print()
    print()
print("-"*100)

# READ
res = agent.invoke({"messages":[
    {"role":"user", "content":"List all the users. Give me name and email only"}
]})

for message in res["messages"]:
    message.pretty_print()
    print()
print("-"*100)

'''
(langchn) steve@alila:~/langchn$ python3 main.py 
================================ Human Message =================================

Save user Ramos of email ramosahmed@gmai.com.

================================== Ai Message ==================================
Tool Calls:
  db_insert_user (bccb5c7f-5549-4583-b0d4-7faf723f4ee4)
 Call ID: bccb5c7f-5549-4583-b0d4-7faf723f4ee4
  Args:
    name: Ramos
    email: ramosahmed@gmai.com

================================= Tool Message =================================
Name: db_insert_user

Record with email 'ramosahmed@gmai.com' already exists, skipped insertion

----------------------------------------------------------------------------------------------------
================================ Human Message =================================

List all the users. Give me name and email only

================================== Ai Message ==================================
Tool Calls:
  db_read_user (ed7a701b-1ce1-47fb-9dac-1d1d1008f834)
 Call ID: ed7a701b-1ce1-47fb-9dac-1d1d1008f834
  Args:

================================= Tool Message =================================
Name: db_read_user

[RealDictRow({'id': 13, 'name': 'John', 'email': 'johndoe@company.net', 'created_at': datetime.datetime(2025, 11, 25, 15, 31, 33, 726549)}), RealDictRow({'id': 14, 'name': 'Jane', 'email': 'janedoe@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 15, 31, 33, 764797)}), RealDictRow({'id': 19, 'name': 'Ramos', 'email': 'ramosahmed@gmai.com', 'created_at': datetime.datetime(2025, 11, 25, 17, 5, 8, 733666)})]

================================== Ai Message ==================================

Here are the users:
* John (johndoe@company.net)
* Jane (janedoe@gmail.com)
* Ramos (ramosahmed@gmai.com)

----------------------------------------------------------------------------------------------------
================================ Human Message =================================

Save user Steve Alila of email stevealila25@gmail.com.

================================== Ai Message ==================================
Tool Calls:
  db_insert_user (4865da3c-3221-423d-a238-59043ee2f05e)
 Call ID: 4865da3c-3221-423d-a238-59043ee2f05e
  Args:
    name: Steve Alila
    email: stevealila25@gmail.com

================================= Tool Message =================================
Name: db_insert_user

Record inserted with ID: 31

----------------------------------------------------------------------------------------------------
================================ Human Message =================================

List all the users. Give me name and email only

================================== Ai Message ==================================

I can help you with that! I'll list all the users, and provide only their names and emails.
Tool Calls:
  db_read_user (5b2caf26-746c-473d-a61c-337f1b711395)
 Call ID: 5b2caf26-746c-473d-a61c-337f1b711395
  Args:

================================= Tool Message =================================
Name: db_read_user

[RealDictRow({'id': 13, 'name': 'John', 'email': 'johndoe@company.net', 'created_at': datetime.datetime(2025, 11, 25, 15, 31, 33, 726549)}), RealDictRow({'id': 14, 'name': 'Jane', 'email': 'janedoe@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 15, 31, 33, 764797)}), RealDictRow({'id': 19, 'name': 'Ramos', 'email': 'ramosahmed@gmai.com', 'created_at': datetime.datetime(2025, 11, 25, 17, 5, 8, 733666)}), RealDictRow({'id': 31, 'name': 'Steve Alila', 'email': 'stevealila25@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 17, 23, 58, 929199)})]

================================== Ai Message ==================================

Here are the users:
- Name: John, Email: johndoe@company.net
- Name: Jane, Email: janedoe@gmail.com
- Name: Ramos, Email: ramosahmed@gmai.com
- Name: Steve Alila, Email: stevealila25@gmail.com

----------------------------------------------------------------------------------------------------
'''