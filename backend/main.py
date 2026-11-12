from flask import Flask, jsonify
from questions import questions_bp, init_db

app = Flask(__name__)

app.register_blueprint(questions_bp)

#initialize database
init_db()

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
