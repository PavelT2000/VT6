import os
from pathlib import Path

from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from config import TEMPLATES_DIR, UPLOAD_DIR
from dependencies import CurrentUser, get_current_user

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def _safe_path(filename: str) -> Path | None:
    name = Path(filename).name
    if not name:
        return None
    target = (UPLOAD_DIR / name).resolve()
    try:
        target.relative_to(UPLOAD_DIR.resolve())
    except ValueError:
        return None
    return target


@router.get("/")
async def index(
    request: Request,
    user: CurrentUser | RedirectResponse = Depends(get_current_user),
):
    if isinstance(user, RedirectResponse):
        return user
    files = sorted(
        f for f in os.listdir(UPLOAD_DIR) if (UPLOAD_DIR / f).is_file()
    )
    source_label = "файл (users.txt)" if user.auth_source == "file" else "MySQL"
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "user": user.username,
            "auth_source": source_label,
            "files": files,
        },
    )


@router.post("/upload")
async def upload(
    request: Request,
    file: UploadFile = File(...),
    user: CurrentUser | RedirectResponse = Depends(get_current_user),
):
    if isinstance(user, RedirectResponse):
        return user
    if not file.filename:
        return RedirectResponse(url="/", status_code=302)
    safe = Path(file.filename).name
    if not safe:
        return RedirectResponse(url="/", status_code=302)
    dest = UPLOAD_DIR / safe
    content = await file.read()
    dest.write_bytes(content)
    return RedirectResponse(url="/", status_code=302)


@router.get("/download/{filename}")
async def download(
    filename: str,
    user: CurrentUser | RedirectResponse = Depends(get_current_user),
):
    if isinstance(user, RedirectResponse):
        return user
    path = _safe_path(filename)
    if path is None or not path.is_file():
        return RedirectResponse(url="/", status_code=302)
    return FileResponse(path, filename=path.name)


@router.post("/delete/{filename}")
async def delete(
    filename: str,
    user: CurrentUser | RedirectResponse = Depends(get_current_user),
):
    if isinstance(user, RedirectResponse):
        return user
    path = _safe_path(filename)
    if path is not None and path.is_file():
        path.unlink()
    return RedirectResponse(url="/", status_code=302)
