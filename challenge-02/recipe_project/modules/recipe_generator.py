import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader, TextLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# import bs4

# from langchain.chains import create_history_aware_retriever
# from langchain_core.prompts import MessagesPlaceholder

# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.chat_history import BaseChatMessageHistory
# from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings



class RecipeGeneratorFromText():

    def __init__(self, path):
        self.path = path
        self.store = {}

        groq_api_key = os.getenv("GROQ_API_KEY")
        os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not set in environment variables.")
        llm = ChatGroq(groq_api_key=groq_api_key, model_name='Llama3-8b-8192')
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        ## Load data
        print(f"...reading text from {path}...")
        loader = TextLoader(path)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        vector_store = Chroma.from_documents(documents=splits, embedding=embeddings)
        retriever = vector_store.as_retriever()

        ## Prompt Template
        system_prompt = (
            "You are an assistant for generating recipe "
            "Yo are given available ingredient data and recipes"
            "The avalable ingerdients consists of name of the food item, available quanitity and unit "
            "\nAvailable ingredients"
            "{ingredients}\n\n"
            "Use the following pieces of retrieved context with many recipes "
            "Make it consise "
            "\n\n {context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages([("system", system_prompt),("human", "{ingredients}"),])

        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        self.chain = create_retrieval_chain(retriever, question_answer_chain)


    def _textify_dictionary(self, ingredients):
        text = ""
        for item in ingredients:
            text += f"{item['name']}: {item['quantity']} {item['unit']}\n"
        return text


    def generate_recipe(self, ingredients):
        print("...generating recipe...")
        ingredients = self._textify_dictionary(ingredients)
        quiz = self.chain.invoke({"input": "", "ingredients": ingredients})['answer']
        # return "\n".join(quiz.split("\n")[1:])

        quiz_lines = quiz.split("\n")

        questions = []
        answers = []
        for line in quiz_lines:
            if line.strip().lower().startswith("answer"):
                answers.append(line.strip())
            else:
                questions.append(line.strip())

        return "\n".join(questions), "\n".join(answers)

