import requests
from utils_excel import *
from bs4 import BeautifulSoup
import time

# Parámetros del excel
num_reglas = 36873
sheet  = 'Reglas'
excel_name = 'ReglasSnort2.xlsx'
Range1 = 'A1'
Range2 = f'E{num_reglas+1}'
# Se obtienen los sid, el nombre de las columnas y el diccionario completo
try:
    sids     = Read_Excel_to_List(excel_name, sheet, 'A2', f'A{num_reglas+1}')
    columnas = Read_Excel_to_List(excel_name, sheet, 'B1', 'E1')
    reglas   = Read_Excel_to_Dic(excel_name, sheet, Range1, Range2)
except FileNotFoundError:
    print(f"El archivo '{excel_name}' no se encontró.")
except Exception as e:
    print(f"Ocurrió un error inesperado al escribir el excel: {e}")

# Se obtine la táctica y técnica mitre de las reglas que contienen esa información
# en la documentación
for sid in sids:
    if reglas[sid, 'Tactic_MITRE'] == 'NO':
        url = f"https://www.snort.org/rule_docs/1-{sid}"
        response = requests.get(url)
        print(sid)
        if response.status_code == 200:
            # Extraer información del HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            description_element = soup.find("p", class_="rule-explanation")
            tactic_element = soup.find("p", class_="mitre-tactic")
            technique_element = soup.find("p", class_="mitre-technique")

            # Almacenamos la descripción
            if description_element:
                reglas[sid, 'Rule Description'] = description_element.text.split("\n\n")[0].strip()
            else:
                reglas[sid, 'Rule Description'] = "MISSING DOCUMENTATION"
                print("Missing Documentation")
            
            # Verificamos si se encontraron los elementos
            if tactic_element and technique_element:
                # Extraemos el texto de la táctica y la técnica
                tactic = tactic_element.text.split(":")[1].strip()
                technique = technique_element.text.split(":")[1].strip()
                # Almacenamos la táctica y la técnica
                reglas[sid, 'Tactic_MITRE'] = tactic
                reglas[sid, 'Technique_MITRE'] = technique
                # print("Táctica:", tactic)
                # print("Técnica:", technique)
            else:
                print("No se encontraron la táctica y/o la técnica en la página.")
                reglas[sid, 'Tactic_MITRE'] = " "
                reglas[sid, 'Technique_MITRE'] = " "
        else:
            print("Error al realizar la solicitud:", response.status_code)
            reglas[sid, 'Tactic_MITRE'] = "NO"
            reglas[sid, 'Technique_MITRE'] = "NO"
            # raise ValueError("PARADO")
            time.sleep(60)
        time.sleep(3)

#%%
for sid in sids:
    if reglas[sid, 'Tactic_MITRE'] is None:
        reglas[sid, 'Tactic_MITRE'] = "NO"
        reglas[sid, 'Technique_MITRE'] = "NO"

for sid in sids:
    if reglas[sid, 'Tactic_MITRE'] == " " or reglas[sid, 'Technique_MITRE'] == " ":
        reglas[sid, 'Tactic_MITRE'] = ""
        reglas[sid, 'Technique_MITRE'] = ""

try:
    libro_excel = openpyxl.load_workbook(excel_name)
    sheet = libro_excel['Reglas']
    # Write list in excel
    Write_Dic_to_Excel(libro_excel, excel_name, sheet, reglas, Range1, Range2, sids, columnas)
    # Cierra el archivo
    libro_excel.close()
except FileNotFoundError:
    print(f"El archivo '{excel_name}' no se encontró.")
except Exception as e:
    print(f"Ocurrió un error inesperado al escribir en excel: {e}")