from flask import Flask, jsonify, request, render_template, url_for, redirect, send_from_directory
from questions import questions_bp, init_db
from pathlib import Path

# Locate the frontend folder
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "Front End v2"

app = Flask(
    __name__,
    template_folder="templates",
    static_folder=str(FRONTEND_DIR),
    static_url_path="/static"
    )

#Register the student question API blueprint
app.register_blueprint(questions_bp)

#Create the database and questions table if it doesn't exist
init_db()

#Landing page
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return redirect(url_for('hackathon'))
    return render_template('frontpage.html')

#Hackathon page
@app.route("/hackathon", methods=['POST', 'GET'])
def hackathon():
    return render_template('hackathon.html')

#Student interface page
@app.route("/student")
def student():
    return send_from_directory(FRONTEND_DIR, "student.html")


# Professor interface
@app.route("/professor")
def professor():
    return send_from_directory(FRONTEND_DIR, "professor.html")

#Health check endpoint
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

# @app.route("/page2")
# def page2():
#     return render_template('page2.html')
print(app.url_map)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)