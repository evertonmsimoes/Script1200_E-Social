from bs4 import BeautifulSoup



class extracao:
    def extrcaoWeb(self, page_content, dicionario):
        site = BeautifulSoup(page_content, 'html.parser')
        informacao = site.find('div', attrs=dicionario)
        informacao = informacao
        return informacao
    
    # Extração de Lista de Elemnteos
    def extrcaoWebListaDeElementos(self, page_content, ListaDicionario):
            site = BeautifulSoup(page_content, 'html.parser')
            for dicionario in ListaDicionario:
                informacao = site.find('div', attrs=dicionario)
                informacao = informacao
                if informacao is not None:
                    break
            if informacao is None:
                 informacao = "Não foi encontrado nenhum elemento da  lista na Pagina."
            return informacao

    # Pegar texto
    # Defina uma função para extrair o texto do HTML e remover os caracteres indesejados
    def extrair_texto_html(self, html):
        # Verifique se o valor é uma string antes de usar o BeautifulSoup
        if isinstance(html, str):
            soup = BeautifulSoup(html, 'html.parser')
            texto = soup.get_text()
            # Remova os caracteres indesejados
            texto = texto.replace('x000D_', '').replace('×', '').replace('.', '').strip()
            return texto
        else:
            return html  # Se não for uma string, mantenha o valor original
