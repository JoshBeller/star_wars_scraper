from bs4 import BeautifulSoup
from utils import fetch_page

class StarWarsEpisodeParser:
    def __init__(self, base_url):
        self.base_url = base_url

    def parse_episodes(self, season_url, episodes_file):
        """Parses episode links from a season page and writes to a file."""
        page_content = fetch_page(season_url)
        if not page_content:
            return []

        soup = BeautifulSoup(page_content, 'html.parser')
        episodes = []

        season_table = soup.find('table', class_="hidable-content nb2-inner")
        if not season_table:
            print(f"No season table found on {season_url}.")
            return episodes

        episode_links = season_table.select("td a")
        with open(episodes_file, 'w') as file:
            for link in episode_links:
                episode_name = link.text.strip()
                episode_url = self.base_url + link['href']
                episodes.append({"name": episode_name, "url": episode_url})
                file.write(f"{episode_name}, URL: {episode_url}\n")

        return episodes
