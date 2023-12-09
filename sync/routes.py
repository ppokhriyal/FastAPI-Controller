from config.database import collection_agents, collection_sync_device
from fastapi import APIRouter, Request, Depends, HTTPException
from jose import jwt


async def get_current_token(request: Request):
    token = request.headers.get("Authorization", None)
    if not token:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    return token.split(" ")[1]

async def decode_token(token: str = Depends(get_current_token)):
    SECRET_KEY = "d91752bec15b072f54e71d942534102c6c089d8c438917decd70a12f7b481b48"
    ALGORITHM = "HS256"
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        sub = payload.get("sub")
        return sub
    except jwt.exceptions.JWTClaimsError:
        raise HTTPException(status_code=400, detail="Invalid token")
    except jwt.exceptions.JWTError:
        raise HTTPException(status_code=401, detail="Unauthorized")


# Endpoint
sync_device_info_router = APIRouter()
@sync_device_info_router.post("/sync-device-info")
async def sync_device_info(request: Request, sub: str = Depends(decode_token)):
    data = await request.json()

    query = {"macid": sub}
    
    result = collection_agents.find(query)
    if len(list(result)) > 0:
        data_payload = {
            "macid": sub,
            "hostname": data["hostname"]
        }
        collection_sync_device.insert_one(data_payload)
        return {"authorization": "PASS" }
    else:
        return {"authorization": "FAILED"}

    