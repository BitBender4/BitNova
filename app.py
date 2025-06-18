from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace with your actual API keys
OPENROUTER_API_KEY = "Your api key"
DEEPAI_API_KEY = "Your api key"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    try:
        data = request.get_json()
        user_input = data.get("msg", "").strip()


        # 🖼️ Image generation trigger
        if user_input.lower().startswith("image:"):
            prompt = user_input[len("image:"):].strip()

            response = requests.post(
                "https://api.deepai.org/api/text2img",
                data={'text': prompt},
                headers={'api-key': DEEPAI_API_KEY}
            )
            response.raise_for_status()
            image_url = response.json()["output_url"]

            return jsonify({
                "response": f"<img src='{image_url}' alt='Generated image' style='max-width: 100%; border-radius: 10px;' />"
            })

        # 🧠 Text response from OpenRouter
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://127.0.0.1:5000",  # Replace with your domain if deployed
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [{"role": "user", "content": user_input}]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]

        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
