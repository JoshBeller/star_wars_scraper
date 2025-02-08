class Character:
    def __init__(self, name, species="Unknown", character_url=""):
        self.name = name
        self.character_url = character_url  # Store character's own page URL
        self.species = species
        self.appearances = []  # List of episode/movie URLs where they appear

    def add_appearance(self, link):
        """Adds a new appearance link if it's not already in the list."""
        if link not in self.appearances:
            self.appearances.append(link)

    def update_species(self, species):
        """Updates the species if new information is found."""
        if self.species == "Unknown" or species.lower() != "unknown":
            self.species = species

    def to_dict(self):
        """Returns the character data as a dictionary (useful for saving as JSON)."""
        return {
            "name": self.name,
            "character_url": self.character_url,
            "species": self.species,
            "appearances": self.appearances
        }

    def __repr__(self):
        return f"Character(name='{self.name}', species='{self.species}', character_url='{self.character_url}', appearances={len(self.appearances)} links)"
