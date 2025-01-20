from star_wars_scraper import StarWarsCharacterScraper
from season_url_scraper import scrape_episode_urls
import os

# Directory for storing files
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def read_episode_file(filename):
    """Reads episode URLs from a file."""
    episode_urls = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                if "URL:" in line:
                    url = line.split("URL:")[1].strip()
                    episode_urls.append(url)
    except FileNotFoundError:
        print(f"File {filename} not found.")
    return episode_urls


if __name__ == "__main__":
    base_url = "https://starwars.fandom.com"

    # Step 1: Scrape episode URLs from a season
    season_url = "https://starwars.fandom.com/wiki/The_Clone_Wars:_Season_One"
    episodes_file = os.path.join(DATA_DIR, "episodes.txt")
    scrape_episode_urls(season_url, episodes_file)

    # Step 2: Read episode URLs
    episode_urls = read_episode_file(episodes_file)

    # Step 3: Scrape characters for each episode
    scraper = StarWarsCharacterScraper(base_url)
    for episode_url in episode_urls:
        print(f"Scraping characters from {episode_url}...")
        scraper.parse_characters(episode_url)

    # Step 4: Save character data
    scraper.save_to_files(
        os.path.join(DATA_DIR, "known_characters.txt"),
        os.path.join(DATA_DIR, "unknown_characters.txt"),
        os.path.join(DATA_DIR, "unidentified_characters.txt"),
    )
