#-*- coding: utf-8 -*-

import locale
import requests 

class TranslaterApiKey(Exception):
    '''
    Please set Api key
    '''

class TranslaterText(Exception):
    '''
    Please set Text
    '''

class TranslaterLang(Exception):
    '''
    Please set source lang
    Or
    Please set destination lang
    '''

class TranslaterInvalidKey(Exception):
    '''
    Invalid API key
    '''

class TranslaterBlockedKey(Exception):
    '''
    Blocked API key
    '''

class TranslaterTextFormat(Exception):
    '''
    Text Format invalid
    '''


class TranslaterError(Exception):
    '''
    Exceeded the daily limit on the amount of translated text
    Or
    Exceeded the maximum text size
    Or
    The text cannot be translated
    Or
    The specified translation direction is not supported
    Or
    Failed to translate text! text_example
    Or
    Failed to get list of supported languages!
    Or
    Failed to detect the language!
    '''

class Translater(object):

    def __init__(self, key = None, text = None, 
                 from_lang = None, to_lang = None, 
                 hint = [], ui = None):
        self.valid_lang = ['az','sq','am','en','ar','hy','af','eu','ba','be','bn','my',
                          'bg','bs','cy','hu','vi','ht','gl','nl','mrj','el','ka','gu',
                           'da','he','yi','id','ga','it','is','es','kk','kn','ca','ky',
                           'zh','ko','xh','km','lo','la','lv','lt','lb','mg','ms','ml',
                           'mt','mk','mi','mr','mhr','mn','de','ne','no','pa','pap','fa',
                           'pl','pt','ro','ru','ceb','sr','si','sk','sl','sw','su','tg',
                           'th','tl','ta','tt','te','tr','udm','uz','uk','ur','fi','fr',
                           'hi','hr','cs','sv','gd','et','eo','jv','ja']

        self.valid_text_format = ['plain', 'html']
        self.valid_default_ui = ['ru','en','tr']

        if not locale.getlocale()[0]:
            self.default_ui = 'en'
        else:
            self.default_ui = locale.getlocale()[0].split('_')[0]

        if not self.default_ui in self.valid_lang:
            self.default_ui = 'en'

        if not ui: self.ui = self.default_ui
        self.hint = hint
        self.base_url = 'https://translate.yandex.net/api/v1.5/tr.json/'
        self.key = key
        self.text = text
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.text_format = 'plain'

    def set_key(self, key):
        if not isinstance(key, str):
            raise TypeError('key must be string')

        if not key:
            raise TranslaterApiKey('key must not be empty')

        self.key = key

    def set_text(self, text):
        if not isinstance(text, str):
            raise TypeError('text must be string')

        if not text:
            raise TranslaterText('text must not be empty')

        self.text = text

    def set_default_ui(self, lang):
        if not isinstance(lang, str):
            raise TypeError('lang must be string')

        if not lang in self.valid_lang:
            raise TranslaterLang('lang not supported by yandex')

        if lang in self.valid_lang:
            self.default_ui = lang

    def set_ui(self, lang):
        if not isinstance(lang, str):
            raise TypeError('lang must be be string')

        if lang in self.valid_lang:
            self.ui = lang
        else:
            self.ui = self.default_ui

    def set_text_format(self, text_format):

        if not text_format in self.valid_text_format:
            raise Exception('')

        self.text_format = text_format

    def set_hint(self, *langs):
        for lang in langs:
            if not lang:
                raise TypeError('lang must not be empty')

            if not isinstance(lang, str):
                raise TypeError('lang must be string')

            if not lang in self.valid_lang:
                raise TranslaterLang('lang not supported by yandex')

            self.hint.append(lang)

    def set_from_lang(self, lang):
        if not lang:
            raise TranslaterLang('lang must not be empty')

        if not isinstance(lang, str):
            raise TypeError('lang must be string')

        if not lang in self.valid_lang:
            raise TranslaterLang('lang not supported by yandex')

        self.from_lang = lang

    def set_to_lang(self, lang):
        if not lang:
            raise TranslaterLang('lang must not be empty')

        if not isinstance(lang, str):
            raise TypeError('lang must be string')

        if not lang in self.valid_lang:
            raise TranslaterLang('lang not supported by yandex')

        self.to_lang = lang

    def translate(self):

        self.set_key(self.key)

        self.set_text(self.text)

        if not self.from_lang:
            self.from_lang = self.detect_lang()
            self.set_from_lang(self.from_lang)

        self.set_to_lang(self.to_lang)

        data = { 'key' : self.key, 'text' : self.text, 
                'lang' : '{0}-{1}'.format(self.from_lang, self.to_lang), 'format' : self.text_format }
        
        query = 'translate?'
        url = self.base_url + query 
        response = requests.post(url, data)

        if response.status_code == 401:
            raise TranslaterApiKey('Invalid API key')
        
        if response.status_code == 402:
            raise TranslaterBlockedKey('Blocked API key')
        
        if response.status_code == 404:
            raise TranslaterError('Exceeded the daily limit on the amount of translated text')
        
        if response.status_code == 413:
            raise TranslaterError('Exceeded the maximum text size')
        
        if response.status_code == 422:
            raise TranslaterError('The text cannot be translated')
        
        if response.status_code == 501:
            raise TranslaterError('The specified translation direction is not supported')

        if not response.status_code == 200:
            raise TranslaterError('Failed to translate text! {0}'.format(response.reason))
        
        result = response.json()
        
        return result['text'][0]

    def detect_lang(self):
        if not self.key:
            raise TranslaterApiKey('Please set Api key')

        if not self.text:
            raise TranslaterText('Please set Text')

        data = {'key' : self.key, 'text' : self.text, 'hint' : ','.join(self.hint)}
        
        query = 'detect?'
        
        url = self.base_url + query
        
        response = requests.post(url, data)

        if response.status_code == 401:
            raise TranslaterInvalidKey('Invalid API key')
        
        if response.status_code == 402:
            raise TranslaterBlockedKey('Blocked API key')
        
        if response.status_code == 404: 
            raise TranslaterError('Exceeded the daily limit on the amount of translated text')
        
        if not response.status_code == 200:
            raise TranslaterError('Failed to detect the language! (response code {0}'.format(response.reason))
        
        result = response.json()
        
        return result['lang']

    def get_langs(self):
        if not self.key:
            raise TranslaterApiKey('Please set Api key')

        data = {'key' : self.key, 'ui' : self.ui}
        query = 'getLangs?'
        url = self.base_url + query
        response = requests.get(url, data)

        if response.status_code == 401:
            raise TranslaterInvalidKey('Invalid API key')

        if response.status_code == 402:
            raise TranslaterBlockedKey('Blocked API key')

        if not response.status_code == 200:
            raise TranslaterError('Failed to get list of supported languages! (response code {0}'.format(response.reason))
        
        result = response.json()
        
        return result['dirs']
