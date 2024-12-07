from source.utils import vars
from pathlib import Path
import os
import shutil


class WriteScripts():
   
    def __init__(self):
        self.path_input = vars.path_input
        self.path_output = vars.path_output
        self.script_ext = vars.ext_scripts

    def geretare_project(self,script_doc):

        for root, dirs, files in os.walk(self.path_output):
            if script_doc['arq_name'] in files:
                # Monta o caminho completo do arquivo
                caminho_arquivo = os.path.join(root, script_doc['arq_name'])
                
                # Sobrescreve o conteúdo do arquivo
                with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                    f.write(script_doc['script'])
                
                print(f"Conteúdo do arquivo '{script_doc['arq_name']}' substituído com sucesso no caminho '{caminho_arquivo}'.")
                arquivo_encontrado = True
                # Caso você queira parar após encontrar o primeiro arquivo, use break
                # break

        if not arquivo_encontrado:
            print(f"Arquivo '{script_doc['arq_name']}' não foi encontrado em '{self.path_output}' ou suas subpastas.")

    def create_project(self):
        subdirs = [d for d in os.listdir(self.path_input) if os.path.isdir(os.path.join(self.path_input, d))]

        # Verifica se existe apenas uma única pasta no diretório de origem
        if len(subdirs) == 1:
            pasta_unica = subdirs[0]
            origem = os.path.join(self.path_input, pasta_unica)
            destino = os.path.join(self.path_output, pasta_unica)
            
            # Copia a pasta única para o destino
            shutil.copytree(origem, destino)
            print(f"Pasta '{origem}' copiada para '{destino}'.")
        elif len(subdirs) >= 1:
            print("Não há exatamente uma pasta no diretório de origem. Nenhuma cópia foi realizada.")
        else:
            print("Não há pastas no diretório de origem. Nenhuma cópia foi realizada.")