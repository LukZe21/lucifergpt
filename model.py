from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
import os
from search import google_search

os.environ["OPENAI_API_KEY"] = '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'

def main_model(user_input):
    query = user_input

    try:
        with open('Data/search.txt', 'w', encoding="utf-8") as f:
            f.write(google_search(query))
    except Exception as e:
        print("")

    text_loader_kwargs = {'autodetect_encoding': True}
    loader = DirectoryLoader('Data', glob='*.txt', loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
    index = VectorstoreIndexCreator().from_loaders([loader])

    result = index.query(query, llm=ChatOpenAI())
    return result