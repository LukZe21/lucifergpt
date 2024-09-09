from openai import OpenAI
from yandex.Translater import Translater
from model import main_model
from search import google_search
import random
import os
import time

yandex_api = # your api key

api_key = # your api key
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
    time.sleep(3)
    message = translate_text(message, 'ka', 'en')
    search_query = client.chat.completions.create(
        model='gpt-3.5-turbo-1106',
        messages=[
            {'role': 'system',
            'content': 'You are a computer program which gets user messages as inputs.\n' 
                        'You should only generate search query according to message for google search.\n'
                        'Do not say anything other than that.'},
            {"role": "user", "content": message}
        ]
    )
    print(search_query.choices[0].message.content)
    response = main_model(search_query.choices[0].message.content)
    en_to_geo = translate_text(response)
    result = process_text(en_to_geo)
    return result

