from Config.vars import Resultado
from Modules.download_diario import SiteTRE
from Modules.check_diario import CheckDiario
from Modules.get_emails import GetSydle
from Modules.send_mails import SendMails
from Modules.logger import LogManager


class AutomationProcess:
    """
    Classe responsável pelo processo de automação, que inclui download de dados,
    verificação de diário, geração de lista de e-mails e envio de e-mails.
    """

    def __init__(self):
        """
        Inicializa uma nova instância da classe AutomationProcess.
        Cria instâncias dos módulos SiteTRE, CheckDiario, GetSydle, SendMails e LogManager.
        """
        self.site_tre = SiteTRE()
        self.check_diario = CheckDiario()
        self.get_sydle = GetSydle()
        self.send_mails = SendMails()
        self.log = None

    def execute(self) -> Resultado:
        """
        Executa o processo de automação, que inclui:
        1. Download do diário.
        2. Verificação do diário.
        3. Geração da lista de e-mails.
        4. Envio dos e-mails.

        Retorna:
            Resultado: O status da execução do processo.
        """
        result_download = self.site_tre.execute()

        if result_download != Resultado.SUCESSO:
            print("Nada a Executar")
            exit()

        list_zonas, edicao, data_publi = self.check_diario.execute()

        self.log = LogManager(log_file=edicao)

        self.log.info('Download do Diario realizado com sucesso')

        self.log.info('Verificção do diario realizada com sucesso')

        list_emails = self.get_sydle.execute(list_zonas)

        self.log.info(list_emails['status'])

        if list_emails['status'] == Resultado.SUCESSO and len(list_emails['zonas']) > 0:
            self.log.info('Lista de emails gerada com sucesso')
            self.log.info(list_emails['zonas'])

        elif len(list_emails['zonas']) == 0:
            self.log.info('Sem possiveis casos a enviar')
            exit()
            
        else:
            self.log.error('erro ao consultar e-mails' + str(list_emails['erro']))
        
        result_send_mails = self.send_mails.execute(list_emails['zonas'], edicao, data_publi)
        
        if result_send_mails['status'] == Resultado.SUCESSO:
            
            self.log.info('Emails enviados com sucesso')
            self.log.info(result_send_mails['list_emails'])
        
        else:
            self.log.error('erro ao enviar e-mails' + str(result_send_mails['erro']))