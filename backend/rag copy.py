from langchain.load import dumps, loads
from operator import itemgetter
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.schema.output_parser import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.retrievers import BM25Retriever,EnsembleRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_models import ChatLiteLLM
import os

os.environ["GEMINI_API_KEY"]="AIzaSyBpB-NLQ50R0ftU9B-cNVEPzS0pY96OtMY"

# llm = ChatLiteLLM(model="gemini/gemini-1.5-flash")

# groq_api_key = "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"
# # llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")


class RAGProccessor:

    def __init__(self, ingestor):
        self.ingestor = ingestor
        self.context_token_limit = 3000

    def process(self, query):
        print("user question in process function in rag",query)
        # self.model =ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192") 
        self.model =ChatLiteLLM(model="gemini/gemini-1.5-flash")
        session_id="124322111123376"
        retriever = self.ingestor.retriver
        # print("retriver------------>",retriever.invoke(query))

        if retriever==None:
            Prompt_template=""""
                        You are a friendly AI, answering questions that you know based on the context if you know:              
            Current conversation: {history}
            Human: {input}
            AI:
            """ 
            PROMPT = PromptTemplate(input_variables=["history","input"], template=Prompt_template)
            # print("Prompt template------------>",PROMPT)   
            response =({"input":itemgetter("input"),"history":itemgetter("history")}
                    |PROMPT
                    |self.model
                    |StrOutputParser())
            # print("response chain------------>",response)
            chain_with_history = RunnableWithMessageHistory(
                response,
                lambda session_id:SQLChatMessageHistory(
                    session_id=session_id,
                    connection_string="sqlite:///sqlite.db"),
                input_messages_key ="input",
                history_messages_key="history", 
            )
            # def get_session_history(session_id) -> BaseChatMessageHistory:

            #     return ChatMessageHistoryTrubcated(
            #         session_id =session_id,
            #         connection_string="sqlite:///sqlite.db"),
            #         truncate_at_token=3200,
            #         language_model=self.model,
            #     )

            # chain_with_history = RunnableWithMessageHistory(
            #     response,
            #     get_session_history,
            #     input_messages_key="input"
            #     history_messages_key="history",
            # )

            config = {"configurable":{"session_id": session_id}}
            # print("config=========>",config)
            # print("chain_with_history========>",chain_with_history)
            res = chain_with_history.invoke({"input":query}, config=config)
            # res = response.invoke({"input":query})
            # memory = ConversationBufferMemory(memory_key="history")
            # chain = ConversationChain(llm=self.model, memory=memory, verbose=True)
            # res = chain.predict(input=query)

            return res
        else:
            print("====================under rag==================")
            keyword_retriever = self.ingestor.keyword_retriver

            if keyword_retriever != None:
                print("-----------inside Keyword retriver--------------")
                keyword_retriever.k = 3
            # if retriever !=None:
            #     retriever.k = 3
        
            # ensemble_retriever = EnsembleRetriever(retrievers=[retriever,keyword_retriever],weights=[0.5,0.5])

            # print("Ensemble retriver ============>",ensemble_retriever.invoke(query))
              
            # template ="""You are an AI language model assistant. Your task is to generate five different versions of the given user question to retrieve relevant documents from a vector database. By generating multiple perspectives on the user question, your goal is to help the user overcome some of the limitations of the distance-based similarity search. Provide these alternative questions separated by newlines. Original question: {input}
            #         """ 

            # # prompt_perspectives = ChatPromptTemplate.from_messages(
            # #     [
            # #         ("system",template),
            # #         MessagesPlaceholder("chat_history"),
            # #         ("human","{question}"),
            # #     ]
            # # )
            # prompt_perspectives = ChatPromptTemplate.from_template(template)

            # generate_queries = (
            #     prompt_perspectives
            #     | self.model
            #     | StrOutputParser()
            #     | (lambda x: x.split("\n"))
            # )

            # print("multi queries=========================>",generate_queries.invoke(query))

            # Prompt_template_2 =""""
            #             You are a friendly AI, answering questions that you know based on the context if you know: {context}             
            # Chat history: {history}
            # Question: {input}
            # Helpful Answer:
            # """ 
            # prompt_1 = ChatPromptTemplate.from_template(Prompt_template_2)

            # # code_chain =(
            # #     {"context":itemgetter("input")| generate_queries| ensemble_retriever, "input": itemgetter("input"), "history":itemgetter("history")}
            # #     | prompt
            # #     | self.model
            # #     |StrOutputParser()
            # # )
            # retriever_chain = RunnablePassthrough.assign(context = generate_queries| ensemble_retriever.map())
            
            # # print("Retriveal chain response===========>",retriever_chain.invoke(query))
            
            # rag_chain = retriever_chain | prompt_1 | self.model | StrOutputParser()

            # chain_with_history = RunnableWithMessageHistory(
            #     rag_chain,
            #     lambda session_id:SQLChatMessageHistory(
            #         session_id=session_id,
            #         connection_string="sqlite:///sqlite.db"),
            #     input_messages_key ="input",
            #     history_messages_key="history", 
            # )

            # config = {"configurable":{"session_id": session_id}}
            # res = chain_with_history.invoke({"input":query} , config=config)
            # print("result -------------------------->",res)
            # return res
            ensemble_retriever = EnsembleRetriever(retrievers=[retriever,keyword_retriever],weights=[0.5,0.5])

            print("Ensemble retriver ============>",ensemble_retriever.invoke(query))
                
            template ="""You are an AI language model assistant. Your task is to generate five different versions of the given user question to retrieve relevant documents from a vector database. By generating multiple perspectives on the user question, your goal is to help the user overcome some of the limitations of the distance-based similarity search. Provide these alternative questions separated by newlines. Original question: {input}
                    """ 

            # prompt_perspectives = ChatPromptTemplate.from_messages(
            #     [
            #         ("system",template),
            #         MessagesPlaceholder("chat_history"),
            #         ("human","{question}"),
            #     ]
            # )
            prompt_perspectives = ChatPromptTemplate.from_template(template)

            generate_queries = (
                prompt_perspectives
                | self.model
                | StrOutputParser()
                | (lambda x: x.split("\n"))
            )


            print("multi queries=========================>",generate_queries.invoke(query))

            Prompt_template_2 =""""
                        You are a friendly AI, answering questions that you know based on the context if you know: {context}             
            Chat history: {history}
            Question: {input}
            Helpful Answer:
            """ 
            prompt_1 = ChatPromptTemplate.from_template(Prompt_template_2)

            # code_chain =(
            #     {"context":itemgetter("input")| generate_queries| ensemble_retriever, "input": itemgetter("input"), "history":itemgetter("history")}
            #     | prompt
            #     | self.model
            #     |StrOutputParser()
            # )
            retriever_chain = RunnablePassthrough.assign(context = generate_queries | ensemble_retriever.map())  # ❌ Incorrect

            print("Retrieval chain response===========>", retriever_chain.invoke({"input": query}))

            rag_chain = retriever_chain | prompt_1 | self.model | StrOutputParser()


            print("Rag chain response=========>",rag_chain.invoke({"input":query , "history":" "}))

            chain_with_history = RunnableWithMessageHistory(
                rag_chain,
                lambda session_id:SQLChatMessageHistory(
                    session_id=session_id,
                    connection_string="sqlite:///sqlite.db"),
                input_messages_key ="input",
                history_messages_key="history", 
            )

            config = {"configurable":{"session_id": session_id}}
            
            res = chain_with_history.invoke({"input":query}, config=config)
            print("result -------------------------->",res)

            return res
        
    
    # def reciprocal_rank_fusion(self, results: list[list], k=60):

    #     fused_scores = {}

    #     for docs in results:
    #         for rank, doc in enumerate(docs):
    #             doc_str = dumps(doc)
    #             if doc_str not in fused_scores:
    #                 fused_scores[doc_str]=0
                
    #             fused_scores[doc_str] += 1 / (rank + k)

    #     reranked_results = [
    #     (loads(doc), score) 
    #     for doc, score in sorted( 
    #         fused_scores.items(), key=lambda x: x[1], reverse=True 
    #         )
    #     ]    

    #     return reranked_results
    
    def filter_documents_by_token_limit(self, documents):
        print("inside filter function")
        self.model =ChatLiteLLM(model="gemini/gemini-1.5-flash")
        max_tokens = self.context_token_limit
        filtered_docs = []
        total_tokens = 0

        for doc in documents:
            tokens = self.model.get_num_tokens(doc[0].page_content)
            token_count = tokens

            if total_tokens + token_count<=max_tokens:
                filtered_docs.append(doc)
                total_tokens += token_count
            else:
                break

        return filtered_docs 