import os 
from source.utils import vars
from pathlib import Path
from sentence_transformers import SentenceTransformer

class ReadScripts():
    def __init__(self):
        self.path_input = vars.path_input
        self.script_ext = vars.ext_scripts
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def search_scripts(self):
        arq_names = []
        path = Path(self.path_input)
        arq_with_content = {}  
        
        for arq in path.rglob("*"):  
            if arq.suffix in self.script_ext:  
                arq_names.append(arq.name)
                
                with arq.open(encoding="utf-8") as f:
                    content = f.read()
                
                content_with_name = f"# Nome do arquivo {arq.name}\n{content}"

                arq_with_content[str(arq.name)] = content_with_name
                
        
        vectors_db = self.__generate_vector(arq_with_content)
     
        return arq_names, vectors_db, arq_with_content
    
    def __generate_vector(self, conteudos):
        
        vector_db = []
        for arq_name, content in conteudos.items():
            vector = self.model.encode(content) 
            vector_db.append((arq_name, vector))
        return vector_db