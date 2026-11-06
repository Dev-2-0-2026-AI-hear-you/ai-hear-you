Windows instructions:
#Open terminal in your downloaded folder and type the following commands one-by-one:
py -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
pip install Flask
pip install flask_sqlalchemy
pip install SQLAlchemy
py app.py

This last command runs the app on your localhost on port 5000

Web address (type in your browser)
http://localhost:5000

two pages: home and hackathon
