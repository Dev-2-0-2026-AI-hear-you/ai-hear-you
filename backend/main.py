from flask import Flask, jsonify, render_template, request

from questions import questions_bp
from backend.transcription import transcribe_audio

app = Flask(__name__)
app.register_blueprint(questions_bp)

hand_raised = False

@app.get("/")
def home():
    return render_template("test_frontpage.html")

@app.get("/hackathon")
def classroom():
    return render_template("test_hackathon.html")


@app.get("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/hand-raise", methods=["GET", "POST"])
def hand_raise_status():
    global hand_raised

    if request.method == "POST":
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or not isinstance(data.get("raised"), bool):
            return jsonify({"error": "A true or false raised value is required."}), 400
        hand_raised = data["raised"]

    return jsonify({"raised": hand_raised})


@app.post("/transcribe")
def transcribe():
    if not request.data:
        return jsonify({"error": "An audio chunk is required."}), 400

    try:
        text = transcribe_audio(request.data, request.args.get("sample_rate", 16000, type=int))
    except ModuleNotFoundError:
        return jsonify({"error": "Live transcription packages are missing. Install the backend requirements and restart the server."}), 503
    except Exception:
        return jsonify({"error": "The audio chunk could not be transcribed."}), 500

    return jsonify({"text": text})


@app.post("/summarize")
def summarize():
    data = request.get_json(silent=True)
    transcript = data.get("transcript") if isinstance(data, dict) else None
    if not isinstance(transcript, str) or not transcript.strip():
        return jsonify({"error": "Transcript text is required."}), 400

    try:
        import ollama
        response = ollama.chat(
            model="gemma3:1b",
            messages=[
                {"role": "system", "content": "Summarize lecture notes clearly for a student. Use a few short bullet points. Only include information from the transcript."},
                {"role": "user", "content": transcript[-12000:]}
            ],
        )
    except ModuleNotFoundError:
        return jsonify({"error": "Install the Ollama Python package and start Ollama to use summaries."}), 503
    except Exception as error:
        if error.__class__.__name__ == "ResponseError" and getattr(error, "status_code", None) == 404:
            return jsonify({"error": "The gemma3:1b model is missing. Run ollama pull gemma3:1b."}), 503
        return jsonify({"error": "Could not connect to Ollama. Start the Ollama app, then restart this backend."}), 503

    return jsonify({"summary": response.message.content})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
