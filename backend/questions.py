from flask import Blueprint, jsonify, request
from datetime import datetime

questions_bp = Blueprint("questions", __name__)

# Temporary in-memory storage for questions
questions = []
next_question_id = 1

@questions_bp.route("/questions", methods=["POST"])
def submit_question():
    global next_question_id

    data = request.get_json(silent=True)

    if not data or not isinstance(data,dict):
        return jsonify({
            "error": "A valid JSON body is required."
        }), 400

    question_text = data.get("question")

    if not isinstance(question_text, str) or not question_text.strip():
        return jsonify({
            "error": "Question cannot be empty"
        }), 400

    question = {
        "id": next_question_id,
        "question": question_text.strip(),
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }

    questions.append(question)
    next_question_id += 1

    return jsonify(question), 201

@questions_bp.route("/questions", methods=["GET"])

def get_questions():
    return jsonify(questions), 200

@questions_bp.route("/questions/<int:question_id>", methods=["PATCH"])

def answer_question(question_id):
    for question in questions:
        if question["id"] == question_id:
            question["status"] = "answered"
            return jsonify(question), 200

    return jsonify({"error": "Question not fouund"}), 404

    