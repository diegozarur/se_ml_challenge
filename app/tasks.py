from celery import shared_task
import logging

from app.services.rag import RAG

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def ask_question(self, question: str):
    logger.info(f"Task start: ask_question: {question}")
    try:
        rag = RAG()
        response = rag.ask_question(question)
        return response
    except Exception as e:
        logger.error(f"Error in task ask_question: {e}")
        raise self.retry(exc=e, countdown=60, max_retries=3)
    finally:
        logger.info("Task end: ask_question")
