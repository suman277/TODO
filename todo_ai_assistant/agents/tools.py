import datetime
from zoneinfo import ZoneInfo
from google.adk.tools import ToolContext
import httpx


async def login(tool_context: ToolContext, username: str, password: str) -> dict:
    """
    Authenticate a user using username and password.
    """

    payload = {
        "username": username,
        "password": password
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/user/login",
            json=payload
        )

    response.raise_for_status()

    data = response.json()
    print("JSON RESPONSE:", data)

    if "access_token" not in data:
        raise ValueError("Login succeeded but token not found in response")

    tool_context.state["access_token"] = data["access_token"]

    return data

def validate_login(tool_context: ToolContext):
    access_token = tool_context.state.get("access_token")
    if not access_token:
        return {
            "status": "error",
            "response": "Login is expired or missing. Please login again.",
        }

async def get_user_info(tool_context: ToolContext):
    validate_login(tool_context)
    token = tool_context.state.get("access_token")
    headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://127.0.0.1:8000/user/info",
            headers = headers
        )
        data = response.json()

        tool_context.state["user_id"] = data["user_id"]



async def create_todo(tool_context : ToolContext,
                      todo : str,
                      description: str,
                      is_completed: bool):
    validate_login(tool_context)
    user_id = tool_context.state.get("user_id")
    token = tool_context.state.get("access_token")
    payload = {
        "todo" : todo,
        "description" : description,
        "is_completed" : is_completed,
    }
    headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

    async with httpx.AsyncClient() as client:
        response = await client.put(
            "http://127.0.0.1:8000/todo/todos",
            json=payload,
            headers = headers
        )
    response.raise_for_status()

    data = response.json()
    if data :
        return {
            "status": "sucesss",
            "data"  : data
        }
    return {
        "status":  "error",
        "data" : response.data
    }

async def get_todos_list(tool_context: ToolContext):
    validate_login(tool_context)
    token = tool_context.state.get("access_token")
    headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://127.0.0.1:8000/todo/todos",
            headers = headers
        )
        data = response.json()
        return {
            "status" : "Success",
            "data" : data
        }
    return {"status": "Error", "data": "An internal error occured"}

async def get_activity_logs(tool_context : ToolContext):
    validate_login(tool_context)
    token = tool_context.state.get("access_token")
    user_id = tool_context.state.get("user_id")
    headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
    url = f"http://127.0.0.1:8000/user/log/{user_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers = headers
        )
    response.raise_for_status()

    data = response.json()
    if data :
        return {
            "status": "sucesss",
            "data"  : data
        }
    return {
        "status":  "error",
        "data" : response.data
    }