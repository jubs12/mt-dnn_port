#!/usr/bin/env python
# coding: utf-8

# Translate sentences to English and save mapping dicitionary as json.

# Based on https://github.com/ruanchaves/assin/blob/master/sources/translate.py

# Parameters:
# *   sentences =
# *   dictpath =  json dictionary file mapping original sentence with translation
# 
# 

# In[ ]:


from google.cloud import translate_v2 as translate
from os.path import isfile
from os import environ
import six
import json

def translate2dict(sentences, dictpath):
    environ['GOOGLE_APPLICATION_CREDENTIALS'] = './key.json'
    translate_client = translate.Client()

    def translation(text):
        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')
        result = translate_client.translate(text,'en')

        return result['translatedText']

    if not isfile(dictpath):
        with open(dictpath, 'w') as f:
            json.dump({}, f)

    for item in sentences:
        with open(dictpath) as f:
            translations = json.load(f)
        
        try:
            translations[item]
        except KeyError:
            translations[item] = translation(item)
            
            with open(dictpath, 'w+') as f:
                json.dump(translations, f)

