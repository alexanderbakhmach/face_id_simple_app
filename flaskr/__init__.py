import logging
import cv2
import face_recognition
import base64
import numpy as np
import json
import datetime

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask.json import JSONEncoder

from werkzeug.exceptions import BadRequest

from functools import wraps
from jsonschema import validate
from jsonschema import ValidationError

from .validators.main import validate_schema
from .validators.main import validate_json
from .validators.user import create_schema as user_create_schema

from bson.json_util import dumps
from bson.json_util import CANONICAL_JSON_OPTIONS


CONFIG_PATH = './config.py'


app = Flask(__name__)
app.config.from_pyfile(CONFIG_PATH)

mongo = PyMongo(app)

log_file_path = app.config.get('LOG_FILE_PATH')

if log_file_path:
    logging.basicConfig(filename=log_file_path)

from .services import user as user_service

from .controllers.user import *
from .controllers.capture import *
from .controllers.main import *


