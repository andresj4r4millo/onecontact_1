#DRIVERS
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
import requests
import pandas as pd
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

model_e="MOTOROLA"
reglist=[]
cone=0
errorlist=[]
doclist=[]

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



def formularios(cedula,apellido,cedulaa,celular,nip,fechap,serialsim,correo,plan,selleccion,reglist,errorlist,cone,cedul, doclist):
    campo_fecha=driver.find_element(By.ID,'DetailProduct_PortabilityDate')
    #primeros pasos, primer formulario
    #while con el fin de no lanzar error si el script no encuentra los elementos en la pagina
    while True:
        try:
            #FORMULARIO 1
            #LLENAR CEDULA //*[@id="DetailProduct_DocumentNumber"]
            time.sleep(2)
            driver.find_element('xpath','//*[@id="DetailProduct_DocumentNumber"]').send_keys(cedula)
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
            driver.find_element('xpath','//*[@id="DetailProduct_NIP"]').send_keys(nip)
            #FECHA DE PORTACION
            #driver.find_element('xpath','//*[@id="DetailProduct_PortabilityDate"]').clear()
            #driver.find_element('xpath','//*[@id="DetailProduct_PortabilityDate"]').send_keys(fechap)
            campo_fecha.clear()
            driver.execute_script(f'document.getElementById("DetailProduct_PortabilityDate").value = "{fechap}";')
            #SERIAL SIM CARD
            accion = ActionChains(driver)
            # /html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[2]/div[2]/div/input
            accion.double_click(driver.find_element('xpath',"/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[2]/div[2]/div/input")).perform()
            driver.find_element('xpath',"/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[2]/div[2]/div/input").send_keys(serialsim)
            
            break
        except:
            continue
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
        while cone<6:
            try:
                accion = ActionChains(driver)
                accion.double_click(driver.find_element('xpath','//*[@id="DetailProduct_SellerId"]')).perform()
                driver.find_element('xpath','//*[@id="DetailProduct_SellerId"]').send_keys(cedulaa)
                time.sleep(1)
                #driver.find_element('xpath','//*[@id="DetailProduct_PortabilityDate"]').clear()
                #driver.find_element('xpath','//*[@id="DetailProduct_PortabilityDate"]').send_keys(fechap)
                campo_fecha.clear()
                driver.execute_script(f'document.getElementById("DetailProduct_PortabilityDate").value = "{fechap}";')
                #driver.find_element('xpath','//*[@id="DetailProduct_PortabilityDate"]').send_keys(Keys.ENTER)
                #time.sleep(1)
                driver.find_element('xpath','//*[@id="btnNext"]').click()
                ##FORMULARIO 2    
                time.sleep(3)
                driver.find_element('xpath','/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div[2]/div[11]/div/div[2]/div[2]/div').click()
                break
            except:
                cone+=1
                if cone>=5:
                    errorlist.append(cedula)
                    break
    #ESTAS LINEAS DE CODIGO GENERARAN ERROR SI LA PAGINA NO REALIZA LA CONSULTA DESPUES DE 6 INTENTOS
    if cone>=6:
        driver.find_element('xpath','//*[@id="DetailProduct_MinBroughtPortability"]').click()


    ##FORMULARIO 2    
    #time.sleep(3)
    #LA SIGUIENTE ESTRUCTURA
    #1. EVALUA SI LA PORTABILIDAD NUMERICA ES FALSA
    #2. DE LO CONTRARIO DARA CLICK EN EL BOTON DE CONTINUAR HASTA QUE SE REDIRECCIONE, 
    # SI EL PUNTO 2 ES EXITOSO ES PORQUE EL RECHAZO PUEDE SER ENVIADO, DE LO CONTRARIO
    #3. AL NO REDIRIGIRSE DESPUES DE 6 INTENTOS LA CEDULA DEL CLIENTE SE AGREGARA EN LA LISTA DE ERRORES, SALDRA DE LA ESTRUCTURA
    # AL SALIR DE LA ESTRUCTURA SI NO SE REDIRECCIONA LA PAGINA GENERARA ERROR PARA CONTINUAR CON EL SIGUIENTE RECHAZO
    num=0
    while num<6:
        try:
            try:
                #//*[@id="viewErrors"]/ul/li[2]
                wait = WebDriverWait(driver, 10)
                #porta = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="viewErrors"]/ul/li[2]')))
                #porta=driver.find_element('xpath','//*[@id="viewErrors"]/ul/li[2]')
                div_element = wait.until(EC.visibility_of_element_located((By.ID, 'viewErrors')))

                # Obtener el elemento de texto dentro del div
                li_element = div_element.find_element(By.XPATH, './ul/li[2]')
                text = li_element.text
                if 'Solicitud Portabilidad Numerica = Falso' in text:
                    driver.find_element("xpath",'//*[@id="btnPrev"]').click()
                    time.sleep(1)
                    conp=0
                    #perform(conp)
                    while conp<6:
                        try:
                            acction = ActionChains(driver)
                            acction.double_click(driver.find_element(By.XPATH, '//*[@id="DetailProduct_SellerId"]')).perform()
                            time.sleep(1)
                            driver.find_element(By.XPATH, '//*[@id="DetailProduct_SellerId"]').send_keys(cedulaa)
                            time.sleep(1)
                            campo_fecha.clear()
                            #javascript para definir valor en el input de la fecha, ya que al enviar valores este desaparece
                            driver.execute_script(f'document.getElementById("DetailProduct_PortabilityDate").value = "{fechap}";')
                            time.sleep(2)
                            driver.find_element(By.XPATH,'//*[@id="btnNext"]').click()
                            time.sleep(3)
                            driver.find_element('xpath','/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div[2]/div[11]/div/div[2]/div[2]/div').click()
                            break
                        except:
                            conp+=1
                            continue
                    print("porta falso")
                else:
                    #codigo el 
                    errorlist.append(cedula)
                    conp=6
                    break
                num+=1
            except NoSuchElementException:
                cone=0
                while cone<5:
                    try:
                        #driver.find_element(By.XPATH, '//*[@id="btnNext"]').click()
                        #time.sleep(2) 
                        #driver.find_element(By.XPATH, '//*[@id="ActivationClass_CfmToFirstInvoice"]')
                        time.sleep(2)
                        driver.find_element('xpath','//*[@id="btnNext"]').click()
                        time.sleep(2) 
                        driver.find_element('xpath','//*[@id="ActivationClass_CfmToFirstInvoice"]')
                        break
                    except:
                        #regresar
                        cone+=1
                num=6
                break            
            except Exception as e:
                cone=0
                while cone<5:
                    try:
                        #driver.find_element(By.XPATH, '//*[@id="btnNext"]').click()
                        #time.sleep(2) 
                        #driver.find_element(By.XPATH, '//*[@id="ActivationClass_CfmToFirstInvoice"]')
                        time.sleep(2)
                        driver.find_element('xpath','//*[@id="btnNext"]').click()
                        time.sleep(2) 
                        driver.find_element('xpath','//*[@id="ActivationClass_CfmToFirstInvoice"]')
                        break
                    except:
                        #regresar
                        cone+=1
                num=6
                break    
            num+=1
        except:
            num+=1

    if cone>=5:
        try:
            ##las siguientes lineas de codigo evaluan si el rechazo no pasa por el documento
            element = driver.find_element(By.XPATH,'//*[@id="validationResponses"]/div[6]/div[2]/div[3]/div/div/div')
            document= element.text
            if 'DOCUMENTO NO APLICA PARA ACTIVACIÓN POLIEDRO' in document:
                doclist.append(cedula)
                print("documento no aplica")
        except:
            print("documento aplica")

    if cone>=5 or conp>=6 or num>=5:
        errorlist.append(cedula)  
        driver.find_element('xpath','//*[@id="DetailProduct_MinBroughtPortability"]').click()  
        #para generar error
        driver.find_element('xpath','//*[@id="ActivationClass_LinkPreactivation"]').click()

    ####FORMULARIO 3#####
    #APARTIR DE AQUI SE DEFINE SI EL RECHAZO PASA O NO, HAY VARIAS ESTRUCTURAS PARA QUE LOS CAMPOS SEAN DILIGENCIADOS O LLENADOS
    #CON EL FIN DE EVITAR QUE ALGUN CMPO QUEDE SIN SER SELECCIONADO ESTAN EN ESTRUCTURAS CICLICAS POR PASOS.
    cone=0
    while cone<=4:
        try:
            time.sleep(3)
            #CLASES DE ACTIVACION 
            driver.find_element('xpath','//*[@id="ActivationClass_CfmToFirstInvoice"]').click()
            driver.find_element('xpath','//*[@id="ActivationClass_LinkPreactivation"]').click()
            #CORREO DEL CLIENTE //*[@id="PersonalInfo_Email"]
            driver.find_element('xpath','//*[@id="PersonalInfo_Email"]').clear()
            driver.find_element('xpath','//*[@id="PersonalInfo_Email"]').send_keys(correo)
            time.sleep(1)
            #NUMERO DE TELEFONO 
            driver.find_element('xpath','//*[@id="select2-PhoneId-container"]').click()
            time.sleep(1)
            driver.find_element('xpath',"/html/body/span/span/span[2]/ul/li[1]").click()
            time.sleep(2)
            driver.find_element('xpath','//*[@id="select2-PhoneClass-container"]').click()
            time.sleep(2)
            driver.find_element('xpath',"/html/body/span/span/span[2]/ul/li[2]").click()
            time.sleep(2)
            driver.find_element('xpath','//*[@id="select2-Prefix-container"]').click()
            time.sleep(2)
            driver.find_element('xpath',"/html/body/span/span/span[2]/ul/li[2]").click()
            time.sleep(1)
            accion = ActionChains(driver)
            accion.double_click(driver.find_element('xpath','//*[@id="PhoneNumber"]')).perform()
            time.sleep(1)
            driver.find_element('xpath','//*[@id="PhoneNumber"]').send_keys(1111111)
            time.sleep(1)
            #INFORMACION DE PORTABILIDAD
            break
        except:
            cone+=1
    #para generar error en caso de que los elementos no se hagan presentes
    if cone>=4:
        driver.find_element('xpath','//*[@id="DetailProduct_MinBroughtPortability"]').click()
    cone=0
    #pospago boton de seleccion
    time.sleep(2)
    while True:
        try:
            driver.find_element('xpath','//*[@id="PersonalInfo_ProductDonorOperator"]').click()
            #driver.find_element("xpath",'//*[@id="group_4"]/div[2]/div[1]/div/div/div[1]/span/span').click()
            #CONTINUAR 
            print("pospago seleccionado")
            break
        except:
            continue

    buton=driver.find_element(By.ID,'PersonalInfo_ProductDonorOperator')       
    cone=0
    while cone<=4:
        try:           
            driver.find_element('xpath','//*[@id="btnNext"]').click()
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
                time.sleep(1)
                if buton.is_selected():
                    driver.find_element('xpath','//*[@id="btnNext"]').click()
                else:
                    time.sleep(1)
                    driver.find_element('xpath','//*[@id="PersonalInfo_ProductDonorOperator"]').click()
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
            driver.find_element('xpath','//*[@id="select2-EquipmentPlanDataViewModel_MobileEquipment-container"]').click()
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
        driver.find_element('xpath','//*[@id="DetailProduct_MinBroughtPortability"]').click()

    #SELECCIONAR CAMPAÑA DE BENEFICIOS  
    paso="no"
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
        if paso=="si":
            break
 
    #PASOS PARA ENVIAR EL RECHAZO A LA BASE
    cone=0
    while True:
        try:
            time.sleep(2)
            #CONTINUAR //*[@id="btnNext"]
            driver.find_element('xpath','//*[@id="btnNext"]').click()
            time.sleep(3)
            driver.find_element('xpath','//*[@id="MsgModal"]/div/button[2]').click()
            time.sleep(4)
            #activar  
            driver.find_element('xpath','//*[@id="btnNext"]').click()
            time.sleep(4)
            #reglist.append(cedula)
            #pasos finales 
            driver.find_element('xpath','//*[@id="MsgModal"]/div/button[2]').click()
            driver.find_element('xpath','//*[@id="btnPrev"]').click()
            #driver.find_element('xpath','//*[@id="containerNavBar"]/ul/li[9]/a').click()
            reglist.append(cedula)
            break
        except:
            cone+=1
        if cone>=3:
            time.sleep(1)
            break
    time.sleep(1)
    





#FUNCION PARA INGRESAR A POLIEDRO, CON USUARIO, CONTRASEÑA Y TOKEN
#ESTA FUNCION SOLO SE VA A LLAMAR UNA VEZ EN LA EJECUCION
def ingreso():
    #ABRIR POLIEDRO
    driver.get('https://poliedro.comcel.com.co/LoginPoliedro/Login.aspx')

    #ESPERAR A QUE CARGUE LA PAGINA WEB
    time.sleep(2)
    #IR A INICIO POLIEDRO
    driver.find_element('xpath','//*[@id="ctl00_ContentPlaceHolder1_BtnRegresarMensaje"]').click()
    #ESPERAR A QUE CARGUE LA PAGINA WEB
    time.sleep(20)
    #INGRESAR A POLIEDRO
    driver.find_element('xpath','//*[@id="btnIngresarUsuarioContraseña"]').click()
    #ESPERAR A QUE SE INGRESE TOKEN
    time.sleep(22)
    #INGRESAR TOKEN
    driver.find_element('xpath','//*[@id="ctl00_ContentPlaceHolder1_BtnLoginTokenEntrust"]').click()
    time.sleep(2)
    #ESPERAR A QUE CARGUE POLIEDRO
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
df
ingreso()
contador=0
iterador=1
for row, datos in df.iterrows():
    print(f"iteracion: {iterador}")
    iterador+=1
    cc=datos["CEDULA"]
    apellido=datos["APELLIDO"]
    cedulaaa=datos["CEDULAASESOR"]
    ##celular
    celular=datos["MIN_AP"]
    nipn=datos["NIP"]
    fecha=datos["FECHA_P"]
    serialsim=datos["SERIAL_SIM"]
    ##celular: no usar, valor ==0
    minpre=datos["MIN_PRE"]
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
    plan=int(planb)

    if opc.upper()=="S":
        cedulaa=str(cedul)
    else:
        cedulaa=str(cedulaaa)
    #ciclo
    #EL CICLO SE REPITE EN CASO DE ERROR POR SI LOS ELEMENTOS DE LA PAGINA NO CARGAN Y SE GENERA ALGUN ERROR
    #  PARA NO PASAR POR ALTO EL REGISTRO
    try:
        inicio()
        time.sleep(1)
        formularios(cedula,apellido,cedulaa,celular,nip,fechap,serialsim,correo,plan,selleccion,reglist,errorlist,cone,cedul,doclist)
        contador=contador+1
    except:
        try:
            inicio()
            time.sleep(1)
            formularios(cedula,apellido,cedulaa,celular,nip,fechap,serialsim,correo,plan,sellecion,reglist,errorlist,cone,cedul,doclist)
            contador=contador+1
        except Exception as e:
            print(f"error al llenar el formulario {e}")
            errorlist.append(cedula)
    finally:
        time.sleep(1)
        print("one contact")

     


driver.close()
print("iteraciones realizadas ",contador)
print("registros realizados: ")
print(reglist)
print("errores encontrados:")
print(errorlist)
print("los siguientes rechazos no pudieron ser enviados debido al documento: ")
print(doclist)
print(" ONE CONTACT COLOMBIA ")
