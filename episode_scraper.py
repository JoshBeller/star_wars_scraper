from bs4 import BeautifulSoup
from utils import fetch_page

class StarWarsEpisodeScraper:
    def scrape_episode_details(self, episode_urls):
        """Scrapes details from each episode's page."""
        episode_details = []

        for episode_url in episode_urls:
            print(f"Scraping details for {episode_url}...")
            page_content = fetch_page(episode_url)
            if not page_content:
                continue

            soup = BeautifulSoup(page_content, 'html.parser')
            title = soup.find('h1', class_="page-header__title").text.strip() if soup.find('h1', class_="page-header__title") else "Unknown Title"
            description = soup.find('div', class_="mw-parser-output").find('p').text.strip() if soup.find('div', class_="mw-parser-output") else "No description available."

            episode_data = {
                "title": title,
                "url": episode_url,
                "description": description
            }
            episode_details.append(episode_data)
            print(f"Scraped: {title}")

        return episode_details

    def save_episode_details(self, episode_details, filename):
        """Saves episode details to a file."""
        with open(filename, 'w') as file:
            for episode in episode_details:
                file.write(f"Title: {episode['title']}\nURL: {episode['url']}\nDescription: {episode['description']}\n\n")
