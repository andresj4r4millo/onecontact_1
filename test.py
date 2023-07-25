import pandas as pd





# Lee el archivo Excel
data_frame = pd.read_excel('CAMPAÑASB.xlsx', sheet_name='Hoja1')

# Define el plan, operador y convergencia deseados
tu_plan_deseado = 27751
operador = "TIGO"
convergencia = "SI"

# Filtra el DataFrame para obtener la fila deseada
fila_deseada = data_frame.loc[(data_frame['PLAN'] == tu_plan_deseado) & (data_frame['OPERADOR'] == operador)]

# Verifica si se encontró una coincidencia
if not fila_deseada.empty:
    # Obtiene el dato correspondiente según la convergencia
    if convergencia == "SI":
        seleccion = str(fila_deseada['SI'].iloc[0])
    else:
        seleccion = str(fila_deseada['NO'].iloc[0])
else:
    # Si no se encontró una coincidencia, asigna una selección por defecto
    seleccion = "Selección por defecto"

# Imprime el resultado
print(seleccion)
