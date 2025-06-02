from sqlalchemy.orm import Session
from .models import Client, Command
from . import models, schemas
from datetime import datetime

def get_clients(db: Session):
    return db.query(Client).all()

def get_client_by_hostname(db: Session, hostname: str):
    return db.query(Client).filter(Client.hostname == hostname).first()

def create_client(db: Session, client_data: schemas.ClientCreate) -> models.Client:
    db_client = models.Client(**client_data.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_client_by_mac(db: Session, mac: str):
    return db.query(models.Client).filter(models.Client.mac == mac).first()

def create_or_update_client(db: Session, hostname: str, ip_address: str):
    db_client = get_client_by_hostname(db, hostname)
    if db_client:
        db_client.ip_address = ip_address
        db_client.last_seen = datetime.utcnow()
    else:
        db_client = Client(hostname=hostname, ip_address=ip_address)
        db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def create_command(db: Session, client_id: int, command: str):
    cmd = Command(client_id=client_id, command=command)
    db.add(cmd)
    db.commit()
    db.refresh(cmd)
    return cmd

def get_pending_commands(db: Session, client_id: int):
    return db.query(Command).filter_by(client_id=client_id, processed=False).all()

def mark_command_processed(db: Session, cmd_id: int):
    cmd = db.query(Command).filter_by(id=cmd_id).first()
    if cmd:
        cmd.processed = True
        db.commit()
