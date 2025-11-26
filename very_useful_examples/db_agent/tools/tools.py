from langchain.tools import tool
from db import User

@tool(
    name_or_callable="db_insert_user", 
    description="Save user in postgres database", 
    return_direct=True
)
def db_insert_user_tool(name: str, email: str):
    return User().insert_record(name=name, email=email)

@tool(
    name_or_callable="db_read_users", 
    description="Get users already saved in postgres database", 
)
def db_read_users_tool():
    return User().read_records()


@tool(
    name_or_callable="db_delete_user", 
    description="Delete the user of the given user_email from the postgres database", 
)
def db_delete_user_tool(user_email: str):
    return User().delete_record(user_email)