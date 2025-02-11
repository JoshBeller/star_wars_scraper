import json
import pandas as pd
import os
import matplotlib
matplotlib.use("Agg")  # Prevent macOS GUI errors
import matplotlib.pyplot as plt
import re  # Import regex for cleaning

# Ensure static directory exists
os.makedirs("static", exist_ok=True)

def clean_species_name(species):
    """Remove citation numbers like [1], [2] from species names."""
    return re.sub(r"\[\d+\]", "", species).strip()

def generate_species_distribution():
    """Generate a properly formatted bar chart showing the most common species in Star Wars."""

    # Load data
    with open("data/characters/known_characters.json", "r", encoding="utf-8") as file:
        characters = json.load(file)

    # Extract species data and clean up
    species_list = [clean_species_name(char.get("species", "Unknown")) for char in characters.values()]
    
    # Convert to DataFrame
    df = pd.DataFrame(species_list, columns=["species"])

    # Count occurrences
    species_counts = df["species"].value_counts().head(10)  # Top 10 species

    # Set figure size
    plt.figure(figsize=(12, 6))

    # Create the bar chart
    bars = plt.bar(species_counts.index, species_counts.values, color="green")

    # Rotate labels for better readability
    plt.xticks(rotation=30, ha="right", fontsize=12)
    plt.yticks(fontsize=12)

    # Adjust layout
    plt.subplots_adjust(bottom=0.3)

    # Add count labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 5, int(yval), ha="center", fontsize=10, fontweight="bold")

    # Titles and labels
    plt.xlabel("Species", fontsize=14, fontweight="bold")
    plt.ylabel("Number of Characters", fontsize=14, fontweight="bold")
    plt.title("Top 10 Most Common Species in Star Wars", fontsize=16, fontweight="bold")

    # Save the figure
    plt.savefig("static/species_distribution.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("✅ Cleaned species data and saved graph as static/species_distribution.png")


if __name__ == "__main__":
    print("📊 Cleaning and generating graphs...")

    generate_species_distribution()

    print("✅ Graphs updated successfully!")
