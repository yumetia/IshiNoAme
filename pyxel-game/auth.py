import json


async def do_auth(api_url, mode, username, password, fetch_fn):
    """
    Performs login or register against the API.

    fetch_fn: an async callable with the same signature as pyodide's pyfetch,
    i.e. fetch_fn(url, method=..., headers=..., body=...) -> response object
    with `.status` and an async `.json()` method.

    In production (web), pass pyodide.http.pyfetch.
    In tests, pass a fake async function that returns a fake response object.

    Returns a dict:
        {"success": True, "token": "..."}
        or
        {"success": False, "error": "..."}
    """
    endpoint = "/login" if mode == "login" else "/register"
    try:
        response = await fetch_fn(
            f"{api_url}{endpoint}",
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps({
                "username": username,
                "password": password
            })
        )
        data = await response.json()

        if response.status in (200, 201) and "token" in data:
            return {"success": True, "token": data["token"]}
        else:
            return {"success": False, "error": data.get("error", "Unknown error")}

    except Exception as e:
        return {"success": False, "error": f"Error: {e}"}
