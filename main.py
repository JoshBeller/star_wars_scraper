import os
import json
from star_wars_scraper import StarWarsCharacterScraper

# Define data paths
DATA_DIR = "data"
MOVIES_FILE = os.path.join(DATA_DIR, "Movies.txt")
CLONE_WARS_FILE = os.path.join(DATA_DIR, "CloneWarsEpisodes.txt")
CHARACTERS_JSON = os.path.join(DATA_DIR, "characters.json")

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
        scraper.parse_characters(movie_url, "Movies")

    # Scrape Clone Wars Episodes
    for episode_url in read_urls(CLONE_WARS_FILE):
        print(f"Scraping characters from Clone Wars episode: {episode_url}")
        scraper.parse_characters(episode_url, "Clone Wars")

    # Save all character data
    scraper.save_characters(CHARACTERS_JSON)
    print(f"Scraping complete. Character data saved to '{CHARACTERS_JSON}'.")
