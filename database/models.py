# database/models.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    biography = Column(String)

    artworks = relationship("Artwork", back_populates="artist", cascade="all, delete-orphan")

class Artwork(Base):
    __tablename__ = 'artworks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    type = Column(String)
    artist_id = Column(Integer, ForeignKey('artists.id'))

    artist = relationship("Artist", back_populates="artworks")
    exhibitions = relationship("ExhibitionArtwork", back_populates="artwork", cascade="all, delete-orphan")

class Exhibition(Base):
    __tablename__ = 'exhibitions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    start_date = Column(Date)
    end_date = Column(Date)

    artworks = relationship("ExhibitionArtwork", back_populates="exhibition", cascade="all, delete-orphan")

class ExhibitionArtwork(Base):
    __tablename__ = 'exhibition_artworks'

    exhibition_id = Column(Integer, ForeignKey('exhibitions.id'), primary_key=True)
    artwork_id = Column(Integer, ForeignKey('artworks.id'), primary_key=True)

    exhibition = relationship("Exhibition", back_populates="artworks")
    artwork = relationship("Artwork", back_populates="exhibitions")
