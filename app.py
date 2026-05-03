import os
import requests
from flask import Flask, render_template, request, jsonify
 
app = Flask(__name__)
 
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "YOUR_API_KEY_HERE")
 
@app.route("/")
def index():
    return render_template("index.html")
 
@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        body = request.get_json()
        if not body:
            return jsonify({"error": "No JSON body"}), 400
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json=body,
            timeout=30,
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
if __name__ == "__main__":
    app.run(debug=True)
 
