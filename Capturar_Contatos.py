from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located

foto_captura_contato = input("Digite o link da postagem que deseja capturar os contatos: \n=> ")
# Abre o firefox
navegador = webdriver.Firefox(executable_path=r'./Arquivos/Firefox/geckodriver.exe')
# Tempo de espera do navegador para consultas
tempo_espera_navegador = WebDriverWait(navegador, 30)


def logar():
    usuario = ''
    senha = ''
    time.sleep(5)
    elemento_usuario = navegador.find_element_by_xpath("//input[@name='username']")
    elemento_usuario.clear()
    elemento_usuario.send_keys(usuario)
    elemento_senha = navegador.find_element_by_xpath("//input[@name='password']")
    elemento_senha.clear()
    elemento_senha.send_keys(senha)
    time.sleep(1)
    elemento_senha.send_keys(Keys.RETURN)
    btn_agoranao = (By.XPATH, "/html/body/div[1]/section/main/div/div/div/div/button")
    tempo_espera_navegador.until(presence_of_element_located(btn_agoranao))
    navegador.find_element(*btn_agoranao).click()
    btn_agoranao = (By.CSS_SELECTOR, "button.aOOlW:nth-child(2)")
    tempo_espera_navegador.until(presence_of_element_located(btn_agoranao))
    navegador.find_element(*btn_agoranao).click()
    time.sleep(5)
    # Abre o site desejado
    navegador.get(foto_captura_contato)


navegador.get("https://www.instagram.com/")
# Pesquisa pelo botão Fechar (Login)
btn_fechar_login = (By.CSS_SELECTOR, ".glyphsSpriteGrey_Close")
btn_logar = (By.CSS_SELECTOR, "div.bkEs3:nth-child(3)")
# Espera o botão aparecer
tempo_espera_navegador.until(presence_of_element_located(btn_logar))
# Clica no botão
navegador.find_element(*btn_logar).click()
logar()


btn_carregar_comentarios = (By.CSS_SELECTOR, ".NUiEW > button:nth-child(1)")
tempo_espera_navegador = WebDriverWait(navegador, 2)
try:
    tempo_espera_navegador.until(presence_of_element_located(btn_carregar_comentarios))
    while presence_of_element_located(btn_carregar_comentarios):
        tempo_espera_navegador.until(presence_of_element_located(btn_carregar_comentarios))
        navegador.find_element(*btn_carregar_comentarios).click()
except:
    print(f"todos os comentarios foram carregados.")

caixa_cotatos = (By.CSS_SELECTOR, ".XQXOT")
cx = navegador.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/"
                                     "article/div/div[2]/div/div[2]/div[1]/ul")
contatos = navegador.find_elements_by_class_name("sqdOP yWX7d     _8A5w5   ZIAjV ")
contato = cx.find_elements_by_tag_name('a')
lista = []
print("coletando e organizando contatos...")
for num, usr_contato in enumerate(contato):
    if usr_contato.get_attribute("class") == "sqdOP yWX7d     _8A5w5   ZIAjV ":
        # if usr_contato not in lista:
        lista.append("@" + usr_contato.text)
    if usr_contato.get_attribute("class") == "notranslate":
        lista.append(usr_contato.text)
df = pd.DataFrame(lista, columns=['NOME'])
print(f"{len(df)} contatos foram coletados")
df = df.drop_duplicates()
df.to_csv("Arquivos/arquivo.txt",index=False, header=None)
print(df)
print("fim")
