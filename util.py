import re
import os
from os import listdir
from os.path import isfile, join
import shutil

from langchain_ollama import OllamaLLM
from openai import OpenAI

import config as cf

def get_file_names():
    docs = list_files(f'./{cf.FOLDER_DOCS}')
    return docs

def split_lower_followed_by_upper(str):
    clean = re.compile(r'([a-z])([A-Z])')
    return re.sub(clean, r'\1 \2', str)

def create_path_if_not_exists(newpath):
    if not os.path.exists(newpath):
        os.makedirs(newpath)

def list_files(mypath):
    return [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".pdf")]

def delete_all_chunks():
    chunks_path = f'./{cf.FOLDER_CHUNKS}/'
    try:
        shutil.rmtree(chunks_path)
    except:
        print('Falha ao remover pastas')

def get_response(model, prompt):
    if model in cf.OLLAMA_MODELS:
        llm = OllamaLLM(model=model)
        response = llm.invoke(prompt)
    return response