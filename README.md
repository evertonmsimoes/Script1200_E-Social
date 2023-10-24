# Automação assinatura Competencia 1200 e-Social

Este é um script Python que automatiza a assinatura da competência 1200 no sistema e-Social, um sistema brasileiro relacionado a questões trabalhistas. O script utiliza a biblioteca Selenium para interagir com o site e-Social, realizar login, localizar elementos na tela e assinar os documentos necessários.

Pré-requisitos
Antes de executar o script, certifique-se de atender aos seguintes pré-requisitos:

Python e Bibliotecas: Tenha o Python instalado em seu sistema e certifique-se de que todas as bibliotecas necessárias, como o Selenium, Tkinter e outras, estejam instaladas. Você pode instalá-las usando o pip.

bash
Copy code
pip install selenium webdriver_manager pandas pyautogui opencv-python-headless
Navegador Chrome: Certifique-se de ter o navegador Google Chrome instalado, pois o script é configurado para funcionar com ele. Além disso, é necessário o ChromeDriver compatível com a versão do Chrome instalada.

Configuração
1. Configuração do Navegador
O script configura o navegador Chrome com opções específicas, como desabilitar a proteção contra sites maliciosos, permitir downloads em qualquer pasta e definir um diretório de perfil personalizado. Certifique-se de que o ChromeDriver esteja instalado corretamente e acessível.

2. Imagens
O script faz uso de imagens para localizar elementos na tela. Certifique-se de que as imagens usadas (por exemplo, em imagem_path) estejam corretamente configuradas e acessíveis.

3. Arquivos de Dados
O script também pode ler dados de arquivos, como planilhas Excel (no formato .xlsx) e arquivos CSV. Certifique-se de que os caminhos dos arquivos estejam corretos e os arquivos contenham os dados esperados.

Uso
Execute o script Python.

O script abrirá um navegador Chrome, solicitará a senha do certificado, CNPJ e competência (mês e ano).

O script realizará automaticamente o login no site e-Social, localizará os documentos da competência 1200 e assinará os documentos necessários. O processo pode exigir ação do usuário, como clicar em elementos específicos no site.

O processo é repetido até que todos os documentos sejam assinados.

Notas
É importante entender que este script foi projetado para interagir com um site específico e pode não funcionar corretamente se o site for alterado.

O script inclui funcionalidades de reconhecimento de imagem para localizar elementos na tela, o que pode ser sensível a alterações na resolução da tela ou em elementos do site.

Certifique-se de que o arquivo CSV (InformacoesGeradas.csv) esteja configurado corretamente para receber as informações.

O script pode demorar um tempo considerável para ser concluído, dependendo da quantidade de documentos a serem assinados.

Contribuições
Contribuições e melhorias são bem-vindas! Sinta-se à vontade para abrir problemas ou enviar solicitações de pull.

