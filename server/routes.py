from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.ClientOut)
def register_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    existing = crud.get_client_by_mac(db, client.mac)
    if existing:
        raise HTTPException(status_code=400, detail="Client already registered")
    return crud.create_client(db, client)

@router.post("/status")
def post_status(status: schemas.ClientStatusCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_client_status(db, status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/clients", response_model=list[schemas.ClientResponse])
def list_clients(db: Session = Depends(get_db)):
    return crud.get_clients(db)

@router.post("/command", response_model=schemas.CommandResponse)
def send_command(cmd: schemas.CommandCreate, db: Session = Depends(get_db)):
    return crud.create_command(db, cmd.client_id, cmd.command)

@router.get("/commands/{client_id}", response_model=list[schemas.CommandResponse])
def get_commands(client_id: int, db: Session = Depends(get_db)):
    return crud.get_pending_commands(db, client_id)
