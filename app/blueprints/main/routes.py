from flask import render_template, request
import requests
from flask_login import login_required
from .import bp as main


@main.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')


