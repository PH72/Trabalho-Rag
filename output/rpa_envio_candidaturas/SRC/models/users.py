from dataclasses import dataclass

@dataclass
class User:
    """
    Classe que representa um usuário.

    Atributos:
        nome (str): O nome do usuário.
        idade (int): A idade do usuário.
    """
    nome: str
    idade: int
