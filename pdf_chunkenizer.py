import itertools as itt
import multiprocessing as mp
from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import Doc2Vec
from pypdf import PdfReader
import numpy as np

import util as ut
import config as cf
from pdf_stream import extract_words, words_to_chunks, save_chunk, pdf_to_chunks

doc2vec_model = Doc2Vec.load(f'./{cf.FILE_WORD2VEC_MODEL}')

def chunkenize(file_name):
    """
    Gera e salva chunks
    """

    # Cria pasta para o arquivo
    chunk_folder_path = f'./{cf.FOLDER_CHUNKS}/{file_name}.chunks'
    ut.create_path_if_not_exists(chunk_folder_path)

    # Gera stream de chunks
    chunk_stream = pdf_to_chunks(file_name)
    
    # Salva chunks
    for chunk, n in zip(chunk_stream, itt.count()):
        chunk_file_name = f'{chunk_folder_path}/chunk_{n}.txt'
        save_chunk(chunk, chunk_file_name)

def chunkenize_vector(file_name):
    """
    Gera e salva chunks com vetorização
    """
    
    # Cria pasta para o arquivo
    chunk_folder_path = f'./{cf.FOLDER_CHUNKS}/{file_name}.chunks'
    ut.create_path_if_not_exists(chunk_folder_path)

    # Gera stream de chunks
    chunk_stream = pdf_to_chunks(file_name)
    
    # Salva chunks
    for chunk, n in zip(chunk_stream, itt.count()):
        chunk_file_name = f'{chunk_folder_path}/chunk_{n}.txt'
        save_chunk(chunk, chunk_file_name)

        chunk_vec_file_name = f'{chunk_folder_path}/chunk_{n}.vec'
        chunk_vec = doc2vec_model.infer_vector(word_tokenize(chunk.lower()))
        np.save(chunk_vec_file_name, chunk_vec)



def main():
    ut.delete_all_chunks()
    docs = ut.get_file_names()
    pool = mp.Pool(cf.N_PROCESSES)
    pool.map(chunkenize_vector, docs) # usados para similaridade
    

if __name__ == '__main__':
    main()
