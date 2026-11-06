from flask import Flask, jsonify, request, render_template, url_for

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return app.redirect(url_for('hackathon'))
    return render_template('frontpage.html')

@app.route("/hackathon", methods=['POST', 'GET'])
def hackathon():
    if request.method == 'GET':
        render_template('hackathon.html')
    return render_template('hackathon.html')

# @app.route("/page2")
# def page2():
#     return render_template('page2.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)