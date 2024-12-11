import logging
import Config.vars as vars

class LogManager:
    """
    Classe responsável pela gestão de logs da aplicação.
    """

    def __init__(self, log_file, level=logging.DEBUG):
        """
        Inicializa o LogManager.

        Args:
            log_file (str): Nome do arquivo de log.
            level (int): Nível de log a ser usado. O padrão é logging.DEBUG.
        """
        self.logger = logging.getLogger('AppLogger')
        self.logger.setLevel(level)
        
        # Criar um handler para o arquivo de log
        file_handler = logging.FileHandler(vars.path_logs +'\'+ log_file+'.app')
        file_handler.setLevel(level)
        
        # Criar um handler para o console (opcional)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # Criar um formato para os logs
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        
        # Adicionar o formato aos handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Adicionar os handlers ao logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, message):
        """
        Registra uma mensagem de debug.

        Args:
            message (str): Mensagem a ser registrada.
        """
        self.logger.debug(message)
    
    def info(self, message):
        """
        Registra uma mensagem informativa.

        Args:
            message (str): Mensagem a ser registrada.
        """
        self.logger.info(message)
    
    def warning(self, message):
        """
        Registra uma mensagem de aviso.

        Args:
            message (str): Mensagem a ser registrada.
        """
        self.logger.warning(message)
    
    def error(self, message):
        """
        Registra uma mensagem de erro.

        Args:
            message (str): Mensagem a ser registrada.
        """
        self.logger.error(message)
    
    def critical(self, message):
        """
        Registra uma mensagem crítica.

        Args:
            message (str): Mensagem a ser registrada.
        """
        self.logger.critical(message)