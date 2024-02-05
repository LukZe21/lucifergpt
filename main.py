from openai import OpenAI
from yandex.Translater import Translater
from model import main_model
from search import google_search
import random
import os
import time

yandex_api = 'trnsl.1.1.20231218T125713Z.5aedc37fb03eddd5.1a20119c7128cbb5f90c7e7c257a9beb7704cc57'

api_key = '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'
client = OpenAI(api_key=api_key)

def translate_text(text, detect='en', target_language='ka'):
    translater = Translater()
    translater.set_key(yandex_api)
    translater.set_text(text)
    translater.set_from_lang(f'{detect}')
    translater.set_to_lang(target_language)

    translation = translater.translate()
    return translation

def process_text(text):
    words = []
    word_dic = {'დაეხმაროს': 'დავეხმარო', 'დაეხმარეთ':'დაგეხმაროთ', 'ვთხოვო': 'მთხოვეთ', tuple(['მოგვაწოდოთ', 'მიაწოდოთ']): 'მომაწოდოთ', 'გეკითხებით': 'მეკითხებით', 'მოგერიდებათ': 'ნუ მოგერიდებათ', 'დაუსვათ': 'დამისვით', 'პითონი': 'პაითონი', 'შეგქმნა': 'შემქმნა', 'შევიმუშავე': 'შემიმუშავა'}
    for word in text.split(' '):
        if word in word_dic.keys():
            words.append(word_dic.get(word))
        else:
            words.append(word)
    return ' '.join(words)


def get_answer(message):
    message = translate_text(message, 'ka', 'en')
    search_query = client.chat.completions.create(
        model='gpt-3.5-turbo-1106',
        messages=[
            {'role': 'system',
            'content': 'You will recieve a text, make text more structured, easy and engaging.'},
            {"role": "user", "content": main_model(message)}
        ]
    )
    en_to_geo = translate_text(search_query.choices[0].message.content)
    result = process_text(en_to_geo)
    return result

