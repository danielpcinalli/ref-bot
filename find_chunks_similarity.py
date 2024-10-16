from difflib import SequenceMatcher
import multiprocessing as mp
from glob import iglob

import config as cf
import util as ut

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

def get_chunks():
    """
    Retorna stream de chunks
    """
    chunks_files = iglob(f'./{cf.FOLDER_CHUNKS}/*/*', recursive=True)
    chunks = (load_chunk(chunk_file_name) for chunk_file_name in chunks_files)
    return chunks

def get_most_similar_chunks(str_to_compare, amount_to_return):
    """
    Retorna chunks similares
    """
    
    pool = mp.Pool(processes=cf.N_PROCESSES)

    chunk_stream = get_chunks()

    ls_sim_input = ((chunk, str_to_compare,) for chunk in chunk_stream)

    similarities = pool.starmap(similarity, ls_sim_input, chunksize=30)

    sorted_similarities = sorted(similarities, reverse=True)

    return sorted_similarities[:amount_to_return]
