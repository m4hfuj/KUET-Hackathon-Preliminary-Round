import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader, TextLoader, DirectoryLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings



class ChatbotRAGFromText:
    def __init__(self, path):
        self.path = path
        self.store = {}

        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not set in environment variables.")

        llm = ChatGroq(groq_api_key=groq_api_key, model_name='Llama3-8b-8192')

        os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        print("...models loading complete...")




        ## Load data
        # loader = TextLoader(self.path)
        # docs = loader.load()

        loader = DirectoryLoader(self.path, glob='*.txt')
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        vector_store = Chroma.from_documents(documents=splits, embedding=embeddings)
        retriever = vector_store.as_retriever()

        print("...data loading complete...")



        ## Prompt Template
        system_prompt = (
            "You are an assistant for question-answering tasks."
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise."
            "\n\n"
            "{context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history "
            "formulate a stand alone question which can be understood "
            "without the chat history. Do not answer the question, "
            "just formulate it if needed and otherwise return it as is."
        )
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        self.rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        print("...ragchain created...")



    def answer(self, message, session_id):
        # print(session_id)

        def get_session_history(session_id) -> BaseChatMessageHistory:
            # print(session_id)
            if session_id not in self.store:
                self.store[session_id] = ChatMessageHistory()
            return self.store[session_id]

        conversation_rag_chain = RunnableWithMessageHistory(
            self.rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        reply = conversation_rag_chain.invoke(
            {"input": f"{message}"},
            config= {
                "configurable": {"session_id": session_id}
            },
        )["answer"]

        return reply

