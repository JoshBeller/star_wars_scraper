import os
from flask import Flask, render_template
import generate_graphs  # Import from the new location
import multiprocessing

app = Flask(__name__)

@app.route("/")
def index():
    generate_graphs.generate_species_distribution()
    generate_graphs.generate_top_characters()
    return render_template("index.html")

if __name__ == "__main__":
    multiprocessing.set_start_method("fork")  # Prevent macOS multiprocessing crash
    app.run(debug=True)

