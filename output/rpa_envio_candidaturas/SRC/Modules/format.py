from models.users import User

def format_user(user: dict) -> User:
    """
    Formata um dicionário de usuário em uma instância da classe User.

    Args:
        user (dict): Um dicionário contendo as informações do usuário, incluindo 'nome' e 'idade'.

    Returns:
        User: Uma instância da classe User com os dados formatados.
    """
    return User(user['nome'], user['idade'])