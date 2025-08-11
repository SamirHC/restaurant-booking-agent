from collections import defaultdict

from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from uuid import uuid4

from client.booking_client import BookingClient
from services.booking_service import BookingService
from agents.booking_agent import BookingAgent
from agents.utils.state import BookingState
from ai.openai_llm import OpenAILanguageModel
from dotenv import load_dotenv
import os

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


def create_agent():
    load_dotenv()
    client = BookingClient(
        os.environ.get("BOOKING_API_BASE_URL"),
        os.environ.get("BEARER_TOKEN"),
        "TheHungryUnicorn"
    )
    service = BookingService(client)
    llm = OpenAILanguageModel()
    agent = BookingAgent(service, llm)
    return agent

agent = create_agent()
chat_logs = defaultdict(list)
booking_states = defaultdict(BookingState)

@router.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):
    session_id = request.cookies.get("session_id")
    response = Response()

    if not session_id:
        session_id = str(uuid4())
        response.set_cookie("session_id", session_id)

    chat_log = chat_logs[session_id]
    state = booking_states[session_id]

    chat_log.append(("User", message))
    state.message = message
    state = BookingState(**agent.graph.invoke(state))
    print(f"State: {state}")
    print(f"Agent: {state.response}")
    chat_log.append(("Agent", state.response))
    state.message = None
    booking_states[session_id] = state

    template_response = templates.TemplateResponse("index.html", {
        "request": request, 
        "chat_log": chat_log,
    })

    response.body = template_response.body
    response.status_code = template_response.status_code
    response.headers.update(template_response.headers)
    
    return response
