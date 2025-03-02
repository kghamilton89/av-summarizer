from flask import Flask, request, jsonify
from openai import OpenAI
import os
import hashlib

app = Flask(__name__)

# Load OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Error: OPENAI_API_KEY is not set!")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Set the hashed password (use SHA-256)
STORED_PASSWORD_HASH = hashlib.sha256("Portolavalley2025!".encode()).hexdigest()

@app.route("/auth", methods=["POST"])
def authenticate():
    data = request.get_json()
    if not data or "password" not in data:
        return jsonify({"error": "No password provided"}), 400

    # Hash the input password and compare it with the stored hash
    input_password_hash = hashlib.sha256(data["password"].encode()).hexdigest()
    
    if input_password_hash == STORED_PASSWORD_HASH:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Incorrect password"}), 403

# Transcribe function using Whisper API
def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return response.text

# Summarize function using GPT-4
def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a podcast summarization assistant."},
            {"role": "user", "content": f"Summarize this podcast transcript: {text}"}
        ]
    )
    return response.choices[0].message.content

@app.route("/upload", methods=["POST"])
def upload_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = f"uploads/{file.filename}"
    file.save(file_path)

    transcript = transcribe_audio(file_path)
    summary = summarize_text(transcript)

    return jsonify({"transcript": transcript, "summary": summary})

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400
    
    text = data["text"]
    summary = summarize_text(text)
    
    return jsonify({"summary": summary})

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
