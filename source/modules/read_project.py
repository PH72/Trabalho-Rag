
from source.utils import vars
from pathlib import Path
from sentence_transformers import SentenceTransformer


class ReadScripts():
    def __init__(self):
        self.path_input = vars.path_input
        self.script_ext = vars.ext_scripts
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def search_scripts(self):
        path = Path(self.path_input)
        arq_with_content = {}  
        arq_with_name = {}
        
        for arq in path.rglob("*"):  
            if arq.suffix in self.script_ext:  
        
                with arq.open(encoding="utf-8") as f:
                    content = f.read()
                
                files_name_vector = f"# Nome do arquivo {arq.name}."
                arq_with_name[str(arq.name)] = files_name_vector
                arq_with_content [str(arq.name)] = content
        
        vectors_db = self.__generate_vector(arq_with_name)
     
        return arq_with_name, vectors_db, arq_with_content
    
    def __generate_vector(self, conteudos):
        
        vector_db = []
        for arq_name, content in conteudos.items():
            vector = self.model.encode(content) 
            vector_db.append((arq_name, vector))
        return vector_db