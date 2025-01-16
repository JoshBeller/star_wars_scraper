from bs4 import BeautifulSoup
from utils import fetch_page

class StarWarsCharacterScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.known_characters = []
        self.unknown_characters = []
        self.unidentified_characters = []

    def parse_characters(self, media_url):
        """Parses the character list from the specific 'app_characters' section."""
        page_content = fetch_page(media_url)
        if not page_content:
            return

        soup = BeautifulSoup(page_content, 'html.parser')
        characters_section = soup.find('p', id="app_characters")
        if not characters_section:
            print(f"No 'Characters' section found on {media_url}.")
            return

        appearances_table = characters_section.find_next('table', class_="appearances")
        if not appearances_table:
            print(f"No 'appearances' table found in the 'Characters' section on {media_url}.")
            return

        character_links = appearances_table.select("ul li a")
        for link in character_links:
            character_name = link.text.strip()
            character_url = self.base_url + link['href']
            classification = self.get_character_classification(character_url)
            self.add_character(character_name, classification)

    def get_character_classification(self, character_url):
        """Fetches the classification of a character from their individual page."""
        page_content = fetch_page(character_url)
        if not page_content:
            return "Unknown"

        soup = BeautifulSoup(page_content, 'html.parser')
        classification = "Unknown"

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
            'classification': classification.split('[')[0].strip()
        }
        if "Unidentified" in name:
            self.unidentified_characters.append(character_data)
        elif classification == "Unknown":
            self.unknown_characters.append(character_data)
        else:
            self.known_characters.append(character_data)
