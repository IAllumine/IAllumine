from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from orchestrator.agent import root_agent as orchestrator_agent
from google.genai import types # For creating message Content/Parts
from fastapi import FastAPI
from pydantic import BaseModel, Field
from google.adk.cli.fast_api import get_fast_api_app
import os
import uvicorn
from dotenv import load_dotenv
import uuid as guid

load_dotenv()  # Load environment variables from a .env file if present

class requestBody(BaseModel):
    question: str

## INITIALIZE FASTAPI APP AND RUNNER
app: FastAPI = get_fast_api_app(
    agents_dir=os.path.dirname(os.path.abspath(__file__)),
    web=False,
)

session_service = InMemorySessionService()

# Define constants for identifying the interaction context
APP_NAME = "weather_tutorial_app"
USER_ID = "user_1"

runner = Runner(
    agent=orchestrator_agent, # The agent we want to run
    app_name=APP_NAME,   # Associates runs with our app
    session_service=session_service # Uses our session manager
)

## DEFINE ENDPOINTS
@app.post("/chat")
async def query_agent(request: requestBody):
    # session_id = "session_001"
    session_id = guid.uuid4().hex  # Generate a unique session ID for each request
    print(f"Starting new session: {session_id}")
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id
    )
    print(f"User query: {request.question}")
    final_response = "I don't know, sorry."
    message = types.Content(role='user', parts=[types.Part(text=request.question)])
    async for event in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=message):
        if event.is_final_response():
            if event.content and event.content.parts:
                # Assuming text response in the first part
                final_response = event.content.parts[0].text
    print(f"Agent response: {final_response}")
    return {"answer": final_response}

if __name__ == "__main__":
    # Use the PORT environment variable provided by Cloud Run, defaulting to 8080
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))