"""Exemplo de model"""
from dataclasses import dataclass
from models.users import User

@dataclass
class ProgramLog:
    """
    Classe que representa o log de um programa.

    Atributos:
        etapa (str): A etapa do programa.
        status_log (str): O status do log.
        observacao (str, opcional): Observações adicionais sobre o log. Padrão é None.
        nome_user (str, opcional): Nome do usuário associado ao log. Padrão é uma string vazia.
    """
    etapa: str
    status_log: str
    observacao: str = None
    nome_user: str = ""
    
    # O __repr__ deve ser definido de acordo com as propriedades do log do projeto
    def __repr__(self) -> str:
        """
        Representação em string do objeto ProgramLog.

        Retorna:
            str: Uma representação formatada do log, incluindo tipo, etapa e observações.
        """
        obs = "" if self.observacao is None else f"Observação: {self.observacao}"
        
        msg = f"Tipo_log: {self.status_log}, Etapa: {self.etapa}, {obs} " 
        return msg
    
    @property
    def botcity_format(self):
        """
        Formato do log para a integração com o BotCity.

        Retorna:
            dict: Um dicionário contendo o status e a etapa do log.
        """
        return {"status": self.status_log, "etapa": self.etapa}

# Esse método deve ser definido de acordo com os parâmetros de log e models do projeto

def create_log_program_user(etapa: str, status_log: str, obs: str, user: User = None) -> ProgramLog:
    """
    Cria um log de programa para um usuário.

    Parâmetros:
        etapa (str): A etapa do programa.
        status_log (str): O status do log.
        obs (str): Observações adicionais sobre o log.
        user (User, opcional): Um objeto User associado ao log. Padrão é None.

    Retorna:
        ProgramLog: Um objeto ProgramLog com os dados fornecidos.
    """
    if user is not None:
        nome = user.nome
        return ProgramLog(etapa, status_log, obs, nome)
    
    return ProgramLog(etapa, status_log, obs)