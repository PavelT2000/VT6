from fastapi import Request
from fastapi.responses import RedirectResponse


class CurrentUser:
    def __init__(self, username: str, auth_source: str):
        self.username = username
        self.auth_source = auth_source


async def get_current_user(request: Request) -> CurrentUser | RedirectResponse:
    username = request.session.get("username")
    auth_source = request.session.get("auth_source")
    if not username or not auth_source:
        return RedirectResponse(url="/login", status_code=302)
    return CurrentUser(username=username, auth_source=auth_source)
