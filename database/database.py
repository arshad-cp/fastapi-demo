from dotenv import load_dotenv
from fastapi import Header, HTTPException, Depends, Request
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import create_engine
import os

from models import Tenant

load_dotenv()

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/"

SessionLocal = sessionmaker(autocommit=False, autoflush=False)

# Create a dictionary to store engines for different tenants
engines = {}


def get_db_default():
    try:
        # Create a new engine for the specific tenant
        engine = create_engine(DATABASE_URL + os.getenv("DB_DATABASE"))

        # Bind the engine to the SessionLocal
        SessionLocalMaster = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        db = SessionLocalMaster()

    except OperationalError:
        raise HTTPException(status_code=404, detail="Database not found")

    try:
        yield db
    finally:
        db.close()

    return engine


# Dependency to get the SQLAlchemy session for the request
def get_db(x_tenant_id: str = Header(None), db: Session = Depends(get_db_default)):
    # Check if tenant_id is provided
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header is required")

    tenant = db.query(Tenant).filter(Tenant.id == x_tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    try:
        # Create a new engine for the specific tenant
        engines[x_tenant_id] = create_engine(DATABASE_URL +  tenant.data['tenancy_db_name'])

        # Bind the engine to the SessionLocal
        SessionLocal.configure(bind=engines[x_tenant_id])

        db = SessionLocal()

    except OperationalError:
        raise HTTPException(status_code=404, detail="Database not found")

    try:
        yield db
    finally:
        db.close()

    return engines[x_tenant_id]
