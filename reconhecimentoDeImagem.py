import cv2
import numpy as np
import pyautogui
import time
from time import sleep

class reconhecerImagem():

    # Função para verificar a presença de uma imagem em outra imagem
    def verificar_presenca_imagem(self, imagem_grande, imagem_pequena, limite_correspondencia=0.8):
        resultado = cv2.matchTemplate(imagem_grande, imagem_pequena, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(resultado)

        # Se a imagem foi encontrada com base no limite de correspondência
        if max_val >= limite_correspondencia:
            return True, max_loc
        else:
            return False, None


    # Função para encontrar e clicar no centro da imagem
    def encontrar_e_clicar_no_centro(self, imagem_path, limite_correspondencia=0.8, tempo_maximo=50):
        # Inicie o contador de tempo
        tempo_inicial = time.time()

        while True:
            # Captura um screenshot da tela
            screenshot = pyautogui.screenshot()
            imagem_grande = np.array(screenshot)
            imagem_pequena = cv2.imread(imagem_path)

            # Verifica a presença da imagem pequena na imagem grande
            encontrada, max_loc = self.verificar_presenca_imagem(imagem_grande, imagem_pequena, limite_correspondencia)

            # Se a imagem foi encontrada
            if encontrada:
                # Encontre a localização do centro da imagem encontrada
                largura, altura = imagem_pequena.shape[1], imagem_pequena.shape[0]
                centro_x = max_loc[0] + largura // 2
                centro_y = max_loc[1] + altura // 2
                # Clique no centro da imagem encontrada
                sleep(0.7)
                pyautogui.click(centro_x, centro_y)

                break

            # Verifique se o tempo máximo foi atingido
            tempo_atual = time.time()
            if tempo_atual - tempo_inicial > tempo_maximo:
                print("Tempo máximo de busca atingido.")
                break

            # Aguarde um pequeno intervalo de tempo antes de verificar novamente
            time.sleep(1)
