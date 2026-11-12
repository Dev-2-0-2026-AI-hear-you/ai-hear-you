from flask import Flask, jsonify
from questions import questions_bp

app = Flask(__name__)

app.register_blueprint(questions_bp)

@app.get("/")
def home():
    return jsonify({
        "message": "Welcome to AI Hear You!",
        "status": "running"
    })

@app.get("/health")
def health():
    return jsonify({
        "status": "healthy"

    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
