from pypdf import PdfReader

import util as ut
import config as cf




def get_all_chunks():
    """
    Retorna stream de chunks de todos os arquivos
    """
    file_names = ut.get_file_names()
    for file_name in file_names:
        chunk_stream = pdf_to_chunks(file_name)
        for chunk in chunk_stream:
            yield chunk

def pdf_to_chunks(file_name):
    """
    Retorna stream de chunks
    """
    reader = PdfReader(f'./{cf.FOLDER_DOCS}/{file_name}')
    word_stream = extract_words(reader.pages)
    chunk_stream = words_to_chunks(word_stream)
    return chunk_stream

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

def words_to_chunks(word_stream):
    """
    Transforma uma stream de palavras em uma stream de chunks com overlap
    """

    # Overlap inicial vazio
    overlap = []

    empty_generator = False

    while not empty_generator:
        # Chunk atual = overlap anterior + quantidade restante de palavras para ter cf.CHUNK_SIZE palavras
        chunk = overlap
        for _ in range(cf.CHUNK_SIZE-len(overlap)):
            try:
                chunk.append(next(word_stream))
            except StopIteration:
                # Se stream de palavras estiver vazia, termina loop
                empty_generator = True
        # Overlap de últimas cf.OVERLAP_SIZE palavras do chunk atual
        overlap = chunk[-cf.OVERLAP_SIZE:]
        yield ' '.join(chunk)

def save_chunk(chunk, chunk_file_name):
    """
    Salva um chunk
    """   
    with open(chunk_file_name, 'w') as f:
        f.write(chunk)