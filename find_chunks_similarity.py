from difflib import SequenceMatcher
import multiprocessing as mp
from glob import iglob
from nltk.tokenize import word_tokenize
from gensim.models.doc2vec import Doc2Vec
import numpy as np
from gensim import matutils

import config as cf
import util as ut

doc2vec_model = Doc2Vec.load(f'./{cf.FILE_WORD2VEC_MODEL}')

def similarity_vector(chunk_vec_dict, vec_to_compare):
    chunk_vec = chunk_vec_dict['vec']
    sim = np.dot(matutils.unitvec(chunk_vec), matutils.unitvec(vec_to_compare))
    chunk_vec_dict['similarity'] = sim
    return chunk_vec_dict

def similarity(chunk, str_to_compare):
    """
    Retorna similaridade entre chunk e frase
    """
    sim = SequenceMatcher(None, chunk, str_to_compare).ratio()
    return (sim, chunk)

def load_chunk(chunk_file_name):
    """
    Carrega chunk
    """
    with open(chunk_file_name, 'r') as f:
        chunk = f.read()
    return chunk

def get_all_saved_chunks():
    """
    Retorna stream de chunks
    """
    chunks_files = iglob(f'./{cf.FOLDER_CHUNKS}/*/*.txt', recursive=True)
    chunks = (load_chunk(chunk_file_name) for chunk_file_name in chunks_files)
    return chunks

def get_saved_chunks(file_names):
    chunks = (load_chunk(chunk_file_name) for chunk_file_name in file_names)
    return chunks

def get_vec_chunks():
    """
    Retorna stream de chunks
    """
    chunks_files = iglob(f'./{cf.FOLDER_CHUNKS}/*/*.vec.npy', recursive=True)
    # chunks = (load_chunk(chunk_file_name) for chunk_file_name in chunks_files)
    chunks_dicts = (
        {
            'file_name': chunk_file_name,
            # 'vec': load_chunk(chunk_file_name),
            'vec': np.load(chunk_file_name),
        } for chunk_file_name in chunks_files
        )
    return chunks_dicts

def get_most_similar_chunks(str_to_compare, amount_to_return):
    """
    Retorna chunks similares
    """
    
    pool = mp.Pool(processes=cf.N_PROCESSES)
    
    # chunk_stream = get_chunks()
    # ls_sim_input = ((chunk, str_to_compare,) for chunk in chunk_stream)
    # similarities = pool.starmap(similarity, ls_sim_input, chunksize=30)
    # sorted_similarities = sorted(similarities, reverse=True)
    # return sorted_similarities[:amount_to_return]


    vector_to_compare = doc2vec_model.infer_vector(word_tokenize(str_to_compare.lower()))
    chunks_vec = get_vec_chunks()
    ls_sim_input = ((chunk, vector_to_compare,) for chunk in chunks_vec)
    similarities = pool.starmap(similarity_vector, ls_sim_input, chunksize=30)
    sorted_similarities = sorted(similarities, reverse=True, key=lambda ch_dict: ch_dict['similarity'])
    filtered_file_names_vec = [(ch_dict['similarity'], ch_dict['file_name']) for ch_dict in sorted_similarities[:amount_to_return]]
    filtered_file_names_txt = [(sim, file_name.replace('.vec.npy', '.txt')) for sim, file_name in filtered_file_names_vec]
    chunks_txt = [(sim, load_chunk(file_name)) for sim, file_name in filtered_file_names_txt]
    
    return chunks_txt

