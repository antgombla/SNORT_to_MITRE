from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from utils import *

# Carga el modelo y los embeddings
model = Word2Vec.load("nombre_modelo.model")
embeddings_cargados = KeyedVectors.load_word2vec_format('mine_emb.bin', binary=True)

# Comprobaciones del modelo
#vector = model.wv['detective']
#print(vector)
#palabras_cercanas = model.wv.most_similar("hombre", topn=10)
#print(palabras_cercanas)
analogias('niño', 'hombre', 'mujer', embeddings_cargados)