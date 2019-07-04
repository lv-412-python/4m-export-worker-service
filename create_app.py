"""Create flask app"""
from flask import Flask
from flask_marshmallow import Marshmallow
#pylint: disable=unused-import
import delete_files

APP = Flask(__name__)

MA = Marshmallow(APP)

#pylint: disable=wrong-import-position
#pylint: disable=cyclic-import
import views.views
