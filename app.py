__author__ = 'schwa'

from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
import json
import os

app = Flask(__name__)

info = json.load(file('Info.json'))
all_types = info['UTExportedTypeDeclarations'] + info['UTImportedTypeDeclarations']
types_by_identifier = { t['UTTypeIdentifier']: t for t in all_types }
del all_types

def listify(o):
    if isinstance(o, basestring):
        return [o]
    else:
        return o

for t in types_by_identifier.values():
    if 'UTTypeConformsTo' in t:
        t['UTTypeConformsTo'] = listify(t['UTTypeConformsTo'])
        if 'UTTypeTagSpecification' in t:
            tags = t['UTTypeTagSpecification']
            if 'public.filename-extension' in tags:
                tags['public.filename-extension'] = listify(tags['public.filename-extension'])
            if 'public.mime-type' in tags:
                tags['public.mime-type'] = listify(tags['public.mime-type'])

        for conforming_t in t['UTTypeConformsTo']:
            if conforming_t not in types_by_identifier:
                types_by_identifier[conforming_t] = { 'UTTypeIdentifier': conforming_t}

            if 'UTTypeConformedBy' not in types_by_identifier[conforming_t]:
                types_by_identifier[conforming_t]['UTTypeConformedBy'] = []
            types_by_identifier[conforming_t]['UTTypeConformedBy'].append(t['UTTypeIdentifier'])

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


if __name__ == "__main__":
    if os.environ.get('PYCHARM_HOSTED', False):
        app.debug = True
        app.run()
    else:
        app.run()
