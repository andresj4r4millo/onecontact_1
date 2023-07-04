import re
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

planes={
        27744:37900,
        27745:37900,
        27746:47900,
        27747:47900,
        27750:49900,
        27751:49900,
        27788:33900,
        27787:33900,
        27965:45900,
        27966:45900,
        28627:42900,
        28628:42900,
        28689:33000,
        28690:33000,
        28691:37900,
        28692:37900,
        28693:42900,
        28694:42900,

    }

convergencia="SI"
operador="ETB"
PLAN="27787 Fideliza L PRO Mx 23"
match = re.search(r'\d{5}', PLAN)

if match:
    numeros = match.group()
    print("Los primeros cinco números son:", numeros)
else:
    print("No se encontraron cinco números consecutivos al principio de la cadena.")
plan=numeros
valor=planes[plan]

    
        
if convergencia == "SI" and operador == "WOM":
    if plan in planes:
        selleccion = dicplan['WOM']
    else:
        selleccion = '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div/div/div/div[2]/div[2]/fieldset/div[1]/span/span/input'
elif convergencia == "NO" and operador == "WOM":
    if plan in planes:
        selleccion = dicplan['WOMNO']
    else:
        selleccion = '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div/div/div/div[2]/div[2]/fieldset/div[1]/span/span/input'
elif convergencia == "SI" and operador == "MOVISTAR":
    if plan in planes:
        selleccion = dicplan['MOVISTAR']
    else:
        selleccion = dicplan['MOVISTARNO']
elif convergencia == "NO" and operador == "MOVISTAR":
    if plan in planes:
        selleccion = dicplan['MOVISTARNO']
    else:
        selleccion = dicplan['MOVISTAR']
elif convergencia == "SI" and operador == "TIGO":
    if plan in planes:
        selleccion = dicplan['TIGO']
    else:
        selleccion = dicplan['TIGONO']
elif convergencia == "NO" and operador == "TIGO":
    if plan in planes:
        selleccion = dicplan['TIGONO']
    else:
        selleccion = dicplan['TIGO']
elif convergencia == "NO" and operador == "ETB":
    if plan in planes:
        selleccion = dicplan["ETBNO"]
    else:
        selleccion = dicplan["ETB"]
elif convergencia == "SI" and operador == "ETB":
    if plan in planes:
        selleccion = dicplan["ETB"]
    else:
        selleccion = dicplan["ETBNO"]
elif convergencia == "NO" and operador == "AVANTEL":
    if plan in planes:
        selleccion = dicplan["AVANTELNO"]
    else:
        selleccion = dicplan["AVANTEL"]
elif convergencia == "SI" and operador == "AVANTEL":
    if plan in planes:
        selleccion = dicplan["AVANTEL"]
    else:
        selleccion = dicplan["AVANTELNO"]
else:
    selleccion = '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/div/div/div/div[2]/div[2]/fieldset/div[1]/span/span/input'
