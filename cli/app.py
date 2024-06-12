# cli/app.py

import os
import sys
from datetime import datetime

# Ensure the script can find the database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from database.setup import create_tables
from database.models import Artist, Artwork, Exhibition, ExhibitionArtwork
from sqlalchemy.orm import joinedload

def main():
    # Initialize the database and create tables if they don't exist
    create_tables()

    # Collect user input
    artist_name = input("Enter artist's name: ")
    artist_biography = input("Enter artist's biography: ")

    artwork_title = input("Enter artwork title: ")
    artwork_type = input("Enter artwork type: ")

    exhibition_name = input("Enter exhibition name: ")
    exhibition_start_date = input("Enter exhibition start date (YYYY-MM-DD): ")
    exhibition_end_date = input("Enter exhibition end date (YYYY-MM-DD): ")

    # Convert date strings to date objects
    start_date = datetime.strptime(exhibition_start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(exhibition_end_date, '%Y-%m-%d').date()

    # Connect to the database
    db = SessionLocal()

    try:
        # Create an artist
        artist = Artist(name=artist_name, biography=artist_biography)
        db.add(artist)
        db.commit()
        db.refresh(artist)

        # Create an artwork
        artwork = Artwork(title=artwork_title, type=artwork_type, artist_id=artist.id)
        db.add(artwork)
        db.commit()
        db.refresh(artwork)

        # Create an exhibition
        exhibition = Exhibition(name=exhibition_name, start_date=start_date, end_date=end_date)
        db.add(exhibition)
        db.commit()
        db.refresh(exhibition)

        # Link artwork to exhibition
        exhibition_artwork = ExhibitionArtwork(exhibition_id=exhibition.id, artwork_id=artwork.id)
        db.add(exhibition_artwork)
        db.commit()

        # Query the database for inserted records with eager loading
        artists = db.query(Artist).all()
        artworks = db.query(Artwork).options(joinedload(Artwork.artist)).all()
        exhibitions = db.query(Exhibition).all()

        # Display results
        print("\nArtists:")
        for artist in artists:
            print(artist)

        print("\nArtworks:")
        for artwork in artworks:
            print(f"{artwork}, Artist: {artwork.artist.name}")

        print("\nExhibitions:")
        for exhibition in exhibitions:
            print(exhibition)

    finally:
        # Close the database session
        db.close()

if __name__ == "__main__":
    main()
