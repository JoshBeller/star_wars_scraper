import os
from star_wars_scraper import StarWarsCharacterScraper

# Define new paths for test directory
TEST_DIR = os.path.join("data", "test", "characters")  # Save test results here
EPISODES_FILE = os.path.join("data", "episodes", "testFile.txt")

# Ensure the test directory exists
os.makedirs(TEST_DIR, exist_ok=True)

# Define test JSON file paths
KNOWN_FILE = os.path.join(TEST_DIR, "known_characters.json")
UNKNOWN_FILE = os.path.join(TEST_DIR, "unknown_characters.json")
UNIDENTIFIED_FILE = os.path.join(TEST_DIR, "unidentified_characters.json")

def read_test_urls(filename):
    """Reads URLs from the test file."""
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return []
    
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

if __name__ == "__main__":
    base_url = "https://starwars.fandom.com"
    scraper = StarWarsCharacterScraper(base_url)

    # Read test URLs from testFile.txt
    test_urls = read_test_urls(EPISODES_FILE)
    
    if not test_urls:
        print("No URLs found in testFile.txt. Add some episode links to test.")
    else:
        print(f"Running test on {len(test_urls)} episodes...")
        
        for episode_url in test_urls:
            print(f"Scraping characters from {episode_url}...")
            scraper.parse_characters(episode_url)

        # Save test character data to `data/test/characters/`
        scraper.save_to_files(TEST_DIR)
        print(f"Test complete. Data saved in '{TEST_DIR}'.")
