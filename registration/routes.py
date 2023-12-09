from fastapi import APIRouter, HTTPException, Request
from config.database import collection_agents
import time
from jose import jwt

class AgentRegistrationService:
    def __init__(self, data) -> None:
        self.data = data
        self.collection_agents = collection_agents

    async def register_agent(self):
        # Check if mac-id is already registered for the agent
        if self.__check_macid_exists(self.data["macid"]):
            raise HTTPException(status_code=409, detail="Agent already registered")
        # Register new agent
        token = self.__generate_token(self.data["macid"])
        data_dict = {
            "macid": self.data["macid"],
            "token": token,
            "is_active": False,
        }
        self.collection_agents.insert_one(data_dict)
        return {"access_token": token}
    
    def __check_macid_exists(self, macid) -> bool:
        query = {"macid": macid}
        result = self.collection_agents.find(query)
        if len(list(result)) > 0:
            return True
        return False
    
    def __generate_token(self, macid) -> str:
        SECRET_KEY = "d91752bec15b072f54e71d942534102c6c089d8c438917decd70a12f7b481b48"
        ALGORITHM = "HS256"
        token_payload = {
            "iss": "contoller",
            "sub": macid,
            "iat": time.time(),
            "exp": time.time() + 31536000  # 365 days in seconds
        }
        return jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)

# Endpoint
agent_registration_router = APIRouter()
@agent_registration_router.post("/agent-registration")
async def agent_registration(request: Request):
    # Collect POST data
    data = await request.json()
    agent_registration_service = AgentRegistrationService(data)
    return await agent_registration_service.register_agent()