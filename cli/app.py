import os
import sys
from datetime import datetime

# Ensure the script can find the database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from database.setup import create_tables
from database.models import Artist, Artwork, Exhibition, ExhibitionArtwork
from sqlalchemy.orm import joinedload

def display_data(db):
    # Query the database for inserted records with eager loading
    artists = db.query(Artist).all()
    artworks = db.query(Artwork).options(joinedload(Artwork.artist)).all()
    exhibitions = (
        db.query(Exhibition)
        .options(
            joinedload(Exhibition.artworks).joinedload(ExhibitionArtwork.artwork).joinedload(Artwork.artist)
        )
        .all()
    )

    # Display results
    print("\nArtists:")
    for artist in artists:
        print(f"ID: {artist.id}, Name: {artist.name}, Biography: {artist.biography}")

    print("\nArtworks:")
    for artwork in artworks:
        artist_name = artwork.artist.name if artwork.artist else "Unknown Artist"
        print(f"ID: {artwork.id}, Title: {artwork.title}, Type: {artwork.type}, Artist: {artist_name}")

    print("\nExhibitions:")
    for exhibition in exhibitions:
        print(f"ID: {exhibition.id}, Name: {exhibition.name}, Start Date: {exhibition.start_date}, End Date: {exhibition.end_date}")
        for ea in exhibition.artworks:
            artist_name = ea.artwork.artist.name if ea.artwork.artist else "Unknown Artist"
            print(f"    - Artwork ID: {ea.artwork.id}, Title: {ea.artwork.title}, Artist: {artist_name}")

def delete_artist(db):
    artist_id = int(input("Enter the ID of the artist to delete: "))
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if artist:
        db.delete(artist)
        db.commit()
        print(f"Artist ID {artist_id} and all related artworks and exhibitions deleted.")
    else:
        print(f"Artist ID {artist_id} not found.")

def delete_artwork(db):
    artwork_id = int(input("Enter the ID of the artwork to delete: "))
    artwork = db.query(Artwork).filter(Artwork.id == artwork_id).first()
    if artwork:
        # Remove associated ExhibitionArtwork records first
        db.query(ExhibitionArtwork).filter(ExhibitionArtwork.artwork_id == artwork_id).delete()
        db.delete(artwork)
        db.commit()
        print(f"Artwork ID {artwork_id} and all associated exhibition links deleted.")
    else:
        print(f"Artwork ID {artwork_id} not found.")

def delete_exhibition(db):
    exhibition_id = int(input("Enter the ID of the exhibition to delete: "))
    exhibition = db.query(Exhibition).filter(Exhibition.id == exhibition_id).first()
    if exhibition:
        db.delete(exhibition)
        db.commit()
        print(f"Exhibition ID {exhibition_id} deleted.")
    else:
        print(f"Exhibition ID {exhibition_id} not found.")

def update_artist(db):
    artist_id = int(input("Enter the ID of the artist to update: "))
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if artist:
        new_name = input(f"Enter new name for artist (current: {artist.name}): ")
        new_biography = input(f"Enter new biography for artist (current: {artist.biography}): ")
        if new_name:
            artist.name = new_name
        if new_biography:
            artist.biography = new_biography
        db.commit()
        print(f"Artist ID {artist_id} updated.")
    else:
        print(f"Artist ID {artist_id} not found.")

def update_artwork(db):
    artwork_id = int(input("Enter the ID of the artwork to update: "))
    artwork = db.query(Artwork).filter(Artwork.id == artwork_id).first()
    if artwork:
        new_title = input(f"Enter new title for artwork (current: {artwork.title}): ")
        new_type = input(f"Enter new type for artwork (current: {artwork.type}): ")
        if new_title:
            artwork.title = new_title
        if new_type:
            artwork.type = new_type
        db.commit()
        print(f"Artwork ID {artwork_id} updated.")
    else:
        print(f"Artwork ID {artwork_id} not found.")

def update_exhibition(db):
    exhibition_id = int(input("Enter the ID of the exhibition to update: "))
    exhibition = db.query(Exhibition).filter(Exhibition.id == exhibition_id).first()
    if exhibition:
        new_name = input(f"Enter new name for exhibition (current: {exhibition.name}): ")
        new_start_date = input(f"Enter new start date for exhibition (current: {exhibition.start_date}, YYYY-MM-DD): ")
        new_end_date = input(f"Enter new end date for exhibition (current: {exhibition.end_date}, YYYY-MM-DD): ")
        if new_name:
            exhibition.name = new_name
        if new_start_date:
            exhibition.start_date = datetime.strptime(new_start_date, '%Y-%m-%d').date()
        if new_end_date:
            exhibition.end_date = datetime.strptime(new_end_date, '%Y-%m-%d').date()
        db.commit()
        print(f"Exhibition ID {exhibition_id} updated.")
    else:
        print(f"Exhibition ID {exhibition_id} not found.")

def main():
    # Initialize the database and create tables if they don't exist
    create_tables()

    # Connect to the database
    db = SessionLocal()

    try:
        while True:
            print("\nOptions:")
            print("1. Add new data")
            print("2. Display data")
            print("3. Delete artist")
            print("4. Delete artwork")
            print("5. Delete exhibition")
            print("6. Update artist")
            print("7. Update artwork")
            print("8. Update exhibition")
            print("9. Exit")

            choice = input("Select an option: ")

            if choice == '1':
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

            elif choice == '2':
                display_data(db)

            elif choice == '3':
                delete_artist(db)

            elif choice == '4':
                delete_artwork(db)

            elif choice == '5':
                delete_exhibition(db)

            elif choice == '6':
                update_artist(db)

            elif choice == '7':
                update_artwork(db)

            elif choice == '8':
                update_exhibition(db)

            elif choice == '9':
                break

            else:
                print("Invalid option. Please try again.")

    finally:
        # Close the database session
        db.close()

if __name__ == "__main__":
    main()
