import json
from bs4 import BeautifulSoup
from utils import fetch_page
from Character import Character

class StarWarsCharacterScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.known_characters = {}
        self.unknown_characters = {}
        self.unidentified_characters = {}

    def parse_characters(self, media_url):
        """Parses character list from an episode/movie page."""
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
            print(f"No 'appearances' table found on {media_url}.")
            return

        character_links = appearances_table.select("ul li a")
        for link in character_links:
            character_name = link.text.strip()
            character_url = self.base_url + link['href']  # Save character's own page URL
            species = self.get_character_species(character_url)

            # Add the character with the episode/movie URL in appearances
            self.add_character(character_name, species, media_url, character_url)

    def get_character_species(self, character_url):
        """Fetches species of a character from their page."""
        page_content = fetch_page(character_url)
        if not page_content:
            return "Unknown"

        soup = BeautifulSoup(page_content, 'html.parser')
        species_label = soup.find('h3', string="Species")
        if species_label:
            species_value = species_label.find_next('div', class_="pi-data-value pi-font")
            if species_value:
                return species_value.text.strip()

        return "Unknown"



    def __init__(self, base_url):
            self.base_url = base_url
            self.known_characters = {}
            self.unknown_characters = {}
            self.unidentified_characters = {}

    def add_character(self, name, species, media_url, character_url):
            """Adds character to the appropriate category."""
            new_character = Character(name, species, character_url)
            new_character.add_appearance(media_url)

            if "Unidentified" in name:
                if name in self.unidentified_characters:
                    self.unidentified_characters[name]["appearances"].append(media_url)
                else:
                    self.unidentified_characters[name] = new_character.to_dict()
            elif species == "Unknown":
                if name in self.unknown_characters:
                    self.unknown_characters[name]["appearances"].append(media_url)
                else:
                    self.unknown_characters[name] = new_character.to_dict()
            else:
                if name in self.known_characters:
                    self.known_characters[name]["appearances"].append(media_url)
                else:
                    self.known_characters[name] = new_character.to_dict()

    def save_to_files(self, known_file, unknown_file, unidentified_file):
        """Saves characters to separate JSON files."""
        with open(known_file, 'w', encoding='utf-8') as f:
            json.dump(self.known_characters, f, indent=4, ensure_ascii=False)

        with open(unknown_file, 'w', encoding='utf-8') as f:
            json.dump(self.unknown_characters, f, indent=4, ensure_ascii=False)

        with open(unidentified_file, 'w', encoding='utf-8') as f:
            json.dump(self.unidentified_characters, f, indent=4, ensure_ascii=False)
