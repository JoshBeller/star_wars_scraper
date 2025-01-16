import requests
from bs4 import BeautifulSoup

#Not using this file anymore split up the files to make more sense

class StarWarsCharacterScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.known_characters = []
        self.unknown_characters = []
        self.unidentified_characters = []

    def fetch_page(self, url):
        """Fetches the content of a webpage."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_characters(self, media_url):
        """Parses the character list from the specific 'app_characters' section."""
        page_content = self.fetch_page(media_url)
        if not page_content:
            return

        soup = BeautifulSoup(page_content, 'html.parser')
        # Locate the 'Characters' section by its id
        characters_section = soup.find('p', id="app_characters")
        if not characters_section:
            print(f"No 'Characters' section found on {media_url}.")
            return

        # Dynamically find the 'appearances' table following the 'Characters' section
        appearances_table = characters_section.find_next('table', class_="appearances")
        if not appearances_table:
            print(f"No 'appearances' table found in the 'Characters' section on {media_url}.")
            return

        # Extract character links
        character_links = appearances_table.select("ul li a")
        if not character_links:
            print(f"No character links found in the 'Characters' section on {media_url}.")
            return

        for link in character_links:
            character_name = link.text.strip()
            character_url = self.base_url + link['href']
            print(f"Processing character: {character_name} ({character_url})")  # Debug log
            classification = self.get_character_classification(character_url)
            self.add_character(character_name, classification)

    def get_character_classification(self, character_url):
        """Fetches the classification of a character from their individual page."""
        page_content = self.fetch_page(character_url)
        if not page_content:
            return "Unknown"

        soup = BeautifulSoup(page_content, 'html.parser')
        classification = "Unknown"

        # Locate the species information
        species_label = soup.find('h3', text="Species")
        if species_label:
            species_value = species_label.find_next('div', class_="pi-data-value pi-font")
            if species_value:
                species_text = species_value.text.strip().lower()
                if "droid" in species_text:
                    classification = "Droid"
                else:
                    classification = species_text.capitalize()

        return classification

    def add_character(self, name, classification):
        """Adds a new character to the appropriate list."""
        character_data = {
            'name': name,
            'classification': classification.split('[')[0].strip()  # Remove citation numbers
        }
        if "Unidentified" in name:
            self.unidentified_characters.append(character_data)
        elif classification == "Unknown":
            self.unknown_characters.append(character_data)
        else:
            self.known_characters.append(character_data)

    def parse_episodes(self, season_url, episodes_file):
        """Parses episode links from a season page and writes to a file."""
        page_content = self.fetch_page(season_url)
        if not page_content:
            return []

        soup = BeautifulSoup(page_content, 'html.parser')
        episodes = []

        # Locate the season's table containing episodes
        season_table = soup.find('table', class_="hidable-content nb2-inner")
        if not season_table:
            print(f"No season table found on {season_url}.")
            return episodes

        # Extract episode links
        episode_links = season_table.select("td a")
        with open(episodes_file, 'w') as file:
            for link in episode_links:
                episode_name = link.text.strip()
                episode_url = self.base_url + link['href']
                episodes.append({"name": episode_name, "url": episode_url})
                file.write(f"{episode_name}, URL: {episode_url}\n")

        return episodes

    def scrape_episode_urls(self, episodes_file):
        """Reads episode URLs from a file and prints them."""
        try:
            with open(episodes_file, 'r') as file:
                urls = [line.split('URL: ')[1].strip() for line in file.readlines() if 'URL:' in line]
                return urls
        except FileNotFoundError:
            print(f"File {episodes_file} not found.")
            return []

    def scrape(self, media_urls):
        """Main method to scrape all media URLs."""
        for url in media_urls:
            print(f"Scraping characters from {url}...")
            self.parse_characters(url)

    def save_to_files(self, known_filename, unknown_filename, unidentified_filename):
        """Saves the scraped data to three separate files."""
        with open(known_filename, 'w') as known_file:
            for character in self.known_characters:
                known_file.write(f"{character['name']}, Classification: {character['classification']}\n")

        with open(unknown_filename, 'w') as unknown_file:
            for character in self.unknown_characters:
                unknown_file.write(f"{character['name']}, Classification: {character['classification']}\n")

        with open(unidentified_filename, 'w') as unidentified_file:
            for character in self.unidentified_characters:
                unidentified_file.write(f"{character['name']}, Classification: {character['classification']}\n")
    

# Example usage
if __name__ == "__main__":
    base_url = "https://starwars.fandom.com"
    media_urls = [
        "https://starwars.fandom.com/wiki/Chapter_1:_The_Mandalorian#app_characters"
    ]

    scraper = StarWarsCharacterScraper(base_url)
    scraper.scrape(media_urls)
    scraper.save_to_files("known_characters.txt", "unknown_characters.txt", "unidentified_characters.txt")

    # Example to scrape episodes from a season URL and write to a file
    season_url = "https://starwars.fandom.com/wiki/The_Clone_Wars:_Season_One"
    episodes_file = "episodes.txt"
    scraper.parse_episodes(season_url, episodes_file)

    # Example to scrape episode URLs from the file
    episode_urls = scraper.scrape_episode_urls(episodes_file)
    print("Episode URLs to scrape:")
    print("\n".join(episode_urls))
