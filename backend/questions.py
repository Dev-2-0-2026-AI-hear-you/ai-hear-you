from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
import sqlite3
from pathlib import Path

questions_bp = Blueprint("questions", __name__)

# Store the database in the backend folder
DATABASE = Path(__file__).resolve().parent / "questions.db"


def get_db_connection():
    """Create and return a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create the questions table if it doesn't already exist."""
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL
        )
   """)

    connection.commit()
    connection.close()

#POST: sumbit a new question
@questions_bp.route("/questions", methods=["POST"])
def submit_question():

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

    created_at = datetime.now(timezone.utc).isoformat()

    connection = get_db_connection()

    cursor = connection.execute(
        """
        INSERT INTO questions (question, created_at)
        VALUES (?, ?)
        """,
        (question_text.strip(), created_at)
    )

    connection.commit()
    question_id = cursor.lastrowid

    question = connection.execute(
        "SELECT * FROM questions WHERE id = ?",
        (question_id,)
    ).fetchone()

    connection.close()

    return jsonify(dict(question)), 201

#GET: retrieve all questions
@questions_bp.route("/questions", methods=["GET"])
def get_questions():

    status_filter = request.args.get("status")
    connection = get_db_connection()

    if status_filter in ("pending", "answered"):
        results = connection.execute(
            "SELECT * FROM questions WHERE status = ? ORDER BY id ASC",
            (status_filter,)
        ).fetchall()
    elif status_filter is None:
        results = connection.execute(
            "SELECT * FROM questions ORDER BY id ASC"
        ).fetchall()
    else:
        connection.close()
        return jsonify({
            "error": "Invalid status filter. Use 'pending' or 'answered'."
        }), 400


    connection.close()

    return jsonify([dict(question) for question in results]), 200

#PATCH: update the status of a question
@questions_bp.route("/questions/<int:question_id>", methods=["PATCH"])
def answer_question(question_id):
    connection = get_db_connection()

    cursor = connection.execute(
        """
        UPDATE questions
        SET status = 'answered'
        WHERE id = ?
        """,
        (question_id,)
    )

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        return jsonify({"error": "Question not found"}), 404

    question = connection.execute(
        "SELECT * FROM questions WHERE id = ?",
        (question_id,)
    ).fetchone()

    connection.close()

    return jsonify(dict(question)), 200

    