from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# Initialize OpenAI client with API key
client = openai.OpenAI(api_key="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")

@app.route("/generate", methods=["POST"])
def generate_post():
    data = request.json
    topic = data.get("topic", "")
    audience = data.get("audience", "")
    word_count = data.get("word_count", 100)
    tone = data.get("tone", "Professional")

    if not topic or not audience or not word_count or not tone:
        return jsonify({"error": "Please provide all fields"}), 400

    prompt = f"Write a LinkedIn post about '{topic}' targeting '{audience}'. Keep it {word_count} words long and in a {tone} tone."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in writing high-engagement LinkedIn posts."},
                {"role": "user", "content": prompt}
            ]
        )
        generated_text = response.choices[0].message.content
        return jsonify({"post": generated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
