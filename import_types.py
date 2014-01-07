__author__ = 'schwa'


#!/usr/local/bin/python

import Foundation
import PyObjCTools

import json



thePath = '/System/Library/CoreServices/CoreTypes.bundle/Contents/Info.plist'

thePlist = Foundation.NSDictionary.dictionaryWithContentsOfFile_(thePath)

theDocumentTypes = thePlist['UTExportedTypeDeclarations']

theDocumentTypes = PyObjCTools.Conversion.pythonCollectionFromPropertyList(theDocumentTypes)

print theDocumentTypes

json.dump(theDocumentTypes, file('Test.json', 'w'), sort_keys = True, indent = 4)
