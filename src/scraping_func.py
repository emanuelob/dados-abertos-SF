from selenium import webdriver
from selenium.webdriver.common.by import By


def acessar_pagina_de_pesquisa():
    driver.get("https://www25.senado.leg.br/web/atividade/pronunciamentos")


def abrir_navegador():
    global driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
