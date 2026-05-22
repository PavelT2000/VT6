from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from config import TEMPLATES_DIR
from services import user_db, user_file

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/login")
async def login_page(request: Request, error: str | None = None):
    if request.session.get("username"):
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(
        request,
        "login.html",
        {"error": error},
    )


@router.post("/login")
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    source: str = Form(...),
):
    ok = False
    if source == "file":
        ok = user_file.verify(username, password)
    elif source == "mysql":
        ok = user_db.verify(username, password)
    else:
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": "Неверный источник аутентификации"},
            status_code=400,
        )

    if not ok:
        return templates.TemplateResponse(
            request,
            "login.html",
            {"error": "Неверный логин или пароль"},
            status_code=401,
        )

    request.session["username"] = username
    request.session["auth_source"] = source
    return RedirectResponse(url="/", status_code=302)


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)
