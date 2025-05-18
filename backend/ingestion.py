# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.vectorstores.utils import filter_complex_metadata
from langchain.embeddings import FastEmbedEmbeddings,FakeEmbeddings
from langchain.retrievers import BM25Retriever,EnsembleRetriever

class Ingestor:

    def __init__(self):
        
        self.retriver=None
        self.keyword_retriver=None
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024,chunk_overlap=100)

    def ingest(self, file_path:str,file_type:str):
        print("File path===============>",file_path)
        print("File type------------------>",file_type)
        if file_type =="pdf":
            docs=PyPDFLoader(file_path=file_path).lazy_load()
            # print("docs================>",docs)
            self.process_data(docs)

    def process_data(self, docs):
        print("Inside process_data function") 
        chunks = self.text_splitter.split_documents(docs)
        self.chunks = filter_complex_metadata(chunks)
        # print(chunks)
        vector_store = Chroma.from_documents(documents=chunks,embedding= FakeEmbeddings(size=1532))

        self.retriver = vector_store.as_retriever()
        # print("retriver==========>",self.retriver.invoke("give me information about vijay"))
        self.keyword_retriver = BM25Retriever.from_documents(self.chunks)
