import ast
import json
import random
import re
import string
from pathlib import Path

import pandas as pd
from dateutil.parser import parse
from flask import Flask
from flask import render_template
from flask_restful import reqparse, abort, Api, Resource

from gaCentile import getCentile, getSFHData, get_plot

app = Flask(__name__, static_url_path='/static')
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201


class GACentile(Resource):
    def get(self):
        # return 'Submit data'
        return render_template("index.html")

    def post(self):
        args = parser.parse_args()
        centstring = args['task']
        gainput = re.search('ga(.*)bweight', centstring)
        gainput = int(gainput.group(1))
        bweight = re.search('bweight(.*)gender', centstring)
        bweight = int(bweight.group(1))
        gender = int(centstring.partition('gender')[2])

        uk90m = None
        t = 'loaded'

        filename_data_uk90M = str(Path.cwd() / 'static/uk90M.csv')
        filename_data_uk90F = str(Path.cwd() / 'static/uk90F.csv')
        filename_data_ukwhoM = str(Path.cwd() / 'static/ukwhoM.csv')
        filename_data_ukwhoF = str(Path.cwd() / 'static/ukwhoF.csv')

        centile = 0

        try:
            bw, gastr, centile, cent_ref = getCentile(gainput, bweight, gender)
            t = cent_ref
        except:
            t = 'wont process centile'

        # return t

        test1 = [ele for ele in ['1', '21', '31', '41', '51', '61', '71', '81', '91'] if (ele == str(centile))]
        test2 = [ele for ele in ['2', '22', '32', '42', '52', '62', '72', '82', '92'] if (ele == str(centile))]
        test3 = [ele for ele in ['3', '23', '33', '43', '53', '63', '73', '83', '93'] if (ele == str(centile))]

        if centile == 0:
            centilestr = '0th'
        elif centile == 1:
            centilestr = '%sst' % str(centile)
        elif test1:
            centilestr = '%sst' % str(centile)
        elif test2:
            centilestr = '%snd' % str(centile)
        elif test3:
            centilestr = '%srd' % str(centile)
        else:
            centilestr = '%sth' % str(centile)

        ga_string = {'bweight': bw, 'gastr': gastr, 'centile': centilestr, 'cent_ref': cent_ref}
        ga_string = json.dumps(ga_string)
        ga_string = json.loads(ga_string)

        return ga_string


api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(GACentile, '/ga')

if __name__ == '__main__':
    app.run()
