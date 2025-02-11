import json
import pandas as pd
import os
import matplotlib
matplotlib.use("Agg")  # Prevent macOS GUI errors
import matplotlib.pyplot as plt

from flask import Flask, jsonify, render_template

# Load JSON file
CHARACTERS_FILE = os.path.join("data", "characters", "known_characters_cleaned.json")

def load_character_data():
    """Loads Star Wars character data from JSON."""
    with open(CHARACTERS_FILE, "r", encoding="utf-8") as f:
        characters = json.load(f)
    return pd.DataFrame(characters.values())

def plot_most_frequent_characters(df):
    """Plots the top 20 most appearing characters."""
    df["appearance_count"] = df["appearances"].apply(len)
    top_characters = df.nlargest(20, "appearance_count")

    plt.figure(figsize=(12, 6))
    plt.barh(top_characters["name"], top_characters["appearance_count"], color="blue")
    plt.xlabel("Number of Appearances")
    plt.ylabel("Character Name")
    plt.title("Top 20 Most Appearing Star Wars Characters")
    plt.gca().invert_yaxis()

    # Save in static/ instead of static/graphs/
    plt.savefig("static/top_characters.png", dpi=300, bbox_inches="tight")
    plt.close()

def plot_species_distribution(df):
    """Plots the distribution of character species."""
    species_counts = df["species"].value_counts().head(10)  # Top 10 species

    plt.figure(figsize=(10, 5))
    species_counts.plot(kind="bar", color="green")
    plt.xlabel("Species")
    plt.ylabel("Number of Characters")
    plt.title("Top 10 Most Common Species in Star Wars")
    plt.xticks(rotation=45, ha="right")

    # Save in static/ instead of static/graphs/
    plt.savefig("static/species_distribution.png", dpi=300, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    print("📊 Loading character data...")
    df = load_character_data()

    # Ensure `static/` directory exists
    os.makedirs("static", exist_ok=True)

    print("\n📈 Generating graphs...")
    plot_most_frequent_characters(df)
    plot_species_distribution(df)

    print("\n✅ Graphs saved in 'static/' directory!")
