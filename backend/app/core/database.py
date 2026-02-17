
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create the declarative base for all models
Base = declarative_base()

# 1. Create the Engine
# pool_pre_ping=True prevents "server closed the connection unexpectedly" errors
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True
)

# 2. Create the Session Factory
# Routers will use this to create a temporary database handle for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)