from pydantic import BaseModel

class ClientCreate(BaseModel):
    hostname: str
    ip: str
    mac: str

class ClientOut(BaseModel):
    id: int
    hostname: str
    ip: str
    mac: str
    model_config = {
        "from_attributes": True
    }

class ClientResponse(ClientCreate):
    id: int
    is_active: bool
    model_config = {
        "from_attributes": True
    }

class CommandCreate(BaseModel):
    client_id: int
    command: str

class CommandResponse(BaseModel):
    id: int
    client_id: int
    command: str
    processed: bool

class ClientStatusCreate(BaseModel):
    mac: str
    cpu_load: float
    memory_usage: int
    uptime: int

