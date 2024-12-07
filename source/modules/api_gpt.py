import openai
import os

openai.api_key = os.getenv('apikey_chatgpt4')

def chatgpt_query(prompt: str) -> str:
    """
    Função que envia um prompt para a API do ChatGPT e retorna a resposta gerada.

    :param prompt: Texto de entrada para o ChatGPT.
    :return: Resposta gerada pelo modelo GPT-4.
    """
    try:
        # Envia o prompt para a API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Ou "gpt-3.5-turbo" se desejar uma alternativa mais barata
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,  # Ajusta a criatividade das respostas
        )
        # Extrai e retorna a resposta do modelo
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        # Trata erros e retorna uma mensagem amigável
        return f"Erro ao acessar a API: {e}"

# Exemplo de uso
#if __name__ == "__main__":
#    prompt = "Explique como funciona a API do OpenAI em poucas palavras."
#    resposta = chatgpt_query(prompt)
#    print(resposta)
