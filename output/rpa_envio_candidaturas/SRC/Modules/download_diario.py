from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import Config.vars as vars
import Config.xpath as xpaths
import time
import re
import os

class SiteTRE:
    """
    Classe que automatiza o download do diário de uma determinada edição no site do TRE.
    """
    
    def __init__(self) -> None:
        """
        Inicializa a classe SiteTRE configurando o driver do Edge com as opções necessárias.
        """
        options = Options()
        options.headless = False  # Defina como True se não quiser que o navegador seja exibido
        
        # Configurações do perfil do Edge
        options.add_experimental_option("prefs", {
            "download.default_directory": vars.path_download,
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False,
            "profile.default_content_settings.popups": 0,
            "profile.default_content_setting_values.automatic_downloads": 1,
            "download.directory_upgrade": True,
        })

        self.driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
        
    def execute(self):
        """
        Executa o processo de download do diário. Retorna o resultado da operação.
        """
        result = self.__download_diario()
        if result != vars.Resultado.SUCESSO:
            return vars.Resultado.FIM_DO_LACO
        
        self.__quit()
        
        return vars.Resultado.SUCESSO
            
    def __quit(self):
        """
        Encerra o driver do navegador.
        """
        self.driver.quit()
        
    def __download_diario(self):
        """
        Realiza o download do diário a partir do site do TRE, verificando se a edição está disponível.
        """
        self.driver.get('https://dje-consulta.tse.jus.br/#/dje/calendario?trib=TRE-CE')
        
        init = 2
        
        download = False
        
        while download == False: 
            
            button_download = self.driver.find_element(by='xpath', value=xpaths.download_diario_diatual.format(str(init)))
            
            download = self.__check_edicao(button_download.text)
            
            if download == vars.Resultado.FIM_DO_LACO:
                return vars.Resultado.FIM_DO_LACO
            
            init += 1 
        
        button_download.click()
        
        time.sleep(20)
        
        return vars.Resultado.SUCESSO

    def __check_edicao(self, text: str):
        """
        Verifica se a edição do diário pode ser baixada com base no texto fornecido.
        
        Args:
            text (str): Texto contendo informações sobre a edição.
        
        Returns:
            bool: True se a edição pode ser baixada, False caso contrário.
        """
        
        edicao = self.__convert_text(text)
        
        if text == 'Recentes':
            return vars.Resultado.FIM_DO_LACO
        
        if edicao == vars.Resultado.EDICAO_FORA_DO_RANGE:
            return False
        
        files = os.listdir(vars.path_logs)
        
        if edicao in files:
            return False
        
        return True
        
    def __convert_text(self, text: str):
        """
        Converte o texto da edição para um formato padrão, extraindo o ano e o número da edição.
        
        Args:
            text (str): Texto a ser convertido.
        
        Returns:
            str: Edição formatada ou None se não for possível extrair as informações.
        """
        
        # Usar regex para extrair o ano e o número da edição
        year_match = re.search(r'\b(\d{4})\b', text)
        edition_match = re.search(r'nº\s*(\d+)', text)
        
        
        if year_match and edition_match:
            year = year_match.group(1)
            edition = edition_match.group(1)
            
            if year == '2024' and int(edition) <= 261:
                return vars.Resultado.EDICAO_FORA_DO_RANGE
            
            return f"{year}, nº {edition}.app"
        else:
            return None