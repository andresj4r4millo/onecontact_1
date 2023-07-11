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

model_e="MOTOROLA"
cone=0





def formularios(cedulag,cedula,apellido,cedulaa,celular,nip,fechap,serialsim):

    paso="no"
    #primeros pasos, primer formulario
    #while con el fin de no lanzar error si el script no encuentra los elementos en la pagina
    cone=0
    while cone<6:

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
        return "pagina no cargo"

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
        paso="si"
    except:
        #SI LA CONSULTA NO SE REALIZA EL SIGUIENTE BUCLE DIGITA NUEVAMENTE LA CEDULA DEL ASESOR, LA FECHA Y REALIZA LA CONSULTA HASTA QUE SE REDIRIGA AL SISGUIENTE FORM
        cone=0
        while cone<8:
            #comenzar a usar cedula generica
            if cone>4:
                cedulaa=cedulag
            try:
                accion = ActionChains(driver)
                accion.double_click(driver.find_element('xpath','//*[@id="DetailProduct_SellerId"]')).perform()
                time.sleep(1)
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
                    print("sim adquirida")
                    complement="sim adquirida"
                    cone=8
                    break  
                except:

                    driver.find_element('xpath','//*[@id="btnNext"]').click()
                    ##FORMULARIO 2    
                    #para confirmar que la pagina se redirecciona
                    time.sleep(4)
                    driver.find_element('xpath','/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div[2]/div[11]/div/div[2]/div[2]/div').click()
                    paso="si"
                    cone=0
                    break
            except: 
                if cone==8:
                    break
                elif paso=="si":
                    break
                else:
                    cone+=1
                    continue
                

    #ESTAS LINEAS DE CODIGO GENERARAN ERROR SI LA PAGINA NO REALIZA LA CONSULTA DESPUES DE 6 INTENTOS

    if cone>=8:
        return "consulta no realizada"
    elif complement=="sim adquirida":
        return "sim adquirida"
    elif paso=="si":
        print("en espera por validacion")
        return ""

    

    
#ESTA FUNCION EVALUARA SI EL RECHAZO PASA O NO, Y EL PORQUE, PARA SEGMENTARLO POR LISTAS
def validaciones(): 

    cone=0
    while cone<4:
        try:
            print("buscando el boton para continuar ")
            #driver.find_element(By.XPATH, '//*[@id="btnNext"]').click()
            #time.sleep(2) 
            #driver.find_element(By.XPATH, '//*[@id="ActivationClass_CfmToFirstInvoice"]')
            time.sleep(2)
            driver.find_element(By.XPATH,'//*[@id="btnNext"]').click()
            time.sleep(2) 
            driver.find_element(By.XPATH,'//*[@id="ActivationClass_CfmToFirstInvoice"]')
            break
        except:
            #regresar
            cone+=1
            continue 
    if cone>=4:   
        try:
            porta = driver.find_element(By.XPATH, '//*[@id="viewErrors"]/ul/li[2]')
            validacion=porta.text
        except:
            #//*[@id="validationResponses"]/div[5]/div[2]/div[11]/div/div[2]/div[1]
            validaciones=driver.find_element(By.XPATH, '//*[@id="viewErrors"]/ul/li[2]')
            validacion=validaciones.text   
        return  str(validacion)
    else:
        return ""


####FORMULARIO 3#####
#APARTIR DE AQUI SE DEFINE SI EL RECHAZO PASA O NO, HAY VARIAS ESTRUCTURAS PARA QUE LOS CAMPOS SEAN DILIGENCIADOS O LLENADOS
#CON EL FIN DE EVITAR QUE ALGUN CMPO QUEDE SIN SER SELECCIONADO ESTAN EN ESTRUCTURAS CICLICAS POR PASOS.



def forms2(correo,plan,selleccion):

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
            time.sleep(2)
            #CLASES DE ACTIVACION //*[@id="ActivationClass_CfmToFirstInvoice"]
            
            #CORREO DEL CLIENTE //*[@id="PersonalInfo_Email"]
            driver.find_element('xpath','//*[@id="PersonalInfo_Email"]').clear()
            driver.find_element('xpath','//*[@id="PersonalInfo_Email"]').send_keys(correo)
            time.sleep(1)
            #NUMERO DE TELEFONO 
            break
        except:
            cone+=1
    #para generar error en caso de que los elementos no se hagan presentes
    if cone>=4:
        return "elementos no ubicados"


    cone=0
    while cone<=4:

        nuevo=driver.find_element(By.XPATH,'//*[@id="select2-PhoneId-container"]')

        #//*[@id="select2-PhoneId-container"]
        try:
            try:
                div=driver.find_element(By.ID,"group_4")
                driver.find_element(By.ID,"PhoneId").click()
                lista=driver.find_element(By.ID,"PhoneId")
                # Localizar el elemento de la lista desplegable por su XPath
                # Crear un objeto Select para el elemento de la lista desplegable
                select = Select(lista)
                # Seleccionar la opción "Nuevo" por su valor
                select.select_by_visible_text("Nuevo...")
                div.click()
                #//*[@id="PhoneClass"]
                time.sleep(1)
                driver.find_element(By.ID,"PhoneClass").click()
                lista=driver.find_element(By.ID,"PhoneClass")
                #fijo
                select= Select(lista)
                # Seleccionar la opción "Nuevo" por su valor
                time.sleep(1)
                select.select_by_visible_text("Fijo")
                div.click()
                #1
                driver.find_element(By.ID,"Prefix").click()
                lista=driver.find_element(By.ID,"Prefix")
                
                #fijo
                time.sleep(1)
                select = Select(lista)
                # Seleccionar la opción "Nuevo" por su valor
                select.select_by_visible_text("1")

                accion = ActionChains(driver)
                accion.double_click(driver.find_element(By.ID,"PhoneNumber")).perform()
                time.sleep(1)
                driver.find_element(By.ID,"PhoneNumber").send_keys(1111111)
                time.sleep(1)
                #INFORMACION DE PORTABILIDAD
                break
            except:
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
                break
        except:
            try:
                #PENDIENTE DE VER SU EJECUCION 
                div=driver.find_element(By.ID,"group_4")
                driver.find_element(By.ID,"PhoneNumber").click()
                lista=driver.find_element(By.ID,"PhoneNumber")
                # Localizar el elemento de la lista desplegable por su XPath
                # Crear un objeto Select para el elemento de la lista desplegable
                select = Select(lista)
                # Seleccionar la opción "Nuevo" por su valor
                select.select_by_visible_text("Nuevo...")
                div.click()
                #//*[@id="PhoneClass"]
                time.sleep(1)
                driver.find_element(By.ID,"PhoneClass").click()
                lista=driver.find_element(By.ID,"PhoneClass")
                #fijo
                select= Select(lista)
                # Seleccionar la opción "Nuevo" por su valor
                time.sleep(1)
                select.select_by_visible_text("Fijo")
                div.click()
                #1
                driver.find_element(By.ID,"Prefix").click()
                lista=driver.find_element(By.ID,"Prefix")
                
                #fijo
                time.sleep(1)
                select = Select(lista)
                # Seleccionar la opción "Nuevo" por su valor
                select.select_by_visible_text("1")

                accion = ActionChains(driver)
                accion.double_click(driver.find_element(By.ID,"PhoneNumber")).perform()
                time.sleep(1)
                driver.find_element(By.ID,"PhoneNumber").send_keys(1111111)
                time.sleep(1)
                #INFORMACION DE PORTABILIDAD

                break
            except:
                cone+=1
    #para generar error en caso de que los elementos no se hagan presentes
    if cone>=4:
        return "error lista desplegable"

    
    #pospago boton de seleccion
    seleccionado=""
    time.sleep(2)
    while True:
        try:
            driver.find_element(By.XPATH,'//*[@id="PersonalInfo_ProductDonorOperator"]').click()
            #driver.find_element("xpath",'//*[@id="group_4"]/div[2]/div[1]/div/div/div[1]/span/span').click()
            #CONTINUAR //*[@id="PhoneNumber"]
            print("pospago seleccionado")
            seleccionado="si"
            break
        except:  
            continue
    if seleccionado!="si":
        cone=0
        while cone<=4:
            try:
                driver.find_element(By.XPATH,'//*[@id="PersonalInfo_ProductDonorOperator"]').click()
                #driver.find_element("xpath",'//*[@id="group_4"]/div[2]/div[1]/div/div/div[1]/span/span').click()
                #CONTINUAR //*[@id="PhoneNumber"]
                seleccionado="si"
                break
            except:
                seleccionado="no"
                continue
     
    cone=0
    while cone<=4:
        try:           
            driver.find_element(By.XPATH,'//*[@id="btnNext"]').click()
            time.sleep(2)
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
                ######
                if seleccionado!="si":
                    driver.find_element(By.XPATH,'//*[@id="PersonalInfo_ProductDonorOperator"]').click()
                ######
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

    if  cone>=4:
        return "correo no valido"
        

    cone=0
    while cone<=6:

        try:
            #modelo
            driver.find_element(By.XPATH,'//*[@id="select2-EquipmentPlanDataViewModel_MobileEquipment-container"]').click()
            time.sleep(2)
            driver.find_element('xpath',"/html/body/span/span/span[1]/input").send_keys("MOTOROLA")
            time.sleep(2)
            driver.find_element('xpath',"/html/body/span/span/span[1]/input").send_keys(Keys.ENTER)
            #SELECCIONAR PLAN //*[@id="select2-EquipmentPlanDataViewModel_Plan-container"]
            time.sleep(2)
            driver.find_element('xpath','//*[@id="select2-EquipmentPlanDataViewModel_Plan-container"]').click()
            time.sleep(2)
            driver.find_element('xpath',"/html/body/span/span/span[1]/input").send_keys(plan)
            time.sleep(2)
            driver.find_element('xpath',"/html/body/span/span/span[1]/input").send_keys(Keys.ENTER)
            time.sleep(2)
            #//*[@id="select2-EquipmentPlanDataViewModel_Mo 
            break
        except:
            time.sleep(1)
            cone+=1
    #para generar error en caso de que la pagina no cargue ningun elemento

    if  cone>=6:
        return "correo no valido"


    #SELECCIONAR CAMPAÑA DE BENEFICIOS  
    paso="no"
    cone=0
    while True:
        try:
            time.sleep(2)
            driver.find_element('xpath',selleccion).click()
            time.sleep(2)
            #CONTINUAR //*[@id="btnNext"]
            driver.find_element('xpath','//*[@id="btnNext"]').click()
            time.sleep(2)
            paso="si"
        except:
            try:
                driver.find_element(By.XPATH,'//*[@id="CampaignsViewModel_SelectedCampaigns"]').click()
            except:
                paso="no" 
                cone+=1
        if paso=="si" or cone>=8:

            break
 
    #PASOS PARA ENVIAR EL RECHAZO A LA BASE
    cone=0
    while cone<=3:
        try:
            time.sleep(2)
            #CONTINUAR //*[@id="btnNext"]
            driver.find_element(By.XPATH,'//*[@id="btnNext"]').click()
            time.sleep(2)
            driver.find_element('xpath','//*[@id="MsgModal"]/div/button[2]').click()
            time.sleep(2)
            #activar  
            driver.find_element('xpath','//*[@id="btnNext"]').click()
            time.sleep(2)
            complemento="rechazo enviado"
            break
        except:
            cone+=1
    if cone>=3:
        driver.find_element(By.XPATH,'//*[@id="btnPrev"]').click()
        time.sleep(1)
        driver.find_element('xpath','//*[@id="PhoneNumber"]').click()
        return"error al momento de enviar el rechazo(pago minimo)"
    else:
        complemento="rechazo enviado"
    print(f"rechazo enviado")
    print(f"cedula: {cedula}")
    complemento="rechazo enviado"
    print("complemento")
    acept="no"    
    cone=0
    time.sleep(3)
    modal = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "MsgModal"))
    )
    button = modal.find_element(By.XPATH,'//*[@id="MsgModal"]/div/button[2]')#//*[@id="MsgModal"]/div/button[2]
    time.sleep(1)
    button.click()

    while cone<=4:
        try:
            modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "MsgModal"))
            )
            button = modal.find_element(By.XPATH,'//*[@id="MsgModal"]/div/button[2]')#//*[@id="MsgModal"]/div/button[2]
            time.sleep(1)
            button.click()

            #pasos finales 
            button.click()
            #driver.find_element('xpath','//*[@id="btnPrev"]').click() //*[@id="btnPrev"]
            acept="si"
            break
        except:
            cone+=1
    
    while acept !="si":
        try:
            modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "MsgModal"))
            )
            button = modal.find_element(By.XPATH,'//*[@id="MsgModal"]/div/button[2]')#//*[@id="MsgModal"]/div/button[2]
            time.sleep(1)
            button.click()
            modal.find_element(By.XPATH,'//*[@id="MsgModal"]/div/button[2]').click()
            acept="si"
            cone=0
            break
        except:
            cone+=1
            if cone>=8: 
                break
            continue

    if acept=="si":
        driver.switch_to.default_content()
        #return "enviado"
    while True:
        try:
            if cone>=4:  
                driver.find_element(By.XPATH,'//*[@id="btnPrev"]').click()
                return "enviado"
            else:
                driver.find_element(By.XPATH,'//*[@id="btnPrev"]').click()
                return "enviado"
        except:
            return "enviado"
    #lineas de codigo para generar un regreso en la pagina en caso de intermitencias
    

    
    
    


    





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
    con=0
    while con<4:
        try:
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
            break
        except:
            con+=1
        if con==4:
            return "pagina no carga"
        else:
            return ""

##ESTAS LINEAS DE CODIGO RECIBEN LOS DATOS DE LA FECHA A PORTAR Y LA CEDULA, YA QUE 
#LA CEDULA DEL ASESOR QUE SE CARGA A LA BASE NO SIEMPRE ES APTA PARA DILIGENCIAR LOS FORMULARIOS

print("definamos una fecha a portar para todas las iteraciones")
diap=input("digite dia: ")
mesp=input("digite mes: ")
año=input("digite año: ")


cedulag=input("digite cedula generica de asesor: ")
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
        mi_plan=int(tu_plan_deseado)
        #seleccion
        #ciclo
        print(f"{operador}, {mi_plan}, {convergencia}")
        data_frame = pd.read_excel('CAMPAÑASB.xlsx', sheet_name='Hoja1')

        # Filtra el DataFrame para obtener la fila deseada
        fila_deseada = data_frame.loc[(data_frame['PLAN'] == mi_plan) & (data_frame['OPERADOR'] == operador)]

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
        complemento=""


        inicio()
        time.sleep(1)
        complemento=formularios(cedulag,cedula,apellido,cedulaa,celular,nip,fechap,serialsim)
        if complemento == "":
            complemento=validaciones()
            if complemento =="":
                complemento=forms2(correo,plan,seleccion)
        if complemento=="error lista desplegable":
            inicio()
            complemento=formularios(cedulag,cedula,apellido,cedulaa,celular,nip,fechap,serialsim)
            if complemento == "":
                complemento=validaciones()
                if complemento =="":
                    complemento=forms2(correo,plan,seleccion)

        #escribir en el libro
        datosfila=(f"{cedula}:  {complemento}")
        print(datosfila)
        archivo.write(datosfila + '\n')
        archivo.flush()
        print("onecontact")
        continue
    
           



driver.close()


