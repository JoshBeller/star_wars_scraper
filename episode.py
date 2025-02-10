class Episode:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def to_dict(self):
        """Converts episode object to a dictionary (for JSON storage)."""
        return {"name": self.name, "url": self.url}

    def __repr__(self):
        return f"Episode(name='{self.name}', url='{self.url}')"
