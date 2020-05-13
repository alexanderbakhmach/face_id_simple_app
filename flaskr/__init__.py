import logging
import cv2
import face_recognition

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo


CONFIG_PATH = './config.py'


app = Flask(__name__)
app.config.from_pyfile(CONFIG_PATH)
mongo = PyMongo(app)

log_file_path = app.config.get('LOG_FILE_PATH')

if log_file_path:
    logging.basicConfig(filename=log_file_path)

from .controllers.user import *
from .controllers.capture import *
