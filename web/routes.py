from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from uuid import uuid4


router = APIRouter()

templates = Jinja2Templates(directory="web/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid4())
        response = RedirectResponse(url="/chat")
        response.set_cookie("session_id", session_id)
        return response
    return templates.TemplateResponse("index.html", {"request": request})


chat_log = []

@router.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):
    chat_log.append(("User", message))
    chat_log.append(("Agent", f"Message '{message}', received!"))
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "chat_log": chat_log,
    })
