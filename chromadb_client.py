import chromadb

from pdf_stream import get_all_chunks_for_chromadb

client = chromadb.PersistentClient(path='knowledge-base')

collection = client.get_or_create_collection(name="knowledge-base")

# se coleção estiver vazia popula com pdfs
if collection.count() <= 0:
    gen_docs = get_all_chunks_for_chromadb()
    ids = []
    metadatas = []
    documents = []
    for id_, metadata, doc in gen_docs:
        ids.append(id_)
        metadatas.append(metadata)
        documents.append(doc)
    collection.add(ids=ids, metadatas=metadatas, documents=documents)
        

def get_collection():
    return collection