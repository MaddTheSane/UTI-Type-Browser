__author__ = 'schwa'


#!/usr/local/bin/python

import Foundation
import PyObjCTools

import json

# thePath = '/System/Library/CoreServices/CoreTypes.bundle/Contents/Info.plist'
#
# thePlist = Foundation.NSDictionary.dictionaryWithContentsOfFile_(thePath)
#
# theDocumentTypes = thePlist['UTExportedTypeDeclarations']
#
# theDocumentTypes = PyObjCTools.Conversion.pythonCollectionFromPropertyList(theDocumentTypes)
#
# print theDocumentTypes
#
# json.dump(theDocumentTypes, file('Test.json', 'w'), sort_keys = True, indent = 4)

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

json.dump(types_by_identifier, file('processed.json', 'w'))
