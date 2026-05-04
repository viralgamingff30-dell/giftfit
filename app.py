import os
from flask import Flask, render_template, request, jsonify
import anthropic
 
app = Flask(__name__)
 
# Reads from Render environment variable ANTHROPIC_API_KEY
client = anthropic.Anthropic(
    api_key=os.environ.get("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")
)
 
@app.route("/")
def index():
    return render_template("index.html")
 
@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        body = request.get_json()
        if not body:
            return jsonify({"error": "No JSON body"}), 400
 
        # Use official SDK — clean and reliable
        message = client.messages.create(
            model=body.get("model", "claude-haiku-4-5-20251001"),
            max_tokens=body.get("max_tokens", 1000),
            system=body.get("system", ""),
            messages=body.get("messages", [])
        )
 
        # Return in same format frontend expects
        return jsonify({
            "content": [{"type": "text", "text": message.content[0].text}]
        })
 
    except anthropic.AuthenticationError:
        return jsonify({"error": "Invalid API key. Check your ANTHROPIC_API_KEY in Render environment variables."}), 401
    except anthropic.RateLimitError:
        return jsonify({"error": "Rate limit hit. Please wait a moment and try again."}), 429
    except anthropic.APIConnectionError as e:
        return jsonify({"error": f"Connection error: {str(e)}"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
if __name__ == "__main__":
    app.run(debug=True)
