# Document-Based Question Answering System

## Overview

This project implements a document-based question-answering system using LangChain and OpenAI. The system allows users
to upload documents and then ask questions about the content of those documents. The system leverages LangChain for
handling document ingestion and vector stores, and OpenAI's GPT-3.5 turbo for generating responses.

## Features

- **Upload Documents:** Users can upload documents in PDF format.
- **Ask Questions:** Users can ask questions related to the uploaded documents.
- **Contextual Answers:** The system provides answers based on the content of the documents.
- **Source Citation:** Each answer includes a link to the relevant document and the specific paragraph where the
  information was found.
- **Task Queue:** Background tasks for document processing and question answering using Celery and Redis.
- **Task Monitoring:** Use Flower to monitor Celery tasks.

## Technology Stack

- **Python:** The core language for the backend.
- **Flask:** Web framework for the API.
- **LangChain:** For handling document loading, splitting, and vector stores.
- **OpenAI:** For generating answers to questions.
- **Celery:** For handling background tasks.
- **Redis:** As a message broker for Celery.
- **Docker:** For containerizing the application.
- **Flower:** For monitoring Celery tasks.
- **ReactJS:** For the frontend UI.

## Challenges

### Queue Implementation

One of the significant challenges of this project was implementing a robust task queue to handle document processing and
question answering. This required:

- **Integrating Celery:** Setting up Celery with Flask and configuring Redis as the message broker.
- **Task Management:** Ensuring tasks were retried in case of failures and handled gracefully.
- **Concurrency:** Managing concurrent task execution to handle multiple document uploads and queries efficiently.

### LangChain Integration

Integrating LangChain posed its own set of challenges:

- **Document Processing:** Loading and splitting large PDF documents into manageable chunks.
- **Vector Store Management:** Storing and retrieving document embeddings efficiently.
- **Retrieval Augmented Generation (RAG):** Combining retrieved document chunks with GPT-4 to generate accurate and
  contextually relevant answers.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Python 3.11
- OpenAI API Key
- Node >= 18

### Installation

1. **Clone the Repository**

```bash
git clone https://github.com/your-repo/document-based-qa.git
cd document-based-qa
```

2. **Set Up Environment Variables**
   Create a **.env** file in the root directory with the following content:
    ```.dotenv
    OPENAI_API_KEY=your_openai_api_key
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0
    UPLOAD_FOLDER=/data/app/data_files
    ```

3. **Build and Run Docker Containers**
    ```bash
    docker-compose up --build
    ```

### API Endpoints

#### Upload Documents

* **URL:** /api/documents

* **Method:** POST

* **Description:** Upload documents to the server.

#### Ask Questions

* **URL:** /api/ask

* **Method:** POST

* **Description:** Ask a question about the uploaded documents.

#### Results

* **URL:** /api/result/<task_id>

* **Method:** GET

* **Description:** This endpoint is used to retrieve the result of a previously submitted task. When a task is submitted
  to the system, it is processed asynchronously. Each task is assigned a unique `task_id` which can be used to query the
  `status` and `result` of the task. The result endpoint allows you to check the completion status of a task and
  retrieve
  its result once it is finished.

#### Download

* **URL:** /api/download/<filename>
* **Method:** GET
* **Description:** This endpoint allows you to download a specific document that was used in the question-answering
  process. The document can be accessed by providing its filename.

### Example Requests

#### Upload Document

```bash
    curl -F "file=@/path/to/your/document.pdf" http://127.0.0.1:5002/api/documents   
```

#### Ask Question

```bash
    curl -X POST -H "Content-Type: application/json" -d '{"question": "What is the main topic of the document?"}' http://127.0.0.1:5002/api/ask  
```

### Development

1. **Activate Virtual Environment**

    ```bash
        python3 -m venv venv  source venv/bin/activate  
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run Flask Application**
    ```bash
    flask run --host=0.0.0.0 --port=5002
    ```

### Monitoring with Flower

Flower is included in the docker-compose configuration to monitor Celery tasks. It can be accessed
at http://127.0.0.1:5555.

### Frontend UI

The frontend UI is built with ReactJS and allows users to interact with the question-answering system.

#### Features

*   **Message Input:** Type messages and send them to the chatbot.
    
*   **File Upload:** Upload documents for the chatbot to process.
    
*   **Message Display:** View responses from the chatbot, including text and document previews.
    

#### Running the UI Locally

To run the ReactJS UI locally:

1.  Accessing repository
  ```bash 
    cd ui
  ```
    
2.  Starting UI
  ```bash
  npm installnpm run dev
  ```
The UI will be accessible at http://localhost:3000.
    

### Accessing the Application

*   **Backend API:** The backend API will be accessible at http://localhost:5002.
    
*   **Frontend UI:** The ReactJS frontend will be accessible at http://localhost:3000.

### Why LangChain and OpenAI?

#### LangChain

LangChain is a powerful library for handling document processing workflows. It provides:

* **Document Loaders:** For loading and splitting documents.

* **Vector Stores:** For storing document embeddings and facilitating similarity searches.

* **Retrievers:** For retrieving relevant document chunks based on a query.

#### OpenAI

OpenAI's GPT-3.5 model provides state-of-the-art language understanding and generation capabilities, which are crucial
for:

* **Natural Language Understanding:** Accurately interpreting user questions.

* **Contextual Answer Generation:** Generating answers based on the content of documents.

* **Flexibility and Power:** Handling a wide range of queries with high accuracy.

Together, LangChain and OpenAI create a robust and scalable system for document-based question answering.
