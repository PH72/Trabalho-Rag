from source.modules.read_project import ReadScripts
from source.modules.write_project import WriteScripts
from source.modules.vector_search import VetorialSearch
from source.modules.api_gpt import chatgpt_query
import json

class ExecuterRag:
    def __init__(self):
        self.read_scripts = ReadScripts()
        self.write_scripts = WriteScripts()
        self.vector_search = VetorialSearch()
    
    def execute(self):
        arq_names, vectors_db, arq_with_content = self.read_scripts.search_scripts()
        
        prompts = []
        
        for i in arq_names:
            query = f"""Nome do arquivo {i}."""
            script = self.vector_search.buscar(query, vectors_db, arq_with_content)
            prompt = f"""1 You are an API with the function of receiving a script and returning the same code documented following the Google docstring standard.
                         2 Do not make any changes to the script other than adding the docstrings.
                         3 Do not return any information other than the documented code.
                         4 The response must be a JSON containing a single element called codigo_documentado, and its value must be the code with the documentation. The response must be just the JSON and nothing more. Do not add anything before or after the braces.
                         5 Each class and function must be documented.
                         6 The response must not contain any word outside the JSON.
                         7 The code is provided below.
                         8 Documentation must always be written in Portuguese.
                    \n\n {script}"""
            
            #print(prompt)
            prompts.append({'prompt' : prompt, 'arq_name':i})
        

        scripts_doc = []
        for prompt in prompts:
            resposta = chatgpt_query(prompt['prompt'])
            if "json\n{\n" in resposta:
                resposta.replace('json','',1)  
            
            script_doc = json.loads(resposta)
            print(prompt['arq_name'])
            
            scripts_doc.append({'script':script_doc['codigo_documentado'],'arq_name':prompt['arq_name']})
    
        print(scripts_doc)
        
        self.write_scripts.create_project()
        for script_doc in scripts_doc:
            self.write_scripts.geretare_project(script_doc)