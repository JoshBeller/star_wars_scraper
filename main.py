import os
import json
from star_wars_scraper import StarWarsCharacterScraper

# Define base data directories
DATA_DIR = "data"
EPISODES_DIR = os.path.join(DATA_DIR, "episodes")
CHARACTERS_DIR = os.path.join(DATA_DIR, "characters")

# Define episode text file paths
MOVIES_FILE = os.path.join(EPISODES_DIR, "Movies.txt")
CLONE_WARS_FILE = os.path.join(EPISODES_DIR, "CloneWarsEpisodes.txt")

# Define character JSON file paths
KNOWN_FILE = os.path.join(CHARACTERS_DIR, "known_characters.json")
UNKNOWN_FILE = os.path.join(CHARACTERS_DIR, "unknown_characters.json")
UNIDENTIFIED_FILE = os.path.join(CHARACTERS_DIR, "unidentified_characters.json")

# Ensure directories exist
os.makedirs(CHARACTERS_DIR, exist_ok=True)

def read_urls(filename):
    """Reads URLs from a text file."""
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return []
    
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

if __name__ == "__main__":
    base_url = "https://starwars.fandom.com"
    scraper = StarWarsCharacterScraper(base_url)

    # Scrape Movies
    for movie_url in read_urls(MOVIES_FILE):
        print(f"Scraping characters from movie: {movie_url}")
        scraper.parse_characters(movie_url)

    # Scrape Clone Wars Episodes
    for episode_url in read_urls(CLONE_WARS_FILE):
        print(f"Scraping characters from Clone Wars episode: {episode_url}")
        scraper.parse_characters(episode_url)

    # Save all character data in the correct directory
    scraper.save_to_files(CHARACTERS_DIR)
    print(f"Scraping complete. Character data saved in '{CHARACTERS_DIR}'.")
