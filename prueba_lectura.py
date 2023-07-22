import openpyxl
from unidecode import unidecode
import re
# Abrir el archivo de Excel

workbook = openpyxl.load_workbook('exportacion_total.xlsx', read_only=True, data_only=True, keep_links=False, keep_vba=False)
# Seleccionar la hoja de cálculo que deseas leer
sheet = workbook['CONSULTA']

# Definir los índices de las columnas a modificar
columna_j = 'J'

columna_w = 'W'
# Crear una lista vacía para almacenar los datos extraídos
datos_extraidos = []

# Iterar sobre las filas en la hoja de cálculo
for index, row in enumerate(sheet.iter_rows(values_only=True), start=1):
    if index==1:
        continue
    cedulaa=str(row[4])
    cedula = str(row[8])  # Columna 'I'
    apellido_completo = str(row[9])  # Columna 'J'
    apellido = apellido_completo.split()[-1]
    min_ap = str(row[17])  # Columna 'Q'
    nipn = str(row[18]).replace(" ", "")[-12:]  # Obtener los últimos 12 dígitos de la columna 'R'
    serial= str(row[34]).replace(" ","")# Columna 'AH'
    serial_sim=(serial)[-12:]
    plan = str(row[23])  # Columna 'W'
    correo = str(row[22])  # Columna 'V'
    convergencia = str(row[24])  # Columna 'X'
    operador = str(row[16])  # Columna 'P'

    # Reemplazar caracteres desconocidos por caracteres específicos en las columnas deseadas
    nip = re.sub(r'\D', '', nipn)
    apellido_completo = unidecode(apellido_completo)
    plan = unidecode(plan)


    # Concatenar los datos en una sola cadena separada por comas
    datos_fila = ','.join([cedulaa,cedula, apellido, min_ap, nip, serial_sim, plan, correo, convergencia, operador])
    datos_extraidos.append(datos_fila)

# Cerrar el archivo de Excel
workbook.close()

# Insertar el encabezado en la lista de datos extraídos
encabezado = 'CEDULAA,CEDULA,APELLIDO,MIN_AP,NIP,SERIAL_SIM,PLAN,CORREO,CONVERGENCIA,OPERADOR'
datos_extraidos.insert(0, encabezado)

# Guardar los datos en un archivo CSV
with open('BASEP.csv', 'w' ,encoding='utf-8') as archivo:
    for dato in datos_extraidos:
        archivo.write(dato + '\n')