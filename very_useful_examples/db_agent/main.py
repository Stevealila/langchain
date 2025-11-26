from dotenv import load_dotenv
from tools import db_insert_user_tool, db_read_users_tool, db_delete_user_tool
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

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


# ...........................................Conversation...............................

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        break

    for update in agent.stream({"messages":[HumanMessage(content=user_input),]}, config, stream_mode="updates"):

        if "__interrupt__" in update:
 
            interrupt = update["__interrupt__"][0]
            action_requests = interrupt.value["action_requests"]
            review_configs = interrupt.value["review_configs"]
            
            for action_req, review_config in zip(action_requests, review_configs):
                
                print(f"INTERRUPT: {action_req.get('description', 'Action requires approval')}")

                new_user_name = action_req['args'].get('name', '')
                new_user_email = action_req['args'].get('email', '')
                
                allowed = review_config.get("allowed_decisions", ["approve", "reject"])
                print(f"Are sure you want to add {new_user_name}, {new_user_email}? Allowed decisions: {', '.join(allowed)}")
                
                decision_type = input("\nYour decision (approve/reject): ").strip().lower()
                
                if decision_type not in allowed:
                    print(f"Invalid decision. Must be one of: {', '.join(allowed)}")
                    decision_type = "reject"
                
                my_interrupt_decision = decision_type

            print(my_interrupt_decision)

            resume_response = agent.invoke(
                Command(
                    resume={"decisions": [{"type": my_interrupt_decision}]}
                ),
                config=config
            )
            print("================================== Ai Message ==================================\n")
            print(resume_response["messages"][-1].content)

        else:
            for node_name, node_update in update.items():
                if node_update and "messages" in node_update:
                    for message in node_update["messages"]:
                        message.pretty_print()

'''
------------------rav------------------
Using rav.yaml

Running python3 very_useful_examples/db_agent/main.py 
You: Hello
================================== Ai Message ==================================

Hello! How can I help you today?
You: How many users are there?
================================== Ai Message ==================================
Tool Calls:
  db_read_users (9f71da8e-2100-4b85-a82c-b04b34981634)
 Call ID: 9f71da8e-2100-4b85-a82c-b04b34981634
  Args:
================================= Tool Message =================================
Name: db_read_users

[RealDictRow({'id': 31, 'name': 'Steve Alila', 'email': 'stevealila25@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 17, 23, 58, 929199)}), RealDictRow({'id': 41, 'name': 'Sam Smith', 'email': 'samsmith@node.org', 'created_at': datetime.datetime(2025, 11, 26, 18, 24, 49, 141633)}), RealDictRow({'id': 45, 'name': 'Jane Doe', 'email': 'janedoe@cplusplus.org', 'created_at': datetime.datetime(2025, 11, 26, 18, 40, 31, 954774)})]
================================== Ai Message ==================================

There are 3 users in the database.
You: Who are they?
================================== Ai Message ==================================

The users are:
- Steve Alila (stevealila25@gmail.com)
- Sam Smith (samsmith@node.org)
- Jane Doe (janedoe@cplusplus.org)
You: Can you add John Doe, john.doe@company.net?
================================== Ai Message ==================================
Tool Calls:
  db_insert_user (d1f2c603-8dad-4331-9183-6009062f7963)
 Call ID: d1f2c603-8dad-4331-9183-6009062f7963
  Args:
    name: John Doe
    email: john.doe@company.net
INTERRUPT: Saving user requires your approval
Are sure you want to add John Doe, john.doe@company.net? Allowed decisions: approve, reject

Your decision (approve/reject): approve
approve
================================== Ai Message ==================================

Record inserted with ID: 46
You: Now list users in the format user-email
================================== Ai Message ==================================
Tool Calls:
  db_read_users (c6c22b4c-d233-4e5a-a7ba-8805818bbe53)
 Call ID: c6c22b4c-d233-4e5a-a7ba-8805818bbe53
  Args:
================================= Tool Message =================================
Name: db_read_users

[RealDictRow({'id': 31, 'name': 'Steve Alila', 'email': 'stevealila25@gmail.com', 'created_at': datetime.datetime(2025, 11, 25, 17, 23, 58, 929199)}), RealDictRow({'id': 41, 'name': 'Sam Smith', 'email': 'samsmith@node.org', 'created_at': datetime.datetime(2025, 11, 26, 18, 24, 49, 141633)}), RealDictRow({'id': 45, 'name': 'Jane Doe', 'email': 'janedoe@cplusplus.org', 'created_at': datetime.datetime(2025, 11, 26, 18, 40, 31, 954774)}), RealDictRow({'id': 46, 'name': 'John Doe', 'email': 'john.doe@company.net', 'created_at': datetime.datetime(2025, 11, 26, 18, 58, 41, 44647)})]
================================== Ai Message ==================================

Here are the users in the requested format:
- stevealila25@gmail.com
- samsmith@node.org
- janedoe@cplusplus.org
- john.doe@company.net
You: Great!
================================== Ai Message ==================================

Is there anything else I can help you with?
You: Remove Steve Alila, stevealila25@gmail.com                                                     
================================== Ai Message ==================================
Tool Calls:
  db_delete_user (c47b128a-b724-4080-a888-77804d109da0)
 Call ID: c47b128a-b724-4080-a888-77804d109da0
  Args:
    user_email: stevealila25@gmail.com
================================= Tool Message =================================
Name: db_delete_user

Successfully deleted 1 record(s) with email 'stevealila25@gmail.com'
================================== Ai Message ==================================

Steve Alila has been removed.
You: Now list the remaining users
================================== Ai Message ==================================
Tool Calls:
  db_read_users (c36426aa-3451-4ca1-83be-7d4763915b02)
 Call ID: c36426aa-3451-4ca1-83be-7d4763915b02
  Args:
================================= Tool Message =================================
Name: db_read_users

[RealDictRow({'id': 41, 'name': 'Sam Smith', 'email': 'samsmith@node.org', 'created_at': datetime.datetime(2025, 11, 26, 18, 24, 49, 141633)}), RealDictRow({'id': 45, 'name': 'Jane Doe', 'email': 'janedoe@cplusplus.org', 'created_at': datetime.datetime(2025, 11, 26, 18, 40, 31, 954774)}), RealDictRow({'id': 46, 'name': 'John Doe', 'email': 'john.doe@company.net', 'created_at': datetime.datetime(2025, 11, 26, 18, 58, 41, 44647)})]
================================== Ai Message ==================================

The remaining users are:
- Sam Smith (samsmith@node.org)
- Jane Doe (janedoe@cplusplus.org)
- John Doe (john.doe@company.net)
You: Cheers!
================================== Ai Message ==================================

You're welcome! Let me know if you need anything else.
You: q
---------------------------------------
Status: Success!
---------------------------------------
'''