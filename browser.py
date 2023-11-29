from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
import psutil
import os


class navegador:
    global chrome_options
    chrome_options = Options()


    def denirTempo_Elemt(self, navegador):
        global wait 
        wait = WebDriverWait(navegador, 100)
        
    def definindoPerfil(self): 
       # global chrome_options
        chrome_options.add_experimental_option("prefs", {
            "download.prompt_for_download": False,  # Desabilita o diálogo de confirmação de download
            "download.directory_upgrade": True,  # Permite downloads em qualquer pasta
            "safebrowsing.enabled": "false"  # Desabilita o serviço de proteção contra sites maliciosos
        })  # LInhas relacionada a algumas opções do
        diretorio_atual = os.getcwd()
        caminho_perfil_personalizado = os.path.join(diretorio_atual, "Chrome_Padrao")
        chrome_options.add_argument(f"--user-data-dir={caminho_perfil_personalizado}")
        return chrome_options
    
    def chrome_optionsnavegador_em_segundo_plano(self):
        #global chrome_options
        chrome_options.add_argument("--headless")
        return chrome_options
    
    def criarNavegador(self, perfil, headless):
        global chrome_options
        if perfil == True or headless == True:
            if headless == True:
               chrome_options = self.chrome_optionsnavegador_em_segundo_plano()
            if perfil == True:
                chrome_options = self.definindoPerfil()
            Browser =  webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            Browser.maximize_window()
        else:
            Browser =  webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            Browser.maximize_window()

        return Browser
    
    def clicarElemento(self, xpaf, navegador):

        element = wait.until((Ec.visibility_of_element_located((By.XPATH, xpaf))))
        element.click()


    def clicarElementoClass(self, xpaf, navegador):
        element = wait.until((Ec.visibility_of_element_located((By.ID, xpaf))))
        element.click()
    
    def esperarPaginaCarregar(Self):

        wait.until(Ec.presence_of_element_located((By.TAG_NAME, 'body')))
    
    def escreverElemento(self, xpaf,  valor):

        element = wait.until((Ec.visibility_of_element_located((By.XPATH, xpaf))))
        element.send_keys(valor)

    def digitarAlerta(self, pasta, navegador):

        alerta = Alert(navegador)
        alerta.send_keys(pasta)
        alerta.accept()

    def encerrarNavegador(self, navegador):

        if navegador:
            navegador.quit()
            for proc in psutil.process_iter():
                try:
                    if "chromedriver" in proc.name().lower():
                        proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

