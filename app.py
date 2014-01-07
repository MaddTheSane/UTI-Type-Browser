__author__ = 'schwa'

from flask import Flask
from flask import render_template
from flask import url_for
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
                print conforming_t

            if 'UTTypeConformedBy' not in types_by_identifier[conforming_t]:
                types_by_identifier[conforming_t]['UTTypeConformedBy'] = []
            types_by_identifier[conforming_t]['UTTypeConformedBy'].append(t['UTTypeIdentifier'])




@app.route("/")
def index():
    return render_template('hello.html', all_types = types_by_identifier.values())

@app.route("/<identifier>")
def type_(identifier):
    t = types_by_identifier[identifier]
    image_path = url_for('static', filename='iconsets')
    return render_template('type.html', type = t, image_path = image_path)

if __name__ == "__main__":

    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 5000))
    if os.environ.get('DEVELOPMENT', False):
        host = None
    else:
        app.debug = True

    app.run(host = host, port = port)
