import numpy as np
from sentence_transformers import SentenceTransformer

class VetorialSearch:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Modelo para gerar vetores

    def calcular_similaridade(self, vetor1, vetor2):
        """
        Calcula a similaridade cosenoidal entre dois vetores.
        """
        return np.dot(vetor1, vetor2) / (np.linalg.norm(vetor1) * np.linalg.norm(vetor2))

    def buscar(self, query, vector_db, arq_witch_content, top_k=1):
        """
        Busca no banco de dados vetorial os itens mais similares à consulta.
        :param query: String da consulta.
        :param top_k: Número de resultados mais similares a retornar.
        :return: Lista de tuplas (nome_arquivo, similaridade).
        """
        # Gera o vetor da consulta
        query_vector = self.model.encode(query)

        # Calcula similaridade entre a consulta e cada vetor do banco
        resultados = []
        for nome_arquivo, vetor in vector_db:
            similaridade = self.calcular_similaridade(query_vector, vetor)
            resultados.append((nome_arquivo, similaridade))

        # Ordena por similaridade (descendente) e retorna os top_k
        resultado = sorted(resultados, key=lambda x: x[1], reverse=True)

        
        return arq_witch_content.get(resultado[0][0], "")