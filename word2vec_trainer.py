from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import nltk

import util as ut
import config as cf
from pdf_stream import get_all_chunks

nltk.download('punkt')
nltk.download('punkt_tab')

# Sample data
data = get_all_chunks()

# Tokenizing the data
tokenized_data = (word_tokenize(document.lower()) for document in data)

# Creating TaggedDocument objects
tagged_data = [TaggedDocument(words=words, tags=[str(idx)])
               for idx, words in enumerate(tokenized_data)]

# Training the Doc2Vec model
model = Doc2Vec(vector_size=100, window=2, min_count=1, workers=4, epochs=1000)
model.build_vocab(tagged_data)
model.train(tagged_data, total_examples=model.corpus_count,
            epochs=model.epochs)

model.save(f'./{cf.FILE_WORD2VEC_MODEL}')