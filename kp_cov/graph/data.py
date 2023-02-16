# -*- coding: utf-8 -*-
import json
import sys
import random
import string
import math
if sys.version_info >= (3, 0):
    import urllib.request, urllib.parse, urllib.error
else:
    import urllib

def _byteify(data, ignore_dicts = False):
    if isinstance(data, str):
        return data

    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.items() # changed to .items() for python 2.7/3
        }

    # python 3 compatible duck-typing
    # if this is a unicode string, return its string representation
    if str(type(data)) == "<type 'unicode'>":
        return data.encode('utf-8')

    # if it's anything else, return it in its original form
    return data
if __name__=='__main__':
    with open('snd.json', 'r') as jsonFile:
          weatherData = json.load(jsonFile,object_hook=_byteify)
          print weatherData
    print weatherData['dev']
    for item in weatherData['cmd']:
        print item
    #for item in weatherData['type']:
    #print weatherData['type'][0]['arg1']
    #print json.dump(weatherData)
    data=json.dumps(weatherData)
    print type(weatherData)








