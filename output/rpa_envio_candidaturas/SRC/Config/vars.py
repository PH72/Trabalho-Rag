import json 
from os import getenv, getcwd
import os
from enum import Enum
from pathlib import Path
#Variável que representa o ambiente 
ENV=getenv('ENV')  

#caminhos
num_dir_to_src = 2
src_folder = Path(__file__)
for i in range(num_dir_to_src): src_folder = src_folder.parent


src_folder = src_folder.__str__()
path_elements = src_folder + "\\Files\\elements"

path_download = src_folder + "\\Files\\download"

path_zonas = src_folder + "\\Files\\zonas"

path_logs = src_folder + "\\Files\\logs"

path_tools = src_folder + "\\Files\\tools"



#Metodo que faz a limpeza das pastas do projeto

def limpar_pasta(caminho_pasta):
    """
    Limpa todos os arquivos de uma pasta especificada.

    Args:
        caminho_pasta (str): O caminho da pasta a ser limpa.
    """
    try:
        for arquivo in os.listdir(caminho_pasta):
            caminho_arquivo = os.path.join(caminho_pasta, arquivo)
            if os.path.isfile(caminho_arquivo):
                os.remove(caminho_arquivo)
                print(f"Removido arquivo: {caminho_arquivo}")
            elif os.path.isdir(caminho_arquivo):
                print(f"Encontrada pasta, ignorando: {caminho_arquivo}")
        print(f"Pasta {caminho_pasta} limpa com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao limpar a pasta: {e}")
        
limpar_pasta(path_zonas)
limpar_pasta(path_download)        


#API
BASE_API = ""

#Enums do projeto
class Resultado(Enum):
    """
    Enum que representa os resultados possíveis de operações.
    """
    SUCESSO = 0
    EDICAO_FORA_DO_RANGE = 1
    FIM_DO_LACO = 2
    ERRO_DEFAULT = -42
    
#Metodos de busca Sydle

def elastic_id(id_staff_member):
    """
    Gera uma consulta JSON para buscar um membro da equipe pelo ID.

    Args:
        id_staff_member (str): O ID do membro da equipe.

    Returns:
        str: Consulta JSON como string.
    """
    return json.dumps({
                        "query": {
                            "term": {
                            "_id": id_staff_member 
                            }
                        }
                    })
        

def elastic_organization_unit(zona):
    """
    Gera uma consulta JSON para buscar uma unidade organizacional pela zona.

    Args:
        zona (str): A zona a ser buscada.

    Returns:
        str: Consulta JSON como string.
    """
    return json.dumps({
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "initials.keyword": zona
                        }
                    }
                ]
            }
        }
    })




#Dicionario de prontuação de Palavras
word_weight = [
    {'palavra': 'prefeito', 'peso': 5.0, 'quebra_linha': True},
    {'palavra': 'vice-prefeito', 'peso': 5.0, 'quebra_linha': True},
    {'palavra': 'vereador', 'peso': 5.0, 'quebra_linha': True},
    {'palavra': 'registro de candidatura', 'peso': 12.0, 'quebra_linha': False},
    {'palavra': 'registro dos candidatos', 'peso': 7.0, 'quebra_linha': False}
]