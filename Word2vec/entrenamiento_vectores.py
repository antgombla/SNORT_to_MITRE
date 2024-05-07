import string
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from sklearn.cluster import KMeans
from utils import leer_documentos
from utils_excel import Read_Excel_to_Dic, Read_Excel_to_List

ruta_carpeta = "Textos"
todos_los_textos = leer_documentos(ruta_carpeta)
    
# PREPROCESAMIENTO DE DATOS
# Convertir el texto en una lista de frases, cada frase en una lista de plabras, eliminar signos de puntuación
# y convertir el texto a minúsculas
tamano = 0
frases_totales = []
for documento in todos_los_textos:
    tamano += len (documento)
    frases = documento.split('.')
    frases_totales.extend(frases)

frases_limpias = []
for frase in frases_totales:
    palabras = frase.translate(str.maketrans('', '', string.punctuation)).split()
    palabras_min = []
    for word in palabras:
        if isinstance(word, str):
            palabras_min.append(word.lower())
        else:
            palabras_min.append(word)
    if palabras_min:
        frases_limpias.append(palabras_min)

# ENTRENAMIENTO DEL MODELO WORD2VEC
model = Word2Vec(sentences=frases_limpias, vector_size=500, window=5, min_count=1, workers=6)

# Guardar el modelo
model.save("nombre_modelo.model")
# modelo_cargado = Word2Vec.load("nombre_modelo.model")

# Guardar los embeddings
# model.wv.save_word2vec_format("mine_emb.txt", binary=False)
model.wv.save_word2vec_format("mine_emb.bin", binary=True)
# embeddings_cargados = KeyedVectors.load_word2vec_format('embeddings.txt', binary=False)
embeddings_cargados = KeyedVectors.load_word2vec_format('mine_emb.bin', binary=True)

'''
#
# Obtener los vectores para las reglas de Snort
#

# Parámetros del excel
num_reglas = 36873
sheet  = 'Reglas'
excel_name = 'ReglasSnort2.xlsx'
Range1 = 'A1'
Range2 = f'E{num_reglas+1}'
# Se obtienen los sid, el nombre de las columnas y el diccionario completo
try:
    sids     = Read_Excel_to_List(excel_name, sheet, 'A2', f'A{num_reglas+1}')
    columnas = ["msg"]
    reglas   = Read_Excel_to_Dic(excel_name, sheet, Range1, Range2)
except FileNotFoundError:
    print(f"El archivo '{excel_name}' no se encontró.")
except Exception as e:
    print(f"Ocurrió un error inesperado al escribir el excel: {e}")

# Se obtiene la vectorización de cada regla
vectores_reglas = []
for sid in sids:
    palabras_regla = reglas[int(sid), 'msg'].translate(str.maketrans('', '', string.punctuation)).split()

    palabras_regla_min = []
    for word in palabras_regla:
        if isinstance(word, str):
            palabras_regla_min.append(word.lower())
        else:
            palabras_regla_min.append(word)
    vector_regla = sum(embeddings_cargados[word] for word in palabras_regla_min if word in embeddings_cargados)
    vectores_reglas.append(vector_regla)

# Agrupamos las reglas
kmeans = KMeans(n_clusters=3)
kmeans.fit(vectores_reglas)
etiquetas_clusters = kmeans.labels_

# Asignar cada regla a su respectivo cluster
clusters = {}
for i, regla in enumerate(reglas_snort):
    cluster_id = etiquetas_clusters[i]
    if cluster_id not in clusters:
        clusters[cluster_id] = []
    clusters[cluster_id].append(regla)

# Imprimir los resultados
for cluster_id, reglas in clusters.items():
    print(f"Cluster {cluster_id}:")
    for regla in reglas:
        print(f"  - {regla}")

'''