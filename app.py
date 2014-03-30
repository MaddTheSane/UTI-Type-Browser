__author__ = 'schwa'

from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
import json
import os

app = Flask(__name__)

types_by_identifier = json.load(file('processed.json'))

@app.route("/")
@app.route("/roots")
def roots():
    hits = []
    for t in types_by_identifier.values():
        if 'UTTypeConformsTo' not in t or not t['UTTypeConformsTo']:
            hits.append(t)
    hits = sorted(hits, key = lambda t:t['UTTypeIdentifier'])
    return render_template('list.html', all_types = hits)

@app.route("/all")
def all():
    hits = types_by_identifier.values()
    hits = sorted(hits, key = lambda t:t['UTTypeIdentifier'])
    return render_template('list.html', all_types = hits)

@app.route("/public")
def public():
    hits = []
    for t in types_by_identifier.values():
        if 'UTTypeConformsTo' not in t or not t['UTTypeConformsTo']:
            if t['UTTypeIdentifier'].startswith('public.'):
                hits.append(t)

    hits = sorted(hits, key = lambda t:t['UTTypeIdentifier'])
    return render_template('list.html', all_types = hits)

@app.route("/identifier/<identifier>")
def type_(identifier):
    t = types_by_identifier[identifier]
    image_path = url_for('static', filename='iconsets')
    return render_template('type.html', type = t, image_path = image_path)

@app.route('/search', methods = ['POST'])
def search():

    query = request.form['query']

    hits = []
    for t in types_by_identifier.values():
        if query in t['UTTypeIdentifier']:
            hits.append(t)

    return render_template('list.html', all_types = hits)


# if __name__ == "__main__":
#     if os.environ.get('PYCHARM_HOSTED', False):
#         app.debug = True
#         app.run()
#     else:
#         app.run()

if __name__ == '__main__':
    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 5000))
    if os.environ.get('DEVELOPMENT', False):
        host = None
    app.debug = True
    app.run(host = host, port = port)
