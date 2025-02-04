from star_wars_scraper import StarWarsCharacterScraper
import os

# Directory for storing files
DATA_DIR = os.path.join("data", "Movies")
os.makedirs(DATA_DIR, exist_ok=True)

def read_episode_file(filename):
    """Reads movie URLs from a file where each line is a URL."""
    episode_urls = []
    try:
        with open(filename, 'r') as file:
            episode_urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"File {filename} not found.")
    return episode_urls


if __name__ == "__main__":
    base_url = "https://starwars.fandom.com"

    # Step 1: Read movie URLs from the existing file
    episodes_file = os.path.join(DATA_DIR, "episodes.txt")
    movie_urls = read_episode_file(episodes_file)

    # Step 2: Scrape characters for each movie
    scraper = StarWarsCharacterScraper(base_url)
    for movie_url in movie_urls:
        print(f"Scraping characters from {movie_url}...")
        scraper.parse_characters(movie_url)

    # Step 3: Save character data into the Movies directory
    scraper.save_to_files(
        os.path.join(DATA_DIR, "known_characters.txt"),
        os.path.join(DATA_DIR, "unknown_characters.txt"),
        os.path.join(DATA_DIR, "unidentified_characters.txt"),
    )
