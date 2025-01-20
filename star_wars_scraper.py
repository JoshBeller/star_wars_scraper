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
        # Locate the 'Characters' section
        characters_section = soup.find('p', id="app_characters")
        if not characters_section:
            print(f"No 'Characters' section found on {media_url}.")
            return

        # Locate the 'appearances' table
        appearances_table = characters_section.find_next('table', class_="appearances")
        if not appearances_table:
            print(f"No 'appearances' table found in the 'Characters' section on {media_url}.")
            return

        # Extract character links
        character_links = appearances_table.select("ul li a")
        for link in character_links:
            character_name = link.text.strip()
            character_url = self.base_url + link['href']
            classification = self.get_character_classification(character_url)
            self.add_character(character_name, classification)

    def get_character_classification(self, character_url):
        """Fetches the classification of a character."""
        page_content = fetch_page(character_url)
        if not page_content:
            return "Unknown"

        soup = BeautifulSoup(page_content, 'html.parser')
        classification = "Unknown"

        # Locate the species information
        species_label = soup.find('h3', string="Species")
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
        """Adds a character to the appropriate list."""
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

    def save_to_files(self, known_filename, unknown_filename, unidentified_filename):
        """Saves the scraped data to files."""
        with open(known_filename, 'w') as known_file:
            for character in self.known_characters:
                known_file.write(f"{character['name']}, Classification: {character['classification']}\n")

        with open(unknown_filename, 'w') as unknown_file:
            for character in self.unknown_characters:
                unknown_file.write(f"{character['name']}, Classification: {character['classification']}\n")

        with open(unidentified_filename, 'w') as unidentified_file:
            for character in self.unidentified_characters:
                unidentified_file.write(f"{character['name']}, Classification: {character['classification']}\n")
