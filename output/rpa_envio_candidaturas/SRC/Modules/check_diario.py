import Config.vars as vars
import fitz
import os
import re
import pandas as pd

class CheckDiario:

    def __init__(self) -> None:
        """
        Inicializa a classe CheckDiario.
        Define os caminhos para os arquivos de download e zonas, além de inicializar variáveis para informações resumidas e dados do documento.
        """
        self.arq_path_download = vars.path_download
        self.arq_path_zonas = vars.path_zonas
        self.summary_info = []
        self.end_pag_doc = None
        self.edicao = None
        self.data_publi = None

    def execute(self):
        """
        Executa o processo de verificação do diário.
        Obtém as informações, organiza o resumo, lê o PDF usando expressões regulares e verifica as zonas no PDF.
        
        Returns:
            list: Uma lista de e-mails, a edição e a data de publicação.
        """
        self.__get_infos()
        self.__sumary_organizate()
        self.__read_pdf_regex()
        list_emails = self.__check_pdf_zonas()
        
        return list_emails, self.edicao, self.data_publi

    def __get_infos(self):
        """
        Obtém as informações do arquivo PDF, incluindo a edição e a data de publicação.
        
        Raises:
            FileNotFoundError: Se nenhum arquivo PDF for encontrado no diretório especificado.
        """
        files = os.listdir(self.arq_path_download)
        pdf_files = [file for file in files if file.endswith('.pdf')]
        if not pdf_files:
            raise FileNotFoundError("Nenhum arquivo PDF encontrado no diretório especificado.")
        
        file = os.path.join(self.arq_path_download, pdf_files[0])
        
        # Abrir o documento PDF
        documento = fitz.open(file)
        
        # Quantidade de paginas do documento
        self.end_pag_doc =  documento.page_count
        
        # Selecionar a primeira página
        primeira_pagina = documento.load_page(0)
    
        # Extrair o texto da primeira página linha por linha
        linhas_pagina = primeira_pagina.get_text("text").split('\n')
        
        self.edicao = linhas_pagina[5].replace("Ano: ",'')
        self.data_publi = linhas_pagina[8].replace("Publicação: ",'')
        
        return vars.Resultado.SUCESSO

    def __read_pdf_regex(self):
        """
        Lê o PDF e verifica as zonas eleitorais utilizando expressões regulares.
        
        Returns:
            Resultado: O resultado da operação.
        """
        for index, item in enumerate(self.summary_info):
            if 'zona eleitoral' in item['titulo'].lower():
                start_pag = item['pagina']
                
                count = 1
                check = False
                while check == False: 
                    
                    if index+count >= len(self.summary_info):
                        end_pag = self.end_pag_doc
                        print(start_pag)
                        print(end_pag)
                
                        self.__extract_pages(int(start_pag),int(end_pag),item['titulo'])
                        
                        return vars.Resultado.SUCESSO

                    if 'editais' in self.summary_info[index+count]['titulo'].lower() or'portarias' in self.summary_info[index+count]['titulo'].lower() or 'despachos' in self.summary_info[index+count]['titulo'].lower() or 'sentenças' in self.summary_info[index+count]['titulo'].lower() or 'decisões' in self.summary_info[index+count]['titulo'].lower():
                        count += 1
                        continue
                    
                    end_pag = self.summary_info[index+count]['pagina']
                    check = True
                
                
                print(start_pag)
                print(end_pag)
                
                # if end_pag == '' 
                
                self.__extract_pages(int(start_pag),int(end_pag),item['titulo'])
        
        return vars.Resultado.SUCESSO                
            
    def __extract_pages(self, start_page: int, end_page: int, name:str):
        """
        Extrai as páginas de um PDF e salva como um novo arquivo PDF.
        
        Args:
            start_page (int): Número da página inicial (1-indexed).
            end_page (int): Número da página final (1-indexed).
            name (str): Nome do arquivo de saída.
        
        Raises:
            FileNotFoundError: Se nenhum arquivo PDF for encontrado no diretório especificado.
            ValueError: Se os valores de páginas forem inválidos.
        """
        files = os.listdir(self.arq_path_download)
        pdf_files = [file for file in files if file.endswith('.pdf')]
        if not pdf_files:
            raise FileNotFoundError("Nenhum arquivo PDF encontrado no diretório especificado.")
        
        file = os.path.join(self.arq_path_download, pdf_files[0])
        document = fitz.open(file)
        self.end_pag_doc = document.page_count
        
        if start_page < 1 or end_page > document.page_count or start_page > end_page:
            document.close()
            raise ValueError("Valor de páginas inválido!")

        output_pdf = fitz.open()
        
        for page_num in range(start_page-1, end_page):
            output_pdf.insert_pdf(document, from_page=page_num, to_page=page_num)
        
        output_filename = f'{name}.pdf'
        output_filepath = os.path.join(self.arq_path_zonas, output_filename)
        output_pdf.save(output_filepath)
        
        return vars.Resultado.SUCESSO

    def __sumary_organizate(self):
        """
        Organiza o resumo do PDF, extraindo títulos e números de páginas.
        
        Raises:
            FileNotFoundError: Se nenhum arquivo PDF for encontrado no diretório especificado.
        """
        files = os.listdir(self.arq_path_download)
        pdf_files = [file for file in files if file.endswith('.pdf')]
        if not pdf_files:
            raise FileNotFoundError("Nenhum arquivo PDF encontrado no diretório especificado.")
        
        file = os.path.join(self.arq_path_download, pdf_files[0])
        document = fitz.open(file)
        
        if self.end_pag_doc <= 10:
            len_sum = self.end_pag_doc
        else: 
            len_sum = 10   
        
        for page_num in range(len_sum):
            page = document.load_page(page_num)
            text = page.get_text("text")
            
            lines = text.split("\n")
            for line in lines:
                
                if line.count('.') > 50:
                    
                    partes = line.split('.')
                    titulo = partes[0].strip()
                    pagina_inicio = partes[-1].strip()
                    
                    dicionario = {'titulo': titulo, 'pagina': pagina_inicio}
                    
                    chave_encontrada = any(dicionario['titulo'] in dict_temp.values() for dict_temp in self.summary_info)
                    
                    if chave_encontrada:
                        continue
                    
                    self.summary_info.append(dicionario)
                    
                      
                else:
                    print("A linha não contém mais de 100 pontos.")
        
        for i in self.summary_info:
            print(i)
            
        return vars.Resultado.SUCESSO  
    
    def __check_pdf_zonas(self): 
        """
        Verifica os arquivos PDF nas zonas e identifica candidatos irregulares.
        
        Returns:
            list: Lista de zonas com informações sobre candidatos irregulares.
        """
        list_zonas = []
        list_arqs = os.listdir(self.arq_path_zonas)
        
        for indice, filename in enumerate(list_arqs):
            path = os.path.join(self.arq_path_zonas, filename)
            
            document = fitz.open(path)
            
            text = ""
            for page_num in range(len(document)):
                
                page = document.load_page(page_num)
                text += page.get_text()
            
            
            name = filename.split('.')[0]
            print(name)
            
            text = text.lower()
            
            text = text.split(name.lower(),1)[1]
            
            if indice + 1 < len(list_arqs):
                
                next_doc = list_arqs[indice+1].split('.')[0].lower()
                
                text = text.split(next_doc)[0]
            
            pontos = self.__calculate_match(text, vars.word_weight)
            
            if pontos >= 12:
                tcu_list, tce_list = self.__check_irregular_candidates(text)
                
                irregular_candidates_tcu = bool(tcu_list)
                irregular_candidates_tce = bool(tce_list)
                             
                list_zonas.append({
                    'filename':filename,
                    'irregular_candidates_tcu':irregular_candidates_tcu,
                    'irregular_candidates_tce':irregular_candidates_tce,
                    'tcu_list':tcu_list,
                    'tce_list':tce_list})
        
        return list_zonas  
    
    def __check_irregular_candidates(self,text):
        """
        Verifica se há candidatos irregulares nas listas do TCU e TCE.
        
        Args:
            text (str): Texto a ser verificado.
        
        Returns:
            tuple: Dupla contendo listas de candidatos irregulares do TCU e TCE.
        """
        df_tcu = pd.read_csv(f"{vars.path_tools}\Candidatos_Irregulares_TCU.csv",delimiter=';',encoding='ISO-8859-1')
        df_tce = pd.read_csv(f"{vars.path_tools}\Candidatos_Irregulares_TCE.csv",delimiter=';',encoding='ISO-8859-1')
        
        text_lower = text.lower()
        
        tcu_list = [row.to_dict() for _, row in df_tcu.iterrows() if row['Nome'].lower() in text_lower]
        tce_list = [row.to_dict() for _, row in df_tce.iterrows() if row['Gestor'].lower() in text_lower]  
        
        return tcu_list, tce_list        
    
    def __calculate_match(self,text, word_weight):
        """
        Calcula a pontuação de correspondência com base nas palavras e seus pesos.
        
        Args:
            text (str): Texto a ser verificado.
            word_weight (list): Lista de palavras e seus pesos correspondentes.
        
        Returns:
            int: Pontuação final de correspondência.
        """
        final_score = 0
        for item in word_weight:
            word = item['palavra']
            weight = item['peso']
            quebra_linha = item['quebra_linha']
            
            if quebra_linha:
                padrao = rf'\n{word}\s*\n'
                if re.search(padrao, text):
                    final_score += weight
            else:
                if word in text:
                    final_score += weight
        print(final_score)            
        return final_score