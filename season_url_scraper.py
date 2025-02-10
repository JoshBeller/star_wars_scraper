from bs4 import BeautifulSoup
from utils import fetch_page
import os

def scrape_episode_urls(series_url, episodes_file):
    """Scrapes episode URLs from a series page and writes them to a file."""
    page_content = fetch_page(series_url)
    if not page_content:
        return []

    soup = BeautifulSoup(page_content, 'html.parser')
    episodes = []

    # Find all episode tables inside "hidable-content nb2-inner"
    episode_tables = soup.find_all('table', class_="hidable-content nb2-inner")

    if not episode_tables:
        print(f"No episode tables found on {series_url}.")
        return episodes

    with open(episodes_file, 'w', encoding="utf-8") as file:
        for table in episode_tables:
            # Find episode links inside <td> elements
            episode_links = table.select("td a")

            for link in episode_links:
                episode_name = link.get("title", "").strip()  # Use title attribute for correct name
                episode_url = link["href"]

                # Fix relative URLs
                if not episode_url.startswith("http"):
                    episode_url = f"https://starwars.fandom.com{episode_url}"

                episodes.append({"name": episode_name, "url": episode_url})
                file.write(f"{episode_url}\n")

    print(f"Scraped {len(episodes)} episodes from {series_url}.")
    return episodes

if __name__ == "__main__":
    # Define output file location
    EPISODES_FILE = os.path.join("data", "episodes", "YoungJediAdventures.txt")

    # Ensure directory exists
    os.makedirs(os.path.dirname(EPISODES_FILE), exist_ok=True)

    # URL for Star Wars Rebels episodes
    URL_TO_SCRAPE = "https://starwars.fandom.com/wiki/Young_Jedi_Adventures_Season_One"

    # Run the scraper
    scrape_episode_urls(URL_TO_SCRAPE, EPISODES_FILE)
