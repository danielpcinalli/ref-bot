import itertools as itt
import multiprocessing as mp

from pypdf import PdfReader

import util as ut
import config as cf

# TODO: adicionar chunks doc2vec

def clean_page_text(page_text):
    """
    Retorna texto limpo
    """
    page_text = page_text   \
        .replace('\n', ' ') \
        .replace('\t', ' ')
    page_text = ut.split_lower_followed_by_upper(page_text)
    return page_text

def page_to_words(page):
    """
    Retorna palavras de uma página
    """
    page_text = page.extract_text()
    page_text = clean_page_text(page_text)
    words = page_text.split(' ')
    return words
        
def extract_words(pages):
    """
    Retorna stream de palavras
    """
    for page in pages:
        for word in page_to_words(page):
            yield word

def words_to_chunks(word_stream, chunk_size, overlap_size):
    """
    Transforma uma stream de palavras em uma stream de chunks com overlap
    """

    # Overlap inicial vazio
    overlap = []

    empty_generator = False

    while not empty_generator:
        # Chunk atual = overlap anterior + quantidade restante de palavras para ter chunk_size palavras
        chunk = overlap
        for _ in range(chunk_size-len(overlap)):
            try:
                chunk.append(next(word_stream))
            except StopIteration:
                # Se stream de palavras estiver vazia, termina loop
                empty_generator = True
        # Overlap de últimas overlap_size palavras do chunk atual
        overlap = chunk[-overlap_size:]
        yield ' '.join(chunk)

def save_chunk(chunk, chunk_file_name):
    """
    Salva um chunk
    """   
    with open(chunk_file_name, 'w') as f:
        f.write(chunk)


def chunkenize(file_name, chunk_size=150, overlap_size=15):
    """
    Gera e salva chunks
    """

    # Cria pasta para o arquivo
    chunk_folder_path = f'./{cf.FOLDER_CHUNKS}/{file_name}.chunks'
    ut.create_path_if_not_exists(chunk_folder_path)

    # Gera stream de chunks
    reader = PdfReader(f'./{cf.FOLDER_DOCS}/{file_name}')
    word_stream = extract_words(reader.pages)
    chunk_stream = words_to_chunks(word_stream, chunk_size=chunk_size, overlap_size=overlap_size)
    
    # Salva chunks
    for chunk, n in zip(chunk_stream, itt.count()):
        chunk_file_name = f'{chunk_folder_path}/chunk_{n}'
        save_chunk(chunk, chunk_file_name)
        

def main():
    ut.delete_all_chunks()
    docs = ut.list_files(f'./{cf.FOLDER_DOCS}')
    pool = mp.Pool(cf.N_PROCESSES)
    pool.map(chunkenize, docs)
    

if __name__ == '__main__':
    main()
