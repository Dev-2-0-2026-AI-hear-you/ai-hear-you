from flask import Flask, jsonify, render_template, request

from questions import questions_bp
import transcription
import threading

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


# Transcription Stuff
transcript_lines = []
transcript_lock = threading.Lock()

def save_transcription(text):
    with transcript_lock:
        transcript_lines.append(text)

@app.route("/start-captions", methods=["POST"])
def start_captions():
    try:
        with transcript_lock:
            transcript_lines.clear()

        transcription.start(on_transcription=save_transcription)

        return jsonify({"status": "started"})

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route("/stop-captions", methods=["POST"])
def stop_captions():
    try:
        transcription.stop()
        return jsonify({"status": "stopped"})

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route("/transcript", methods=["GET"])
def get_transcript():
    with transcript_lock:
        return jsonify({"lines": transcript_lines.copy()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
