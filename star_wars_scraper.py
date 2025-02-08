import json
from bs4 import BeautifulSoup
from utils import fetch_page

class StarWarsCharacterScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.known_characters = {}
        self.unknown_characters = {}
        self.unidentified_characters = {}
        self.character_url_map = {}  # Maps character URLs to their stored names

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
            character_url = self.base_url + link['href']
            species = self.get_character_species(character_url)

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

    def add_character(self, name, species, media_url, character_url):
        """Adds character to the appropriate category using `character_url` for duplicates, but storing by name."""
        character_data = {
            "name": name,
            "character_url": character_url,
            "species": species,
            "appearances": [media_url]
        }

        # If this URL has been seen before, update the existing entry
        if character_url in self.character_url_map:
            existing_name = self.character_url_map[character_url]

            # Find the existing entry in the correct category
            if existing_name in self.known_characters:
                existing_character = self.known_characters[existing_name]
            elif existing_name in self.unknown_characters:
                existing_character = self.unknown_characters[existing_name]
            else:
                existing_character = self.unidentified_characters[existing_name]

            # Add the new appearance
            if media_url not in existing_character["appearances"]:
                existing_character["appearances"].append(media_url)

            # Update the name if it's different (keep the most recognizable one)
            if existing_character["name"] != name:
                print(f"Updating name: {existing_character['name']} → {name}")
                existing_character["name"] = name

        else:
            # First time seeing this character, store them under their name
            self.character_url_map[character_url] = name

            if "Unidentified" in name:
                self.unidentified_characters[name] = character_data
            elif species == "Unknown":
                self.unknown_characters[name] = character_data
            else:
                self.known_characters[name] = character_data

    def save_to_files(self, base_directory="data/characters/"):
        """Saves characters to separate JSON files in `data/characters/`."""
        known_file = f"{base_directory}/known_characters.json"
        unknown_file = f"{base_directory}/unknown_characters.json"
        unidentified_file = f"{base_directory}/unidentified_characters.json"

        with open(known_file, 'w', encoding='utf-8') as f:
            json.dump(self.known_characters, f, indent=4, ensure_ascii=False)

        with open(unknown_file, 'w', encoding='utf-8') as f:
            json.dump(self.unknown_characters, f, indent=4, ensure_ascii=False)

        with open(unidentified_file, 'w', encoding='utf-8') as f:
            json.dump(self.unidentified_characters, f, indent=4, ensure_ascii=False)
