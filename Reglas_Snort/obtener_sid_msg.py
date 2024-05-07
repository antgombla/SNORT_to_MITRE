import os
import re
from utils_excel import *

ruta_carpeta = "Reglas"
reglas = {}
num_reglas = 0
sids = []
columnas = ["msg"]

# Se extrae el sid y el mensaje de cada regla, para todos los archivo
for nombre_archivo in os.listdir(ruta_carpeta):
        ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)
        # Si es un fichero se lee
        if os.path.isfile(ruta_archivo):
            try:
                with open(ruta_archivo, 'r', encoding="utf-8") as archivo:
                    contenido = archivo.read()
                    # Utiliza expresiones regulares para encontrar las intenciones
                    # Expresión regular para buscar el patrón "alert" seguido de msg y sid
                    patron_alert = re.compile(r"alert[^)]+\( msg:\"([^\"]+)\";[^)]+sid:(\d+);")
                    # Buscar todas las coincidencias
                    coincidencias = patron_alert.findall(contenido)
                    for msg, sid in coincidencias:
                        #print(f"Mensaje: {msg}, SID: {sid}")
                        if int(sid) not in sids:
                            reglas[int(sid), 'msg'] = msg
                            sids.append(int(sid))
                            num_reglas += 1
            except FileNotFoundError:
                print(f"El archivo {nombre_archivo} no se encontró")
            except Exception as e:
                print(f"Error al procesar el archivo {nombre_archivo}: {str(e)}")

# Datos del excel donde se van a almacenar los datos
excel_name = 'ReglasSnort2.xlsx'
try:
    libro_excel = openpyxl.load_workbook(excel_name)
    sheet =  libro_excel['Reglas']
    Range1 = 'A1'
    Range2 = f'B{num_reglas+1}'
    # Write list in excel
    sids.sort()
    Write_Dic_to_Excel(libro_excel, excel_name, sheet, reglas, Range1, Range2, sids, columnas)
    # Cierra el archivo
    libro_excel.close()
except FileNotFoundError:
    print(f"El archivo '{excel_name}' no se encontró.")
except Exception as e:
    print(f"Ocurrió un error inesperado al escribir el excel: {e}")
print(f"Número de reglas encontradas: {num_reglas}")