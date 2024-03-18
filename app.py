from flask import Flask
from flask import render_template
from flask_restful import reqparse, abort, Api, Resource

import ast
import json
import random
import re
import string
from pathlib import Path
import pandas as pd
from dateutil.parser import parse

app = Flask(__name__, static_url_path='/static')
api = Api(app)

app = Flask(__name__)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('request')


@app.route("/")
def hello_world():
    return render_template("index.html")


class GACentile(Resource):
    def get(self):
        return 'Submit data'

    def post(self):
        args = parser.parse_args()
        getstring = args['request']
        month_req = re.search('mm(.*)yyyy', getstring)
        month_req = str(month_req.group(1))
        year_req = re.search('yyyy(.*)item', getstring)
        year_req = str(year_req.group(1))
        item_req = str(getstring.partition('item')[2])
        filestr = item_req + '.html'
        filename = str(Path.cwd() / year_req / month_req / filestr)
        filetest = str(Path.cwd() / 'static/test.html')

        return render_template(filetest)