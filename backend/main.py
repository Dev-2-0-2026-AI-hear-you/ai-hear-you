from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify({
        "message": "Welcome to AI Hear You!",
        "status": "running successfully"
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
