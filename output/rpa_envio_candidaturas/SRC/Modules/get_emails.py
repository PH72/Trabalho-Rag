import Config.vars as vars
import requests
import json
from dotenv import load_dotenv
import os


class GetSydle:
    """
    Classe para obter informações de unidades organizacionais e membros de equipe a partir da API Sydle.
    """

    def __init__(self) -> None:
        """
        Inicializa a classe GetSydle com a URL da API e os cabeçalhos necessários.
        """
        self.url = "https://mpce.sydle.one/api/1/main/"
        self.resource_organization_unit = "com.sydle.hr/OrganizationUnit/_search"
        self.resource_staff_member = "com.sydle.hr/StaffMember/_search"
        self.resource_pearson = "crm/person/_search"
        
        self.headers = {
            'X-Explorer-Account-Token': 'mpce',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJjdHkiOiJKV1QiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..-owSNv1lzl05K1ywOu4IfA.4gYIQk7I6D7Xrb2380wUT3aF5IYet2N-9MTRpo1l3y2EHdDqvMlD3sfSkbXa7hW1tk9R_hKizR636LWrp8iIW9AHKWENelNi8MVZEn388x2g0Cuc6A9wf-JGkgHjugXXetOkFv7ohKP6sMRBR2Za3FdvMm0wtSSzHBCfW3VfYKQzKurLhWcs0mpRb3LjWYypEx3TtPsdfSekPRCpMkMqgzowLvsxykFBtgCGsda869yAjh_jiJFfe8nXwcIJec60BYu1NcYFmQ06dgNip3Q54vgdTfPq7qRREETeoJaBc7vAWVxQ2oao9GYc9Xb6N5uqCGNiQdJqOlJ5dUBX0EIMDvY6Nc37g278ZNnH2JBCD5njNUQX06EOBkrWpi9tmUGdJs1NcIIKMXqpcJAuRGX4eB-p3BJ80hQ8s-fvmlk7WygJwc5a4GsShWflJW8qUKZGXzVJiv71H6ZxlJ6dFrpvjHOfTkN5mAHo8hxhcq5Rsnrm0doeiHTjW3jsLBjFB3DFq8m45nHg2_GlK9_ShzCy27kXmfd8rMAacuIyxFtP24s4xSw1ypM4KYTc96OUZj16N8vEHOQOtnJ-iFKzzDiohjyscT2YDdbu4Qilnck2QUc.FaxbbMgVY2DQzD7r9TajlQ'
        }
        
    def execute(self, zonas):
        """
        Executa a busca de e-mails para as zonas fornecidas.
        
        Args:
            zonas (list): Lista de dicionários contendo informações sobre as zonas.

        Returns:
            dict: Dicionário com o status da operação e a lista de zonas atualizada com os e-mails.
        """
        try:
            for zona in zonas:
                mails = []
                zona_abv = zona['filename'][:4] + ' ZE'
                id_staffmember, mail_organization = self.__search_organization_unit(zona_abv)
                
                if mail_organization is not None:
                    mails.append(mail_organization)
                
                if id_staffmember == '' or id_staffmember is None:
                    zona['email'] = mails
                    continue
            
                id_person = self.__search_staffmember(id_staffmember)
                email = self.__search_pearson(id_person)
                
                mails.append(email)
                
                zona['email'] = mails
            
            return {'status': vars.Resultado.SUCESSO, 'zonas': zonas}
        
        except Exception as e:
            return {'status': vars.Resultado.ERRO_DEFAULT, 'erro': str(e)}
        
    def __search_pearson(self, id_pearson):
        """
        Busca o e-mail de uma pessoa com base no seu ID na API Pearson.
        
        Args:
            id_pearson (str): ID da pessoa a ser buscada.

        Returns:
            str: O e-mail da pessoa.

        Raises:
            Exception: Se ocorrer um erro ao fazer a requisição à API.
        """
        url = self.url + self.resource_pearson
        payload = vars.elastic_id(id_pearson)

        try:
            response = requests.post(url, headers=self.headers, data=payload)
            response.raise_for_status()  # Levanta um HTTPError para respostas ruins

            data = response.json()  # Usa response.json() em vez de json.loads(response.text)
            hits = data.get('hits', {}).get('hits', [])

            if not hits:
                raise ValueError("Nenhum resultado encontrado na resposta")

            return hits[0]['_source']['email']

        except requests.exceptions.RequestException as e:
            raise Exception(vars.Resultado.ERRO_API_POST) from e
        except (KeyError, IndexError, ValueError) as e:
            raise Exception(vars.Resultado.ERRO_API_POST) from e
        
    def __search_staffmember(self, id_staff_member):
        """
        Busca o ID da pessoa com base no ID do membro da equipe na API.
        
        Args:
            id_staff_member (str): ID do membro da equipe a ser buscado.

        Returns:
            str: O ID da pessoa.

        Raises:
            Exception: Se ocorrer um erro ao fazer a requisição à API.
        """
        try:
            url = self.url + self.resource_staff_member
            payload = vars.elastic_id(id_staff_member)
            response = requests.request("POST", url, headers=self.headers, data=payload)
            data = json.loads(response.text)

            return data['hits']['hits'][0]['_source']['person']['_id']
        
        except requests.exceptions.RequestException as e:
            raise Exception(vars.Resultado.ERRO_API_POST) from e
        except (KeyError, IndexError, ValueError) as e:
            raise Exception(vars.Resultado.ERRO_API_POST) from e
            
    def __search_organization_unit(self, zona):
        """
        Busca informações sobre a unidade organizacional com base na zona fornecida.
        
        Args:
            zona (str): A zona a ser buscada.

        Returns:
            tuple: Uma tupla contendo o ID do membro da equipe responsável e o e-mail da unidade organizacional.

        Raises:
            Exception: Se ocorrer um erro ao fazer a requisição à API.
        """
        try:
            url = self.url + self.resource_organization_unit
            payload = vars.elastic_organization_unit(zona)
            response = requests.request("POST", url, headers=self.headers, data=payload)
            data = json.loads(response.text)
            
            email_unidade = data['hits']['hits'][0]['_source']['additionalData']['detalhamentoDeLocal']['email']
            
            if data['hits']['hits'][0]['_source']['responsavelPelaUnidade'] is None:
                id_stafmenber = None
            
            else:
                id_stafmenber = data['hits']['hits'][0]['_source']['responsavelPelaUnidade']['_id']
                          
            return id_stafmenber, email_unidade
        
        except requests.exceptions.RequestException as e:
            raise Exception(vars.Resultado.ERRO_API_POST) from e
        except (KeyError, IndexError, ValueError) as e:
            raise Exception(vars.Resultado.ERRO_API_POST) from e