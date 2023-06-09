#DRIVERS
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
#para el libro de exporte
import csv

import pandas as pd
import numpy as np
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

model_e="MOTOROLA"
reglist=[]
cone=0
errorlist=[]
doclist=[]
niplist=[]
operlist=[]
simlist=[]
numlist=[]
minimo=[]

#comentario
dicplan={
    "WOM": '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div/div/div/div[2]/div[4]/fieldset/div[1]/span/span/input',
    "TIGO": '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div/div/div/div[2]/div[13]/fieldset/div[1]/span/span/input',
    "MOVISTAR":'/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div/div/div/div[2]/div[4]/fieldset/div[1]/span/span/input',
    "WOMNO":'/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div/div/div/div[2]/div[7]/fieldset/div[1]/span/span/input',
    "TIGONO":'/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div/div/div/div[2]/div[14]/fieldset/div[1]/span/span/input',
    "MOVISTARNO":'/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div/div/div/div[2]/div[7]/fieldset/div[1]/span/span/input',
    "ETB":'/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div/div/div/div[2]/div[13]/fieldset/div[1]/span/span/input',
    "ETBNO":'/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div/div/div/div[2]/div[14]/fieldset/div[1]/span/span/input',
    "AVANTEL":'/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div/div/div/div[2]/div[4]/fieldset/div[1]/span/span/input',
    "AVANTELNO":'/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div/div/div/div[2]/div[7]/fieldset/div[1]/span/span/input'

}

complemento=""

def formularios(cedula,apellido,cedulaa,celular,nip,fechap,serialsim,errorlist,simlist,complemento):
    error="no"
    #primeros pasos, primer formulario
    #while con el fin de no lanzar error si el script no encuentra los elementos en la pagina
    cone=0
    while cone<6:
            print(f"iteracion: {str(cone)}")
            try:
                #FORMULARIO 1
                #LLENAR CEDULA //*[@id="DetailProduct_DocumentNumber"]porta = driver.find_element(By.XPATH, '//*[@id="viewErrors"]/ul/li[2]')
                ced=driver.find_element(By.XPATH, '//*[@id="DetailProduct_DocumentNumber"]')
                time.sleep(2)
                #ced=driver.find_element(By.XPATH('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[1]/div[2]/div/input'))
                ced.send_keys(cedula)

                #LLENAR APELLIDO
                driver.find_element('xpath','//*[@id="DetailProduct_LastName"]').clear()

                driver.find_element('xpath','//*[@id="DetailProduct_LastName"]').send_keys(apellido)
                #NO TRAJO EQUIPO
                driver.find_element('xpath','//*[@id="DetailProduct_WithoutImeiRegistryCheck"]').click()
                #CEDULA ASESOR
                accion = ActionChains(driver)
                accion.double_click(driver.find_element('xpath','//*[@id="DetailProduct_SellerId"]')).perform()
                driver.find_element('xpath','//*[@id="DetailProduct_SellerId"]').send_keys(cedulaa)
                time.sleep(1)
                #CHECK PORTABILIDAD NUMERICA
                driver.find_element('xpath','//*[@id="DetailProduct_PortabilityNumberCheck"]').click()
                #ESPERAR A QUE CARGUE POLIEDRO
                time.sleep(1)
                #MIN A PORTAR
                driver.find_element('xpath','//*[@id="DetailProduct_PortabilityNumber"]').send_keys(celular)
                #NIP //*[@id="DetailProduct_NIP"]
                driver.find_element('xpath','//*[@id="DetailProduct_NIP"]').click()
                driver.find_element(By.XPATH,'//*[@id="DetailProduct_NIP"]').send_keys(nip)
                #FECHA DE PORTACION
                #driver.find_element('xpath','//*[@id="DetailProduct_PortabilityDate"]').clear()
                #driver.find_element('xpath','//*[@id="DetailProduct_PortabilityDate"]').send_keys(fechap)
                campo_fecha=driver.find_element(By.ID,'DetailProduct_PortabilityDate')
                time.sleep(1)
                campo_fecha.clear()
                driver.execute_script(f'document.getElementById("DetailProduct_PortabilityDate").value = "{fechap}";')
                #SERIAL SIM CARD
                accion = ActionChains(driver)
                # /html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[2]/div[2]/div/input
                accion.double_click(driver.find_element('xpath',"/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[2]/div[2]/div/input")).perform()
                driver.find_element('xpath',"/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[2]/div[2]/div/input").send_keys(serialsim)
                
                break
            except:
                cone+=1
                continue
    
    
    if cone>=6:
        driver.find_element('xpath',"/html/body/span/span/span[2]/ul/li[2]").click()

    #llenar los ultimos datos y dar click en el boton de realizar consulta
    try:

        driver.find_element('xpath','//*[@id="DetailProduct_Iccid"]').click()
        driver.find_element('xpath','//*[@id="DetailProduct_Imei"]').click()        
        #ESPERAR A QUE CARGUE POLIEDRO 
        time.sleep(2)
        #PONER MIN PREACTIVADO
        driver.find_element('xpath','//*[@id="DetailProduct_MinBroughtPortability"]').click()
        driver.find_element('xpath','//*[@id="DetailProduct_MinBroughtPortability"]').send_keys(celular)
        time.sleep(2)
        #CONTINUAR   //*[@id="btnNext"]
        driver.find_element('xpath','//*[@id="btnNext"]').click()
        ##FORMULARIO 2    
        time.sleep(3)
        driver.find_element('xpath','/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div[2]/div[11]/div/div[2]/div[2]/div').click()  
    except:
        #SI LA CONSULTA NO SE REALIZA EL SIGUIENTE BUCLE DIGITA NUEVAMENTE LA CEDULA DEL ASESOR, LA FECHA Y REALIZA LA CONSULTA HASTA QUE SE REDIRIGA AL SISGUIENTE FORM
        cone=0
        
        while cone<8:

            try:
                accion = ActionChains(driver)
                accion.double_click(driver.find_element('xpath','//*[@id="DetailProduct_SellerId"]')).perform()
                driver.find_element(By.XPATH,'//*[@id="DetailProduct_SellerId"]').send_keys(cedulaa)
                time.sleep(1)
                #driver.find_element('xpath','//*[@id="DetailProduct_PortabilityDate"]').clear()
                #driver.find_element('xpath','//*[@id="DetailProduct_PortabilityDate"]').send_keys(fechap)
                campo_fecha.clear()
                driver.execute_script(f'document.getElementById("DetailProduct_PortabilityDate").value = "{fechap}";')
                #driver.find_element('xpath','//*[@id="DetailProduct_PortabilityDate"]').send_keys(Keys.ENTER)
                #time.sleep(1)
                try:
                    sim_adquirida=driver.find_element(By.XPATH,'//*[@id="DetailProduct_MinBroughtPortability"]')
                    sim_adquirida.click()
                    simlist.append(cedula)
                    print("sim adquirida")
                    complemento="sim adquirida"
                    cone=6
                    break
                except:

                    driver.find_element('xpath','//*[@id="btnNext"]').click()
                    ##FORMULARIO 2    
                    time.sleep(3)
                    driver.find_element('xpath','/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div[2]/div[11]/div/div[2]/div[2]/div').click()
                    break
            except:
                cone+=1

    #ESTAS LINEAS DE CODIGO GENERARAN ERROR SI LA PAGINA NO REALIZA LA CONSULTA DESPUES DE 6 INTENTOS
    if complemento=="sim adquirida":
        complemento=complemento
    else:
        complemento="error en los datos"
    if cone>=8:
        driver.find_element('xpath','//*[@id="DetailProduct_MinBroughtPortability"]').click()
        errorlist.append(cedula)

    

    
#ESTA FUNCION EVALUARA SI EL RECHAZO PASA O NO, Y EL PORQUE, PARA SEGMENTARLO POR LISTAS
def validaciones(doclist, niplist, operlist, complemento): 

    cone=0
    while cone<7:
        try:
            #driver.find_element(By.XPATH, '//*[@id="btnNext"]').click()
            #time.sleep(2) 
            #driver.find_element(By.XPATH, '//*[@id="ActivationClass_CfmToFirstInvoice"]')
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="btnNext"]').click()
            time.sleep(3) 
            driver.find_element(By.XPATH,'//*[@id="ActivationClass_CfmToFirstInvoice"]')
            break
        except:
            #regresar
            cone+=1
            continue 
    if cone>=6:
        try:
            #//*[@id="validationResponses"]/div[5]/div[2]/div[11]/div/div[2]/div[1]
            v_nip=driver.find_element(By.XPATH,'//*[@id="validationResponses"]/div[5]/div[2]/div[11]/div/div[2]/div[1]/div')
            if "El NIP no se encuentra vigente" in v_nip.text:
                niplist.append(cedula)
                complemento="el nip no se encuentra vigente"
            ##las siguientes lineas de codigo evaluan si el rechazo no pasa por el documento
            element = driver.find_element(By.XPATH,'//*[@id="validationResponses"]/div[6]/div[2]/div[3]/div/div/div')
            document= element.text
            if "DOCUMENTO NO APLICA PARA ACTIVACIÓN POLIEDRO"in element.text:
                doclist.appen(cedula)
                complemento="documento no aplica"
        except:
            print("documento aplica")
    if cone>=6:
        errorlist.append(cedula)  
        driver.find_element('xpath','//*[@id="DetailProduct_MinBroughtPortability"]').click()  
        #para generar error
        driver.find_element('xpath','//*[@id="ActivationClass_LinkPreactivation"]').click()

####FORMULARIO 3#####
#APARTIR DE AQUI SE DEFINE SI EL RECHAZO PASA O NO, HAY VARIAS ESTRUCTURAS PARA QUE LOS CAMPOS SEAN DILIGENCIADOS O LLENADOS
#CON EL FIN DE EVITAR QUE ALGUN CMPO QUEDE SIN SER SELECCIONADO ESTAN EN ESTRUCTURAS CICLICAS POR PASOS.



def forms2(correo,plan,reglist,selleccion,numlist,minimo,complemento):
    cone=0
    while True:
        try:
            driver.find_element(By.XPATH,'//*[@id="ActivationClass_CfmToFirstInvoice"]').click()
            driver.find_element('xpath','//*[@id="ActivationClass_LinkPreactivation"]').click()
            break
        except:
            continue
    cone=0
    while cone<=4:
        try:
            time.sleep(3)
            #CLASES DE ACTIVACION //*[@id="ActivationClass_CfmToFirstInvoice"]
            
            #CORREO DEL CLIENTE //*[@id="PersonalInfo_Email"]
            driver.find_element('xpath','//*[@id="PersonalInfo_Email"]').clear()
            driver.find_element('xpath','//*[@id="PersonalInfo_Email"]').send_keys(correo)
            time.sleep(1)
            #NUMERO DE TELEFONO 
            div_info=driver.find_element(By.ID,'group_4')
            print(div_info.text)
            nuevo=driver.find_element(By.XPATH,'//*[@id="select2-PhoneId-container"]')
            phone=driver.find_element(By.XPATH,'//*[@id="PhoneId"]')
            #//*[@id="select2-PhoneId-container"]

            try:
                nuevo.click()
                #escribir nuevo: 
                driver.find_element(By.XPATH,"/html/body/span/span/span[1]/input").send_keys("NUEVO")#/html/body/span/span/span[1]/input
                driver.find_element(By.XPATH,"/html/body/span/span/span[1]/input").send_keys(Keys.ENTER)
                time.sleep(1)
                #//*[@id="select2-PhoneClass-container"] TIPO
                driver.find_element('xpath','//*[@id="select2-PhoneClass-container"]').click()
                time.sleep(1)
                driver.find_element('xpath','/html/body/span/span/span[1]/input').send_keys("FIJO")#FIJO
                driver.find_element(By.XPATH,"/html/body/span/span/span[1]/input").send_keys(Keys.ENTER)
                #INDICATIVO
                driver.find_element(By.XPATH,'//*[@id="select2-Prefix-container"]').click()
                time.sleep(1)
                driver.find_element('xpath','/html/body/span/span/span[1]/input').send_keys("1")#tipo
                driver.find_element(By.XPATH,"/html/body/span/span/span[1]/input").send_keys(Keys.ENTER)
                time.sleep(1)
                accion = ActionChains(driver)
                accion.double_click(driver.find_element('xpath','//*[@id="PhoneNumber"]')).perform()
                time.sleep(1)
                driver.find_element('xpath','//*[@id="PhoneNumber"]').send_keys(1111111)#//*[@id="PhoneNumber"]
                time.sleep(1) 

            except:
                driver.find_element(By.XPATH,'//*[@id="PhoneNumber"]').click()
                lista=driver.find_element(By.XPATH,'//*[@id="PhoneNumber"]')
                # Localizar el elemento de la lista desplegable por su XPath
                # Crear un objeto Select para el elemento de la lista desplegable
                select = Select(lista)
                # Seleccionar la opción "Nuevo" por su valor
                select.select_by_visible_text("Nuevo...")

                accion = ActionChains(driver)
                accion.double_click(driver.find_element('xpath','//*[@id="PhoneNumber"]')).perform()
                time.sleep(1)
                driver.find_element('xpath','//*[@id="PhoneNumber"]').send_keys(1111111)
                time.sleep(1)
                #INFORMACION DE PORTABILIDAD

            break
        except:
            cone+=1
            continue


    #para generar error en caso de que los elementos no se hagan presentes
    if cone>=4:
        driver.find_element('xpath','//*[@id="DetailProduct_Iccid"]').click()
        print("eror al diligenciar campos")
    
    #pospago boton de seleccion
    time.sleep(2)
    while True:
        try:
            driver.find_element(By.XPATH,'//*[@id="PersonalInfo_ProductDonorOperator"]').click()
            #driver.find_element("xpath",'//*[@id="group_4"]/div[2]/div[1]/div/div/div[1]/span/span').click()
            #CONTINUAR //*[@id="PhoneNumber"]
            print("pospago seleccionado")
            break
        except:
            continue
     
    cone=0
    while cone<=4:
        try:           
            driver.find_element(By.XPATH,'//*[@id="btnNext"]').click()
            time.sleep(3)
            driver.find_element('xpath','//*[@id="select2-EquipmentPlanDataViewModel_MobileEquipment-container"]')
            break
        except:
            try:
                time.sleep(1)
                ncorreo=correo.split("@")
                driver.find_element('xpath','//*[@id="Sendbill_Email"]').click()
                driver.find_element('xpath','//*[@id="Sendbill_Email"]').clear()
                driver.find_element('xpath','//*[@id="Sendbill_Email"]').send_keys(f"{ncorreo[0]}@yahoo.com")
                accion = ActionChains(driver)
                accion.double_click(driver.find_element('xpath','//*[@id="PhoneNumber"]')).perform()
                time.sleep(1)
                driver.find_element('xpath','//*[@id="PhoneNumber"]').send_keys(1111111)
                time.sleep(1)
                buton=driver.find_element(By.XPATH,'//*[@id="PersonalInfo_ProductDonorOperator"]')
                if buton.is_selected():
                    driver.find_element('xpath','//*[@id="btnNext"]').click()
                else:
                    time.sleep(1)
                    buton.click()
                    time.sleep(1)
                    driver.find_element('xpath','//*[@id="btnNext"]').click()
                time.sleep(1)
                driver.find_element('xpath','//*[@id="select2-EquipmentPlanDataViewModel_MobileEquipment-container"]')
                break
            except:
                cone+=1

    cone=0
    while cone<=6:

        try:
            #modelo
            driver.find_element(By.XPATH,'//*[@id="select2-EquipmentPlanDataViewModel_MobileEquipment-container"]').click()
            time.sleep(2)
            driver.find_element('xpath',"/html/body/span/span/span[1]/input").send_keys("MOTOROLA")
            time.sleep(3)
            driver.find_element('xpath',"/html/body/span/span/span[1]/input").send_keys(Keys.ENTER)
            #SELECCIONAR PLAN //*[@id="select2-EquipmentPlanDataViewModel_Plan-container"]
            time.sleep(3)
            driver.find_element('xpath','//*[@id="select2-EquipmentPlanDataViewModel_Plan-container"]').click()
            time.sleep(2)
            driver.find_element('xpath',"/html/body/span/span/span[1]/input").send_keys(plan)
            time.sleep(2)
            driver.find_element('xpath',"/html/body/span/span/span[1]/input").send_keys(Keys.ENTER)
            time.sleep(5)
            #//*[@id="select2-EquipmentPlanDataViewModel_Mo 
            break
        except:
            time.sleep(1)
            cone+=1
    #para generar error en caso de que la pagina no cargue ningun elemento

    if  cone>=6:
        numlist.append(cedula)
        complemento="correo no valido"
        driver.find_element('xpath','//*[@id="DetailProduct_MinBroughtPortability"]').click()

    #SELECCIONAR CAMPAÑA DE BENEFICIOS  
    paso="no"
    cone=0
    while True:
        try:
            time.sleep(4)
            driver.find_element('xpath',selleccion).click()
            time.sleep(2)
            #CONTINUAR //*[@id="btnNext"]
            driver.find_element('xpath','//*[@id="btnNext"]').click()
            time.sleep(3)
            paso="si"
        except:
            paso="no" 
            cone+=1
        if paso=="si" or cone>=6:
            break
 
    #PASOS PARA ENVIAR EL RECHAZO A LA BASE
    cone=0
    while cone<=3:
        try:
            time.sleep(2)
            #CONTINUAR //*[@id="btnNext"]
            driver.find_element(By.XPATH,'//*[@id="btnNext"]').click()
            time.sleep(3)
            driver.find_element('xpath','//*[@id="MsgModal"]/div/button[2]').click()
            time.sleep(4)
            #activar  
            driver.find_element('xpath','//*[@id="btnNext"]').click()
            time.sleep(2)
            break
        except:
            cone+=1
    if cone>=3:
        driver.find_element(By.XPATH,'//*[@id="btnPrev"]').click()
        time.sleep(1)
        driver.find_element('xpath','//*[@id="PhoneNumber"]').click()
        complemento="error al momento de enviar el rechazo(pago minimo)"
        minimo.append(cedula)

    print(f"rechazo enviado")
    print(f"cedula: {cedula}")
    complemento="rechazo enviado"
    reglist.append(cedula)
    #pasos finales 
    time.sleep(6)
    modal = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "MsgModal"))
    )
    button = modal.find_element(By.XPATH,'//*[@id="MsgModal"]/div/button[2]')
    button.click()
    driver.switch_to.default_content()
    #driver.find_element('xpath','//*[@id="btnPrev"]').click() //*[@id="btnPrev"]
    cone=0
    while cone<=3:
        try:
            driver.find_element(By.XPATH,'//*[@id="btnPrev"]').click()
            break
        except:
            cone+=1
    if cone>=3:
        
        driver.find_element(By.XPATH,'//*[@id="btnPrev"]').click()
    
    
    


    





#FUNCION PARA INGRESAR A POLIEDRO, CON USUARIO, CONTRASEÑA Y TOKEN
#ESTA FUNCION SOLO SE VA A LLAMAR UNA VEZ EN LA EJECUCION
def ingreso():
    #ABRIR POLIEDRO
    driver.get('https://poliedro.comcel.com.co/LoginPoliedro/Login.aspx')

    #ESPERAR A QUE CARGUE LA PAGINA WEB
    time.sleep(2)
    #IR A INICIO POLIEDRO
    driver.find_element('xpath','//*[@id="ctl00_ContentPlaceHolder1_BtnRegresarMensaje"]').click()
    #ESPERAR A QUE CARGUE LA PAGINA WEB202
def activacion_pospago():

    time.sleep(4)
    #OPCIONES DE ACTIVACION
    driver.find_element('xpath',"/html/body/table/tbody/tr[5]/td/table/tbody/tr/td[1]/div[1]/div[1]/div[5]").click()
    #ESPERAR A QUE CARGUE POLIEDRO
    time.sleep(2)
    #ACTIVACION CONTRATO FISICO
    driver.find_element('xpath',"/html/body/table/tbody/tr[5]/td/table/tbody/tr/td[1]/div[1]/div[1]/div[6]/div[2]/a").click()
    #ESPERAR A QUE CARGUE POLIEDRO
    time.sleep(2)

#ESTA FUNCION PREPARA EL ENTORNO PARA COMENZAR CON EL DILIGENCIAMIENTO DE LOS FORMULARIOS 
def inicio():
   #ACTIVACION UNICA
    driver.find_element('xpath','//*[@id="containerNavBar"]/ul/li[1]/a/span').click()

    #ESPERAR A QUE CARGUE POLIEDRO
    time.sleep(2)

    #ACTIVACION POSTPAGO
    driver.find_element('xpath','//*[@id="containerNavBar"]/ul/li[1]/ul/li[2]/a/span').click()

    #ESPERAR A QUE CARGUE POLIEDRO
    time.sleep(2)

    
    #ESPERAR A QUE CARGUE POLIEDRO
    time.sleep(1)

    #LLAMAR PORTABILIDAD O MIGRACION  
    driver.find_element('xpath','//*[@id="select2-productShortcut-container"]').click()
    time.sleep(1)
    driver.find_element('xpath','/html/body/span/span/span[1]/input').click()
    time.sleep(2)
    driver.find_element('xpath',"/html/body/span/span/span[1]/input").send_keys(208)
    time.sleep(1)
    driver.find_element('xpath',"/html/body/span/span/span[1]/input").send_keys(Keys.ENTER)
    time.sleep(5)

##ESTAS LINEAS DE CODIGO RECIBEN LOS DATOS DE LA FECHA A PORTAR Y LA CEDULA, YA QUE 
#LA CEDULA DEL ASESOR QUE SE CARGA A LA BASE NO SIEMPRE ES APTA PARA DILIGENCIAR LOS FORMULARIOS

print("definamos una fecha a portar para todas las iteraciones")
diap=input("digite dia: ")
mesp=input("digite mes: ")
año=input("digite año: ")
print("desea usar la cedula de la base o una generica?")

cedul=input("digite cedula generica de asesor: ")
print("digite s si desea usar la cedula generica, cualquier otro caracter si usara la base")
opc=input("digite opcion: ")
dia=str(diap).rjust(2,"0")
mes=str(mesp).rjust(2,"0")
fechap=(f"{dia}/{mes}/{año}")

####   AQUI INICIA EL PROCESO   ####
driver = webdriver.Edge('msedgedriver.edge')
df = pd.read_csv('BASEP.csv', encoding = 'latin-1')
df.replace('nan', np.nan, inplace=True)
df
ingreso()
paso="no"
print("ya ingresaste a la pagina?")
print("digite si de ser correcto: ")
paso=input()
if paso.upper()!="NO":
    print("ejecutando poliedro")
activacion_pospago()
contador=0
iterador=1
nipn=0
with open('BASEP2.csv', 'w', encoding='utf-8', newline='') as archivo:
    writer = csv.writer(archivo)
    for row, datos in df.iterrows():
        print(f"iteracion: {iterador}")
        iterador+=1
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
        if convergencia=="SI" and operador=="WOM":
            sellecion=dicplan['WOM']
        elif convergencia=="NO" and operador=="WOM":
            selleccion=dicplan['WOMNO'] 
        elif convergencia=="SI" and operador=="MOVISTAR":
            selleccion=dicplan['MOVISTAR']
        elif convergencia=="NO" and operador=="MOVISTAR":
            selleccion=dicplan['MOVISTARNO']
        elif convergencia=="SI" and operador=="TIGO":
            selleccion=dicplan['TIGO']
        elif convergencia=="NO" and operador=="TIGO":
            selleccion=dicplan['TIGONO']
        elif convergencia=="NO" and operador=="ETB":
            selleccion=dicplan["ETBNO"]
        elif convergencia=="SI" and operador=="ETB":
            selleccion=dicplan["ETB"] 
        elif convergencia=="NO" and operador=="AVANTEL":
            selleccion=dicplan["AVANTELNO"]   
        elif convergencia=="SI" and operador=="AVANTEL":
            selleccion=dicplan["AVANTEL"]
        else:
            sellecion='/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div/div/div/div[2]/div[2]/fieldset/div[1]/span/span/input'
        cedulaa=str(cedul)
        cedula=str(cc)
        plan=str(planb)

        
        cedulaa=str(cedul)
        
        #ciclo
        #EL CICLO SE REPITE EN CASO DE ERROR POR SI LOS ELEMENTOS DE LA PAGINA NO CARGAN Y SE GENERA ALGUN ERROR
        #  PARA NO PASAR POR ALTO EL REGISTRO
        try:
            inicio()
            time.sleep(1)
            formularios(cedula,apellido,cedulaa,celular,nip,fechap,serialsim,errorlist,simlist,complemento)
            validaciones(doclist, niplist, operlist,complemento)
            forms2(correo,plan,reglist,selleccion,numlist,minimo,complemento)
            contador=contador+1
        except:
            try:
                inicio()
                time.sleep(1)
                formularios(cedula,apellido,cedulaa,celular,nip,fechap,serialsim,errorlist,simlist,complemento)
                validaciones(doclist, niplist, operlist,complemento)
                forms2(correo,plan,reglist,selleccion,numlist,minimo,complemento)
                contador=contador+1
            except:
                continue
        finally:
            time.sleep(1)
            print("one contact")

        writer.writerow([cedula, complemento])

        continue



     


driver.close()
print("iteraciones realizadas ",contador)
print("registros realizados: ")
print(reglist)
print("errores encontrados:")
print(errorlist)
print("los siguientes rechazos no pudieron ser enviados debido al documento: ")
print(doclist)
print("estos rechazos no pasaron por sim adquirida")
print(simlist)
print("los siguientes rechazos no se enviaron debido a que se necesita cambiar el numero a portar")
print(numlist)
print("los siguientes rechazos no pudieron ser enviados debido a que el min se encuentra en otro proceso ")
print(niplist)
print("los siguientes rechazos no pasaron por pago minimo")
print(minimo)

