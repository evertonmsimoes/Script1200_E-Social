import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

class JanelaInterativa:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.withdraw()  # Oculta a janela principal
        
    def exibir_informacoes(self, titulo, mensagem):
        tk.messagebox.showinfo(titulo, mensagem)

    def solicitar_entrada(self, titulo, pergunta):
        resposta = simpledialog.askstring(titulo, pergunta)
        return resposta
    
    def destuirJanela(self):
        self.janela.destroy()


