import PyPDF2
from tqdm import tqdm
import os
#
# Permite comprobar las analogías
#
# analogias('golden', 'key', 'pink', embeddings)
def analogias(v1, v2, v3, embeddings_cargados):
    similitud = embeddings_cargados.most_similar(positive=[v1, v3], negative=[v2])
    print(f"{v1} es a {v2} como {similitud[0][0]} es a {v3}")

#
# Permite cargar un txt
#
def leer_txt(titulo):
    try:
        # Carga de documento
        with open ('Word2vec\\Textos\\alice_in_wonderland.txt', 'r', encoding='utf-8') as file:
            documento = file.read()
            return documento
    except FileNotFoundError:
        print("El archivo no se encuentra en la ubicación")
        return None

#
# Permite cargar un pdf
#
def leer_pdf(titulo):
    with open(titulo, 'rb') as archivo:
        doc_preprocesado = PyPDF2.PdfReader(archivo)
        documento = ""
        for pagina in range(len(doc_preprocesado.pages)):
            documento += doc_preprocesado.pages[pagina].extract_text()
    return documento

#
# Permite cargar un conjunto de documentos
#
def leer_documentos(ruta_carpeta):
    todos_los_textos = []
    for archivo in tqdm(os.listdir(ruta_carpeta)):
        if (archivo.endswith('.pdf') or archivo.endswith('.txt')):
            ruta_completa = os.path.join(ruta_carpeta, archivo)
            try:
                if archivo.endswith('.pdf'):
                    documento = leer_pdf(ruta_completa)
                else:
                    documento = leer_txt(ruta_completa)
                todos_los_textos.append(documento)
            except Exception as e:
                print(f"Error al procesar {archivo}: {e}")
    return todos_los_textos