from source.modules.read_project import ReadScripts
from source.modules.vector_search import VetorialSearch

class ExecuterRag:
    def __init__(self):
        self.read_scripts = ReadScripts()
        self.vector_search = VetorialSearch()
    
    def execute(self):
        arq_names, vectors_db, arq_with_content = self.read_scripts.search_scripts()
        
        prompts = []
        
        for i in arq_names:
            query = f"""Monte a doc string do script {i}"""
            script = self.vector_search.buscar(query, vectors_db, arq_with_content)
            prompt = f"""{query} siga o padrão de docString do Google.
                    não faça nem uma alteração do script alem da adição das dock strings.
                    cada classe e função deve ser documentada.\n\n {script}"""
            
            print(prompt)
            prompts.append(prompt)        