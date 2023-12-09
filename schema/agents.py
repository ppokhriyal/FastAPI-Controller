def individual_serial(agent) -> dict:
    return {
        "id": str(agent["_id"]),
        "macid": agent["macid"],
        "token": agent["token"],
        "is_active": agent["is_active"]
    }

def list_serial(agents) -> list:
    return [individual_serial(agent) for agent in agents]