# database/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    biography = Column(String)

    artworks = relationship('Artwork', back_populates='artist')

    def __repr__(self):
        return f"<Artist(id={self.id}, name='{self.name}', biography='{self.biography}')>"

class Artwork(Base):
    __tablename__ = 'artworks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    type = Column(String)
    artist_id = Column(Integer, ForeignKey('artists.id'))

    artist = relationship('Artist', back_populates='artworks')

    def __repr__(self):
        return f"<Artwork(id={self.id}, title='{self.title}', type='{self.type}', artist_name='{self.artist.name}')>"

class Exhibition(Base):
    __tablename__ = 'exhibitions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    start_date = Column(Date)
    end_date = Column(Date)

    artworks = relationship('ExhibitionArtwork', back_populates='exhibition')

    def __repr__(self):
        return f"<Exhibition(id={self.id}, name='{self.name}', start_date='{self.start_date}', end_date='{self.end_date}')>"

class ExhibitionArtwork(Base):
    __tablename__ = 'exhibition_artworks'

    exhibition_id = Column(Integer, ForeignKey('exhibitions.id'), primary_key=True)
    artwork_id = Column(Integer, ForeignKey('artworks.id'), primary_key=True)

    exhibition = relationship('Exhibition', back_populates='artworks')
    artwork = relationship('Artwork')

    def __repr__(self):
        return f"<ExhibitionArtwork(exhibition_id={self.exhibition_id}, artwork_id={self.artwork_id})>"
