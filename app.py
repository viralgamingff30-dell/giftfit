import os
from flask import Flask, render_template

app = Flask(__name__)

# ── Put your Anthropic API key here ──
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "YOUR_API_KEY_HERE")

@app.route("/")
def index():
    return render_template("index.html", api_key=ANTHROPIC_API_KEY)

if __name__ == "__main__":
    app.run(debug=True)
