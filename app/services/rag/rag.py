import os
from typing import Dict
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.memory import ConversationTokenBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI

from app.services.rag.base import BaseRAG


class RAG(BaseRAG):
    def __init__(self):
        super().__init__()
        self._llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self._chat_history = ConversationTokenBufferMemory(
            llm=ChatOpenAI(), max_token_limit=3097, return_messages=True
        )

    def ask_question(self, question: str) -> Dict[str, str]:
        system_prompt = (
            "You are an assistant that answers questions based on the provided documents. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, say that you don't know. Use three sentences maximum and keep the answer concise."
            "\n\n"
            "{context}"
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(self._llm, prompt)
        rag_chain = create_retrieval_chain(
            self.vectorstore.as_retriever(), question_answer_chain
        )

        results = rag_chain.invoke({"input": question})

        if not results["context"]:
            return {
                "answer": "I don't know. The question is not applicable to the documents provided."
            }

        context_doc = results["context"][0]

        answer = results["answer"]
        paragraph = context_doc.page_content

        filename = os.path.basename(context_doc.metadata["source"].split("#")[0])
        response = {"answer": answer, "paragraph": paragraph, "file": filename}
        self._chat_history.save_context({"input": question}, {"output": answer})

        return response
