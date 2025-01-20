from bs4 import BeautifulSoup
from utils import fetch_page

def scrape_episode_urls(season_url, episodes_file):
    """Scrapes episode URLs from a season page and writes them to a file."""
    page_content = fetch_page(season_url)
    if not page_content:
        return []

    soup = BeautifulSoup(page_content, 'html.parser')
    episodes = []

    # Find the table containing episodes
    season_table = soup.find('table', class_="hidable-content nb2-inner")
    if not season_table:
        print(f"No season table found on {season_url}.")
        return episodes

    # Extract episode links
    episode_links = season_table.select("td a")
    with open(episodes_file, 'w') as file:
        for link in episode_links:
            episode_name = link.text.strip()
            episode_url = link['href']
            if not episode_url.startswith("http"):
                episode_url = f"https://starwars.fandom.com{episode_url}"
            episodes.append({"name": episode_name, "url": episode_url})
            file.write(f"{episode_name}, URL: {episode_url}\n")

    print(f"Scraped {len(episodes)} episodes from {season_url}.")
    return episodes
