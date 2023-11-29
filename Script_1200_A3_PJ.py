from browser import navegador
from janela import JanelaInterativa
from time import sleep
import pyautogui
import threading
from reconhecimentoDeImagem import reconhecerImagem
from extracao_dados import extracao
from arquivos_de_dados import arquivos_de_dados

senha = None
cnpj = None
compet = None



# Chamar e destruir Janela
def solicitarInfamcoesJanela(titulo, texto):
    janela_interacao_user = JanelaInterativa()
    #janela_interacao_user.__init__()
    informacoes = janela_interacao_user.solicitar_entrada(titulo, texto)
    janela_interacao_user.destuirJanela()
    return informacoes


# Solicitar Informações sobre 
def recolherInformações():
    global compet, senha, cnpj
    #Solicitar informações para o usuario.
    compet = solicitarInfamcoesJanela('Competência', 'Digite a competência (Ano e Mês): ')
    #Solicita a Senha
    senha = solicitarInfamcoesJanela('Senha do Certificado', 'Digite a senha do Certificado: ')
    # Solicita à pessoa para digitar o CNPJ
    cnpj = solicitarInfamcoesJanela('CNPJ', 'Digite o CNPJ: ')


# Função para clicar em um elemento do navegador
def clicar_elemento(selector):
    navegador_instancia.clicarElemento(selector, Browser)

# Preencher informação em um Campo OBS: Definido pelo XPATH
def preencher_campo(selector, value):
    navegador_instancia.escreverElemento(selector, value)
    sleep(0.5)

# Thread para Selecionar o 1 certificado
def thread_selecao_certificado():
    clicar_elemento('/html/body/div[1]/main/form/div/div[5]/button')

# Chama Função 
def encontrarClicarImg(caminho):
    instancia_imagem.encontrar_e_clicar_no_centro(caminho)

#Função de Login
def realizar_login(navegador):
    global senha, cnpj
 
    # Seleciona a caixa entrar
    clicar_elemento('/html/body/div[2]/div[3]/form/fieldset/div[1]/div[2]/p/button')

    # Inicie a thread para selecionar o certificado em segundo plano
    thread = threading.Thread(target=thread_selecao_certificado)
    thread.start()
    sleep(6)
    # Clica no Botação Ok para Abrir a tela de Assinatura do Certificadi
    pyautogui.hotkey('enter')
    encontrarClicarImg(r'imagens\caixaLoginGov.png')
    sleep(0.5)
    pyautogui.typewrite(senha)
    sleep(0.7)
    pyautogui.hotkey('enter')


# Função para Realizar Relogin no sistema do E-Social.        
def  realizar_relogin(Browser):
    navegador_instancia.encerrarNavegador(Browser)
    sleep(25)
    Browser = navegador_instancia.criarNavegador(True, False)
    realizar_login(Browser)
    
    
# Função para consultar CPF e inicluir Função de Assinatura
def consulta(CPF, Browser):
    global compet
    link = f'https://www.esocial.gov.br/portal/FolhaPagamento/RemuneracaoCompleto?cpf={CPF}&competencia={compet}&possuiDae=False&tipo=1200'
    Browser.get(link)
    # Executando JavaScript para rolar a Página Até o final
    Browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        # Clicar no botão salvar
        clicar_elemento("/html/body/div[3]/div[5]/div/form/div[2]/div[4]/input")
        assinarJava()
        navegador_instancia.esperarPaginaCarregar()
        resposta = instancia_extracao.extrcaoWebListaDeElementos(Browser.page_source, [{'class': 'fade-alert alert alert-danger'}, {'class': 'fade-alert alert alert-success retornoServidor'}])
        return resposta
    except:
        resposta ="Botão salvar não econtrolado"
        return resposta

# Chama Função para assina o Arquivo .Java
def assinarJava():
    # Chama a função para clicar no Assinador Java
    encontrarClicarImg(r'imagens\AbrirAssinadorJava.png')
    # Chama a função para clicar dentro do arquivo Java e depois seleciona Enter no Teclado.
    encontrarClicarImg(r'imagens\ClicarEmExecutar.png')
    pyautogui.hotkey('enter')
    # Chama a função para clicar no Botão Assinar Dentro da Janela do assinador Java
    encontrarClicarImg(r'imagens\ClicarBotaoAssinar.png')
    # Chama a função para Clicar na Caixa de inserir a Senha no Assinador Java
    encontrarClicarImg(r'imagens\ClicarCaixaDeSennha.png')
    pyautogui.typewrite(senha)
    sleep(0.5)
    # Chama a função para Clicar no Botão Ok
    encontrarClicarImg(r'imagens\ClicarBotaoOk.png')
    sleep(0.8)




if __name__ == "__main__":

    # Insanciando as classes
    navegador_instancia = navegador() # Objeto: Navegador
    instancia_imagem = reconhecerImagem() # Objeto para Reconhecer Imagem
    instancia_extracao = extracao() # Objeto Web Scraping 
    instancia_dados = arquivos_de_dados()
    janela_exibir_menssagem = JanelaInterativa()

    cont = 0
    

    # Chama função para recolher Informações 
    recolherInformações()

    # Chamando a Classe relacionada a Coleta de Info Sobre os Dados
    df = instancia_dados.lendo_base_de_dados()

    #Começo da Interação com o Navegador
    Browser = navegador_instancia.criarNavegador(True, False)
    navegador_instancia.denirTempo_Elemt(Browser)
    Browser.get('https://login.esocial.gov.br/login.aspx')
    realizar_login(Browser)

    for col, linh in df.iterrows():
        resposta = consulta(linh['CPF'], Browser)
        linh['html'] = str(resposta)
        linh['html2'] = instancia_extracao.extrair_texto_html(linh['html'])
        
        instancia_dados.GravLog(linh['CPF'], linh['Nome'], linh['html2'])
        # Relogin de 16 em 16 Execuções
        if cont == 12:
            realizar_relogin(Browser)
            cont = 0
        else:
            cont += 1


    janela_exibir_menssagem.exibir_informacoes('Fim da Lista.', 'A Lista foi finalizada!')
    navegador_instancia.encerrarNavegador(Browser)    
