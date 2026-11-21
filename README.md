# General Information for this project

## Local Installation Instructions - Windows

You need to have a virtual environement installed.

Run the following commands in your terminal in the 'website' folder (this folder). This will create the virtual environment/ folder 'virtualenv' and activate it, allowing you to install Flask. The application is made using Flask.

```powershell
py -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
python.exe -m pip install --upgrade pip
pip install Flask
flask --app application init-db
pip install gunicorn
```

## To run the Flask application locally

```powershell
flask --app application run --debug
```

## Web Deployment Instructions - Windows

This project uses Gunicorn to deploy the Flask app to the web. Please install Gunicorn to your virtual environment with the following command:

```powershell
pip install gunicorn
```

To deploy the app, use the following command:

```powershell
gunicorn myapp:app
```

## Notes

This application should run on port 5000

If you are running this locally, web address: http://localhost:5000
