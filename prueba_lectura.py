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
from selenium.common.exceptions import TimeoutException
driver = webdriver.Edge('msedgedriver.edge')
driver.get('https://poliedro.comcel.com.co/LoginPoliedro/Login.aspx')
cone=0
while cone!=4:
    time.sleep(4)
    driver.find_element('xpath','//*[@id="ctl00_ContentPlaceHolder1_BtnRegresarMensaje"]').click()
    time.sleep(4)
    driver.back()
    time.sleep(3)
    cone+=1