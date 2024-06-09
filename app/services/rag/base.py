import logging
from flask import current_app
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


class BaseRAG:
    def __init__(self) -> None:
        self._logger = logger
        self._docs_dir = current_app.config["UPLOAD_FOLDER"]

    @property
    def docs_list(self) -> list:
        loader = DirectoryLoader(self._docs_dir, recursive=True)
        docs_list = loader.load_and_split()

        if not docs_list:
            error_msg = "No valid documents found to update the retriever."
            self._logger.warning(error_msg)
            return []

        self._logger.info(f"Loaded {len(docs_list)} documents from {self._docs_dir}")
        return docs_list

    @property
    def vectorstore(self) -> Chroma:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(self.docs_list)
        return Chroma.from_documents(
            splits, embedding=OpenAIEmbeddings(), persist_directory="."
        )
