from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from application import questions_db
from application.auth import login_required

bp = Blueprint('lecture', __name__)

@bp.route('/')
def index():
    q_db = questions_db.get_db()
    questions = q_db.execute(
        'SELECT q.id, author_id, body, created, username'
        ' FROM question q JOIN user u ON q.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    
    return render_template('lecture/index.html', questions=questions)