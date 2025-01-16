from character_scraper import StarWarsCharacterScraper
from episode_parser import StarWarsEpisodeParser
from episode_scraper import StarWarsEpisodeScraper

if __name__ == "__main__":
    base_url = "https://starwars.fandom.com"
    
    # Character Scraper Example
    character_scraper = StarWarsCharacterScraper(base_url)
    media_urls = ["https://starwars.fandom.com/wiki/Chapter_1:_The_Mandalorian#app_characters"]
    character_scraper.scrape(media_urls)
    character_scraper.save_to_files("known_characters.txt", "unknown_characters.txt", "unidentified_characters.txt")

    # Episode Parser Example
    episode_parser = StarWarsEpisodeParser(base_url)
    season_url = "https://starwars.fandom.com/wiki/The_Clone_Wars:_Season_One"
    episodes_file = "episodes.txt"
    episode_parser.parse_episodes(season_url, episodes_file)

    # Episode Scraper Example
    episode_scraper = StarWarsEpisodeScraper()
    with open(episodes_file, 'r') as file:
        episode_urls = [line.split('URL: ')[1].strip() for line in file.readlines() if 'URL:' in line]
    episode_details = episode_scraper.scrape_episode_details(episode_urls)
    episode_scraper.save_episode_details(episode_details, "episode_details.txt")
 