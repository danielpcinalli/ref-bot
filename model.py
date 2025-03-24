import itertools as itt
import sys

from chromadb_client import get_collection
import util as ut

def retrieve_chunks_get_answer(question):

    collection = get_collection()

    # passando para formato antigo de resposta para manter resto do código
    results = collection.query(query_texts=[question], n_results=5)
    similarities = results['distances'][0]
    docs = results['documents'][0]
    similar_chunks = zip(similarities, docs)


    chunks_str = [f' {similarity*100:.1f}% : [{n+1}]:  [...]{chunk}[...]: ' for n, (similarity, chunk) in zip(itt.count(), similar_chunks)]
    chunks_str = '\n'.join(chunks_str)

    prompt = f"""
    You are an assistant that answers questions from the user using references.
    Only answer the question, without adding opinion or extra text.
    Use the references to justify your answer. There is no need to use every reference presented.
    Answer in brazilian portuguese.

    Referências:
    {chunks_str}

    Pergunta:
    {question}
    """

    print('Prompt')
    print(prompt)

    models = ['llama3.1:8b', 'llama3.1:70b', 'phi3:14b', 'gemma2:27b']

    response = ut.get_response(models[0], prompt)

    print('Resposta')
    print(response)

def main():
    question = sys.argv[1]
    retrieve_chunks_get_answer(question)

if __name__ == '__main__':
    main()