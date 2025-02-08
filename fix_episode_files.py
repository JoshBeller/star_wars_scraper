import os

# Define the directory containing the episode files
EPISODES_DIR = "data/episodes"

def clean_episode_file(filename):
    """Cleans episode file by removing 'URL:' and numbers, keeping only episode names."""
    file_path = os.path.join(EPISODES_DIR, filename)

    if not os.path.exists(file_path):
        print(f"File {filename} not found.")
        return
    
    cleaned_lines = []
    
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            # Remove "URL:" and numbers, keeping only the episode name
            cleaned_line = line.split("URL:")[-1].strip()
            cleaned_lines.append(cleaned_line)

    # Overwrite the file with cleaned content
    with open(file_path, "w", encoding="utf-8") as file:
        for line in cleaned_lines:
            file.write(line + "\n")

    print(f"Cleaned {filename} and saved.")

if __name__ == "__main__":
    # List of episode files to process
    episode_files = ["CloneWarsEpisodes.txt", "Movies.txt", "testFile.txt"]

    for episode_file in episode_files:
        clean_episode_file(episode_file)
