import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.agents import CEOAgent, LibrarianAgent, ScoutAgent, OperatorAgent

app = FastAPI(title="Nexus: The Autonomous Venture OS")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agents
ceo = CEOAgent()
librarian = LibrarianAgent()
scout = ScoutAgent()
operator = OperatorAgent()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    steps: list

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Step 1: Librarian Context
        notes = librarian.retrieve(request.message)
        
        # Step 2: Scout Research (optional)
        research = scout.research(f"Research current trends related to: {request.message}")
        
        # Step 3: CEO Synthesizes and Plans
        # We pass notes and research context to the CEO
        prompt = f"""
        User Message: {request.message}
        Past Notes: {notes}
        Current Research: {research}
        Synthesize the mission brief and determine action items (e.g., calendar prep, task creation).
        """
        response = ceo.orchestrate(prompt)
        
        # We manually suggest steps for the UI demo
        steps = [
            {"agent": "Librarian", "action": "Querying historical meeting notes..."},
            {"agent": "Scout", "action": "Searching web for recent venture news..."},
            {"agent": "CEO", "action": "Synthesizing strategy..."},
            {"agent": "Operator", "action": "Syncing with your Calendar & Tasks..."}
        ]
        
        return ChatResponse(response=response, steps=steps)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "alive"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
