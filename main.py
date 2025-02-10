import os
import json
from star_wars_scraper import StarWarsCharacterScraper

# Define base data directories
DATA_DIR = "data"
EPISODES_DIR = os.path.join(DATA_DIR, "episodes")
CHARACTERS_DIR = os.path.join(DATA_DIR, "characters")

# Ensure directories exist
os.makedirs(CHARACTERS_DIR, exist_ok=True)

def read_urls(filename):
    """Reads URLs from a text file."""
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return []
    
    with open(filename, 'r', encoding="utf-8") as file:
        return [line.strip().split(", ")[-1] for line in file if line.strip()]

if __name__ == "__main__":
    base_url = "https://starwars.fandom.com"
    scraper = StarWarsCharacterScraper(base_url)

    # Loop through all episode text files in the directory
    for episode_file in os.listdir(EPISODES_DIR):
        if episode_file.endswith(".txt"):
            series_name = episode_file.replace("Episodes.txt", "")  # Extract series name
            episode_path = os.path.join(EPISODES_DIR, episode_file)
            episode_urls = read_urls(episode_path)

            if not episode_urls:
                print(f"No episodes found in {episode_file}, skipping...")
                continue

            print(f"Scraping characters for {series_name} ({len(episode_urls)} episodes)...")

            for episode_url in episode_urls:
                try:
                    print(f"Scraping: {episode_url}")
                    scraper.parse_characters(episode_url)
                except Exception as e:
                    print(f"Error scraping {episode_url}: {e}")

    # Save all character data by passing only the directory
    scraper.save_to_files(CHARACTERS_DIR)

    print("All character data saved.")
