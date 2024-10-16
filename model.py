from find_chunks_similarity import get_most_similar_chunks
import itertools as itt

import util as ut
import config as cf

question = "Reduzido à sua forma abstrata, o argumento do cidadão Weston traduzir-se-ia no seguinte:"
similar_chunks = get_most_similar_chunks(question, 5)

chunks_str = [f'[{n+1}]: {chunk}' for n, chunk in zip(itt.count(), [chunk for _, chunk in similar_chunks])]
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



