import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import Config.vars as vars
from dotenv import load_dotenv
import os


class SendMails:
    """
    Classe responsável pelo envio de e-mails com informações sobre candidaturas.
    """
    
    def __init__(self) -> None:
        """
        Inicializa a classe e carrega as variáveis de ambiente necessárias para o envio de e-mails.
        """
        load_dotenv()

        self.relay_host = os.getenv('RELAY_HOST')
        self.relay_port = os.getenv('RELAY_PORT')
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.username = os.getenv('USER_AD')
        self.password = os.getenv('PASSWORD_AD')

        self.to = ["pedro.freitas1@mpce.mp.br","dilthey.forte@mpce.mp.br"]
        self.bcc = ["pedro.freitas1@mpce.mp.br","dilthey.forte@mpce.mp.br"]

    def execute(self, list_emails, edicao, data_publi):
        """
        Executa o envio de e-mails para uma lista de destinatários.

        Args:
            list_emails (list): Lista de dicionários contendo informações sobre os e-mails a serem enviados.
            edicao (str): Informação sobre a edição do Diário.
            data_publi (str): Data de publicação.

        Returns:
            dict: Dicionário contendo o status do envio e a lista de e-mails com seus status.
        """
        try:
            for i, dict in enumerate(list_emails):
                result = self.__send_mail(dict, edicao, data_publi)
                if result['status'] == vars.Resultado.SUCESSO:
                    dict['status'] = "Enviado"
                else:
                    dict['status'] = "Falha: "+ str(result['erro'])
            return {'status':vars.Resultado.SUCESSO,'list_emails':list_emails}        
        except Exception as e:
            return {'status':vars.Resultado.ERRO_DEFAULT, 'erro':e}

    def __send_mail(self, dict, edicao, data_publi):
        """
        Envia um e-mail para um destinatário específico com as informações fornecidas.

        Args:
            dict (dict): Dicionário contendo as informações do destinatário e do e-mail.
            edicao (str): Informação sobre a edição do Diário.
            data_publi (str): Data de publicação.

        Returns:
            dict: Dicionário contendo o status do envio e, se houver erro, a mensagem de erro.
        """
        path = vars.path_zonas +'\'+ dict['filename']
        ca_cert = vars.path_tools+'\'+'ca.pem'

        # Criar uma mensagem MIME
        message = MIMEMultipart("alternative")
        if dict.get('irregular_candidates_tcu', True) or dict.get('irregular_candidates_tce', True):
            message["Subject"] = "Registro de candidatura e pessoas constando na lista de contas irregulares do TCU ou TCE " + dict['filename'].replace('.pdf','')
        else:
            message["Subject"] = "Registro de candidatura " + dict['filename'].replace('.pdf','')    
        message["From"] = self.sender_email
        message["To"] = ', '.join(dict['email'])
        message["Bcc"] = ', '.join(self.bcc)  # Adiciona endereços de BCC

        # Corpo do email
        text = f"""
        Olá 
        
        Estamos enviando este e-mail porque acreditamos que a edição {edicao} do Diário do TRE-CE publicada em {data_publi}, contém informações de registro de candidaturas para as eleições de 2024. O trecho que diz respeito à sua zona eleitoral está anexado.
        """
        html = self.__build_email_body(dict, edicao, data_publi)

        # Anexar partes do corpo do email ao contêiner MIME
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        # Anexar o arquivo
        with open(path, "rb") as attachment:
            part = MIMEBase("application", "pdf")
            part.set_payload(attachment.read())

        # Codificar o arquivo em base64
        encoders.encode_base64(part)

        # Adicionar cabeçalhos
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {dict['filename'].replace('ª','')}",
        )

        # Anexar a parte ao email
        message.attach(part)

        # Contexto SSL com o certificado CA
        context = ssl.create_default_context(cafile=ca_cert)

        # Conectar ao servidor e enviar email
        try:
            with smtplib.SMTP_SSL(self.relay_host, self.relay_port, context=context) as server:
                server.login(self.username, self.password)
                server.sendmail(self.sender_email, dict['email']+self.bcc, message.as_string())
            return {'status':vars.Resultado.SUCESSO}
        except Exception as e:
            return {'status':vars.Resultado.ERRO_DEFAULT,'erro':str(e)}
        
    def __build_email_body(self, dict, edicao, data_publi):
        """
        Constrói o corpo do e-mail em formato HTML com base nas informações fornecidas.

        Args:
            dict (dict): Dicionário contendo informações sobre candidatos.
            edicao (str): Informação sobre a edição do Diário.
            data_publi (str): Data de publicação.

        Returns:
            str: Corpo do e-mail em formato HTML.
        """
        if dict.get('irregular_candidates_tcu', False):
            mensagem_inicial_tcu = '<p>Pessoas citadas neste diário oficial cujo nome consta na lista de irregularidades do TCU (Verificar se trata-se de candidato), link da lista: <a href="https://contasirregulares.tcu.gov.br/ordsext/f?p=105:2:0::NO:RP:P2_MOSTRAR_LISTA:1">Clique aqui</a></p>'

            table_rows_tcu = ""
            for email_info in dict['tcu_list']:
                table_rows_tcu += f"<tr><td>{email_info['Nome']}</td><td>{email_info['CPF']}</td><td>{email_info['UF']}</td><td>{email_info['Município']}</td><td>{email_info['Processo']}</td><td>{email_info['Deliberações']}</td><td>{email_info['Trânsito em julgado']}</td><td>{email_info['Data final']}</td><td>{email_info['Cargo/Função']}</td></tr>"
            html_table_tcu = f"""
                {mensagem_inicial_tcu}
                </p>
                <table border="1" style="border-collapse: collapse;">
                    <tr>
                        <th>Nome</th>
                        <th>CPF</th>
                        <th>UF</th>
                        <th>Município</th>
                        <th>Processo</th>
                        <th>Deliberações</th>
                        <th>Trânsito em julgado</th>
                        <th>Data final</th>
                        <th>Cargo/Função</th>
                    </tr>
                    {table_rows_tcu}
                </table>
                """
        else:
            html_table_tcu = """  # Nenhuma tabela será gerada se o booleano for False
            """
            
        if dict.get('irregular_candidates_tce', False):
            mensagem_inicial_tce = '<p>Pessoas citadas neste diário oficial cujo nome consta na lista de irregularidades do TCE (Verificar se trata-se de candidato), link da lista: <a href="https://www.tce.ce.gov.br/downloads/LISTAIRREGULARES2024TCECE.pdf">Clique aqui</a></p>'

            table_rows_tce = ""
            for email_info in dict['tce_list']:
                table_rows_tce += f"<tr><td>{email_info['Gestor']}</td><td>{email_info['CPF']}</td><td>{email_info['Localidade']}</td><td>{email_info['Processo']}</td><td>{email_info['Especie']}</td><td>{email_info['Transito em Julgado']}</td><td>{email_info['Debito']}</td></tr>"
            html_table_tce = f"""
                {mensagem_inicial_tce}
                </p>
                <table border="1" style="border-collapse: collapse;">
                    <tr>
                        <th>Gestor</th>
                        <th>CPF</th>
                        <th>Localidade</th>
                        <th>Processo</th>
                        <th>Espécie</th>
                        <th>Trânsito em Julgado</th>
                        <th>Débito</th>
                    </tr>
                    {table_rows_tce}
                </table>
                """
        else:
            html_table_tce = """  # Nenhuma tabela será gerada se o booleano for False    
            """
        
        html = f"""
        <html>
        <body>
            <p> Olá,<br>
            </p>
            <p>
                Estamos enviando este e-mail porque acreditamos que a edição {edicao} do Diário do TRE-CE publicada em {data_publi}, contém informações de registro de candidaturas para as eleições de 2024. O trecho que diz respeito à sua zona eleitoral está anexado.
            </p>
            {html_table_tcu}  <!-- Inclui a tabela somente se foi gerada -->
            {html_table_tce}  <!-- Inclui a tabela somente se foi gerada -->
            <p>Em caso de dúvida Técnica: <strong>csti@mpce.mp.br</strong><br>
            Em caso de dúvida Eleitoral: <strong>caopel@mpce.mp.br</strong><br>
            </p>
            <p>Por favor, não responder a este e-mail.<br>
            </p>
        </body>
        </html>
        """ 
        return html