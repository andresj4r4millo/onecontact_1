from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
#para el libro de exporte
import openpyxl
from unidecode import unidecode
import re
import pandas as pd
import numpy as np
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select




df = pd.read_csv('BASEP.csv', encoding = 'latin-1')
df.replace('nan', np.nan, inplace=True)
df

contador=0
iterador=1
nipn=0
with open('BASEP2.csv', 'w', encoding='utf-8', newline='') as archivo:
    archivo.write('CEDULA:  COMPLEMENTO\n') 

    for row, datos in df.iterrows():
        print(f"iteracion: {iterador}")
        iterador+=1
        cedulaa=datos["CEDULAA"]
        cc=datos["CEDULA"]
        apellido=datos["APELLIDO"]
        ##celular
        celular=datos["MIN_AP"]
        nipn=datos["NIP"]
        serialsim=datos["SERIAL_SIM"]
        ##celular: no usar, valor ==0
        correo=datos["CORREO"]
        planb=datos["PLAN"]
        conver=datos["CONVERGENCIA"] 
        operr=datos["OPERADOR"]
        operador=str(operr)
        convergencia=str(conver)

        nip=str(nipn).rjust(5,"0")
        
        #condicion sellecion
        cedula=str(cc)
        plan=str(planb)

        match = re.search(r'\d{5}', plan)

        if match:
            tu_plan_deseado = match.group()
        #seleccion
        #ciclo
        data_frame = pd.read_excel('CAMPAÑASB.xlsx', sheet_name='Hoja1')

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
            seleccion = "/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div/div/div/div[2]/div[10]/fieldset/div[1]/span/span/input"
            seleccion = "seleccion por defecto"
        

        datosfila=(f"{cedula}: {operador}, {convergencia}, {plan},{seleccion}")
        print(datosfila)
        archivo.write(datosfila + '\n')
        archivo.flush()
    
 