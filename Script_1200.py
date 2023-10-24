"""

NOME:               esocial-1200.py
CLIENTE-CCBA:       Vallourec
VERSÃO:             1.2
DESCRIÇÃO:          realiza o preenchimento blablabla
DATA DE CRIAÇÃO:    21/09/2023
E-MAIL:             automacao@coimbrachaves.com.br
INTERPRETADOR:      Python 3.11.4 64-bit
LICENÇA:            Interno equipe P.R.E - Coimbra, Chaves & Batista Sociedade de Advogados
PROJETO:
Atualização:        Versão Feita para Otimizar o Codigo, inplemntando a função de reconhecimento de imagem para otimizar o processo de assinatura

"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
import tkinter as tk
from tkinter.simpledialog import askstring
import threading
import time
import pandas as pd
import pyautogui
import psutil
import cv2
import numpy as np
import csv
import os

# ------------------------------------------------ Bloco relacionado ao Navegador ------------------------------------------------

# Abrir navegador
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.prompt_for_download": False,  # Desabilita o diálogo de confirmação de download
    "download.directory_upgrade": True,  # Permite downloads em qualquer pasta
    "safebrowsing.enabled": "false"  # Desabilita o serviço de proteção contra sites maliciosos
})  # LInhas relacionada a algumas opções do
diretorio_atual = os.getcwd()
caminho_perfil_personalizado = os.path.join(diretorio_atual, "Chrome_Padrao")
chrome_options.add_argument(f"--user-data-dir={caminho_perfil_personalizado}")
navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
navegador.maximize_window()


# ------------------------------------------------ Fim do Bloco ------------------------------------------------

# ------------------------------------------------ Funçao de Reconhecimento de Imgagem ------------------------------------------------

# Função para verificar a presença de uma imagem em outra imagem
def verificar_presenca_imagem(imagem_grande, imagem_pequena):
    resultado = cv2.matchTemplate(imagem_grande, imagem_pequena, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(resultado)
    return max_val, max_loc

# Função para encontrar e clicar no centro da imagem
def encontrar_e_clicar_no_centro(imagem_path, intervalo_captura=1, limite_correspondencia=0.8, tempo_maximo=50):
    imagem_pequena = cv2.imread(imagem_path)

    # Inicie o contador de tempo
    tempo_inicial = time.time()

    while True:
        # Captura um screenshot da tela
        screenshot = pyautogui.screenshot()
        imagem_grande = np.array(screenshot)

        # Verifica a presença da imagem pequena na imagem grande
        max_val, max_loc = verificar_presenca_imagem(imagem_grande, imagem_pequena)

        # Se a imagem foi encontrada com base no limite de correspondência
        if max_val >= limite_correspondencia:
            # Encontre a localização do centro da imagem encontrada
            largura, altura = imagem_pequena.shape[1], imagem_pequena.shape[0]
            centro_x = max_loc[0] + largura // 2
            centro_y = max_loc[1] + altura // 2
            # Clique no canto inferior esquerdo da imagem encontrada
            pyautogui.click(max_loc[0], max_loc[1] + altura)

            break

        # Verifique se o tempo máximo foi atingido
        tempo_atual = time.time()
        if tempo_atual - tempo_inicial > tempo_maximo:
            print("Tempo máximo de busca atingido.")
            break

        # Aguarde o próximo intervalo de captura de tela
        time.sleep(intervalo_captura)



# ------------------------------------------------ Fim da função ------------------------------------------------

# ------------------------------------------------ Bloco para criar a Janela Tk ------------------------------------------------

# Cria uma janela principal
root = tk.Tk()
root.withdraw()  # Esconde a janela principal

# ------------------------------------------------ Fim do Bloco ------------------------------------------------


# ------------------------------------------------ Bloco Para Definir Variveis Globais ------------------------------------------------
# Bloco de Login
link = 'https://login.esocial.gov.br/login.aspx'
contador = 0

# ------------------------------------------------ Fim do Bloco ------------------------------------------------


# ------------------------------------------------ Bloco para Solcitar informaççoes para o Usuario ------------------------------------------------

# Solicita à pessoa para digitar a senha do Certificado
def getPassw():
    senha = askstring("Senha do Certificado", "Digite a senha do Certificado:")
    return senha


## Solicita à pessoa para digitar o CNPJ
def getCnpj():
    cnpj = askstring("CNPJ", "Digite o CNPJ:")
    return cnpj


# Solicita à pessoa para digitar a competência
def Compt():
    competencia = askstring("Competência", "Digite a competência (mês e ano):")
    return competencia


# ------------------------------------------------ Fim do Bloco ------------------------------------------------

# ------------------------------------------------ Funções de Login ------------------------------------------------

def clique_elemento():
    navegador.find_element(By.XPATH, "/html/body/div[1]/main/form/div/div[5]/button").click()


# Função para Logar a primeira vez no E-social capturando as posições
def login():

    global link
    while True:
        try:
            navegador.get(link)
            wait = WebDriverWait(navegador, 10)  # Tempo máximo de espera em segundos
            element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/form/fieldset/div[1]/div[2]/p/button")))
            element.click()
            # Clicar em seu certificado
            thread = threading.Thread(target=clique_elemento)
            thread.start()
            sleep(4)
            pyautogui.hotkey('enter')
            imagem_path = r'img\1695325395774.png'
            encontrar_e_clicar_no_centro(imagem_path)
            pyautogui.typewrite(senha)
            sleep(2)
            pyautogui.hotkey('enter')
            #imagem_path = r'img\1695325420078.png'
            encontrar_e_clicar_no_centro(imagem_path)
            element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[4]/div/form/div/section/div[1]/div/select")))
            element.click()
            pyautogui.moveTo(0, 7, duration=1)
            sleep(1)
            pyautogui.hotkey('down')
            sleep(1)
            pyautogui.hotkey('down')
            sleep(1)
            pyautogui.hotkey('enter')
            element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[4]/div/form/div/section/div[3]/div[1]/input")))
            element.click()
            pyautogui.typewrite(cnpj)
            sleep(1)
            navegador.find_element(By.XPATH, "/html/body/div[3]/div[4]/div/form/div/section/div[3]/div[2]/input").click()
            element = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[3]/div[4]/div/form/div/section/div[7]/div[2]/div[4]/div")))
            element.click()
            break
        except TimeoutException:
            print("Erro de Timeout. Tentando novamente em 10 minutos.")
            time.sleep(600)  # Aguarda 10 minutos antes de tentar novamente
            relogin()



# Relogar
def relogin():
    global navegador, chrome_options
    # Verifique se o navegador está em execução e finalize-o
    if navegador:
        navegador.quit()
        for proc in psutil.process_iter():
            try:
                if "chromedriver" in proc.name().lower():
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    sleep(30)
    navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()),  options=chrome_options)
    navegador.maximize_window()
    navegador.get(link)
    login()

# ------------------------------------------------ Fim do Bloco ------------------------------------------------

# ------------------------------------------------ Bloco para Pegar o CPF ------------------------------------------------

def GetCPF():
    df_excel = pd.read_excel('Dados\Dados_CPF.xlsx')
    df_csv = pd.read_csv('Dados\InformacoesGeradas.csv', sep=';', encoding='latin-1')

    # Encontre as entradas que estão na planilha, mas não estão no CSV
    resultado = df_excel[~df_excel['CPF-RPA'].isin(df_csv['CPF'])]

    # Salve o resultado em um novo arquivo Excel, se desejar
    resultado.to_excel(r'Dados\resultado.xlsx', index=False)
    Df_res = pd.read_excel(r'Dados\resultado.xlsx', dtype={'CPF-RPA': 'object'})
    return Df_res



# ------------------------------------------------ Fim do Bloco ------------------------------------------------

# ------------------------------------------------ Bloco de Consulta ------------------------------------------------

def Consulta(CPF):
    global compet
    wait = WebDriverWait(navegador, 10)  # Tempo máximo de espera em segundos
    # Definindo Link para a pagina do Governo que contem os arquivos que devemos assinar, passando o CPF e  a competencia
    link = f'https://www.esocial.gov.br/portal/FolhaPagamento/RemuneracaoCompleto?cpf={CPF}&competencia={compet}&possuiDae=False&tipo=1200'
    navegador.get(link)
    # Executando JavaScript para rolar a Página Até o final
    navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[5]/div/form/div[2]/div[4]/input")))
    element.click()
    try:
        imagem_path = r'img\1695358328144.png'
        encontrar_e_clicar_no_centro(imagem_path)
        imagem_path = r'img\1695358407745.png'
        encontrar_e_clicar_no_centro(imagem_path)
        pyautogui.hotkey('enter')
        imagem_path = r'img\1695358477753.png'
        encontrar_e_clicar_no_centro(imagem_path)
        imagem_path = r'img\1695325395774.png'
        encontrar_e_clicar_no_centro(imagem_path)
        pyautogui.typewrite(senha)
        sleep(2)
        pyautogui.hotkey('enter')
        imagem_path = r'img\2011.png'
        encontrar_e_clicar_no_centro(imagem_path)
        pyautogui.hotkey('enter')
        try:
            wait = WebDriverWait(navegador, 60)  # Tempo máximo de espera em segundos
            element = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[5]/div/div[1]/div")))
            msn_log = element.text
        except NoSuchElementException:
            try:
                wait = WebDriverWait(navegador, 120)  # Tempo máximo de espera em segundos
                element = wait.until(
                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[5]/div/div[1]/div")))
                msn_log = element.text
            except NoSuchElementException:
                try:
                    wait = WebDriverWait(navegador, 120)  # Tempo máximo de espera em segundos
                    element = wait.until(
                        EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[5]/div/form/div[1]")))
                    msn_log = element.text
                except NoSuchElementException:
                    try:
                        wait = WebDriverWait(navegador, 120)  # Tempo máximo de espera em segundos
                        element = wait.until(
                            EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[5]/div/form/div[1]/ul/li")))
                        msn_log = element.text
                    except:
                        msn_log = "XPath não encontrado"
    except:
        msn_log = "Erro desconhecido"

    return msn_log


# ------------------------------------------------ Fim do Bloco -------------------------------------------
def GravLog(CPF, Nome, resposta):
    nome_arquivo_csv = "Dados\InformacoesGeradas.csv"

    try:
        with open(nome_arquivo_csv, "a", newline="", encoding="utf-8") as arquivo_csv:
            escritor_csv = csv.writer(arquivo_csv, delimiter=";")
            escritor_csv.writerow([CPF, Nome, resposta])
        print("Informações gravadas com sucesso no arquivo Log.csv!")
    except Exception as e:
        print("Ocorreu um erro ao gravar as informações:", e)

def main():
    global contador
    login()
    Plan_cpf = GetCPF()
    for col, linh in Plan_cpf.iterrows():
        msn_log = Consulta(linh['CPF-RPA'])
        GravLog(linh['CPF-RPA'], linh['Nome do empregado ou candidato'], msn_log)
        contador += 1
        if contador == 30:
            contador = 0
            relogin()




senha = getPassw()
cnpj = getCnpj()
compet = Compt()
main()

# ------------------------------------------------ Fechar Navegador ------------------------------------------------
navegador.close()
# ------------------------------------------------ Fim do Bloco ------------------------------------------------
