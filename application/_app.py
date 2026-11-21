from flask import Flask
from . import __init__

app = __init__.create_app()