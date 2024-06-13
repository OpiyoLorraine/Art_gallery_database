# Art Gallery Database By Opiyo Lorraine

## Project Description
Art Gallery Database is a CLI application designed to manage an art gallery's inventory, including artists, artworks, and exhibitions. The system allows for managing artist profiles, artwork details, and exhibition schedules. The application interacts with an SQLite database using Object-Oriented Programming (OOP) and ORM principles. It features three primary tables with one-to-many relationships and a composite key for exhibition schedules.


## Installation Instructions
1. Clone the repository:
   ```sh
   git clone https://github.com/OpiyoLorraine/Art_gallery_database

2. Navigate to the project repository:
   cd Art_gallery_database

3. Install the dependencies using Pipenv:
    pipenv install

4. Enter the virtual environment:
pipenv shell


## Usage Instructions
1. Ensure the database is set up:
python database/setup.py

2. Run the application:
    python cli/app.py

3. Follow the on-screen prompts to perform actions such as adding, displaying, updating, or deleting data.

## Database Structure
The application uses SQLite as the default database. Below is the structure of the database tables used:

1. Artists: Stores information about artists including their name and biography.

2. Artworks: Contains details about artworks such as title, type, and the artist associated with each artwork.

3. Exhibitions: Stores exhibition details including name, start date, and end date.

4. Exhibition_artworks: Represents the many-to-many relationship between exhibitions and artworks, linking which artworks are displayed in which exhibitions.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request on GitHub.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any inquiries or feedback, please contact OpiyoLorraine.