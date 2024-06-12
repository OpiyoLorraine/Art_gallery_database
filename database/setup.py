from .connection import engine
from .models import Base

def create_tables():
    Base.metadata.create_all(bind=engine)
