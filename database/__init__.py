# database/__init__.py

from .connection import get_db_connection
from .setup import create_tables
from .models import Artist, Artwork, Exhibition, ExhibitionArtwork
