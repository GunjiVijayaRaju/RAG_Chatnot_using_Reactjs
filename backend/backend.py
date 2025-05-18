from ingestion import Ingestor
from rag import RAGProccessor

class ChatBot:

    def __init__(self):
        self.ingestor = Ingestor()
        self.rag_processor = RAGProccessor(self.ingestor)

    def ask(self, query:str):
        print("User question in ask function",query)
        res = self.rag_processor.process(query)
        print("Result===========>",res)
        
        if hasattr(res, "content"):
            return res.content
        else:
            return res 