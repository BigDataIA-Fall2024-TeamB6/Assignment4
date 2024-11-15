# Assignment4
## Agent-Based Research Tool: Automating Document Analysis and Knowledge Retrieval
An interactive, agent-based research application built using FastAPI, Coagents, and Langraph to analyze and explore publications. The application parses document contents—including text, tables, images, and graphs—using Docling and stores structured data as vector embeddings in Pinecone for scalable similarity search. Users can interactively explore selected documents, query research insights, and retrieve responses leveraging multi-agent capabilities such as Arxiv search, web search, and Retrieval-Augmented Generation (RAG).

The tool enables robust Q/A functionality, real-time document selection, and multi-step workflows for comprehensive research. It supports professional reporting by exporting results to templated PDF files and structured Codelabs documentation, enhancing usability and facilitating knowledge discovery. This end-to-end system empowers researchers with an automated, efficient, and interactive solution for document-based research and analysis.


## Live Application Link
- Streamlit application link: http://18.219.124.78:8501/
- FastAPI: http://18.219.124.78:8000/health

## Codelabs Link
Codelabs documentation link: https://codelabs-preview.appspot.com/?file_id=1qFJkJYuKjS6lhUt_rgpfV4QB3Ic7YJtiIAI4vZ_7vW0#1
## **Video of Submission**
Demo Link in Codelabs Document 



## Attestation and Team Contribution
**WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK**

Name | NUID | Contribution% | Work_Contributed
--- | --- | --- | --- |
Sandeep Suresh Kumar | 002841297 | 33% | 
Deepthi Nasika       | 002474582 | 33% | 
Gomathy Selvamuthiah | 002410534 | 33% | 
Ramy Solanki         | 002816593 | 33% | 

## Problem Statement
This project aims to address these challenges by creating an agent-based research tool that leverages Retrieval-Augmented Generation (RAG) and multi-agent systems to enable users to interact seamlessly with document content. By incorporating advanced technologies like Langraph and Pinecone, the application simplifies research processes and empowers users to derive accurate, context-aware insights.

The application primarily focuses on:

1. Content Parsing and Vector Storage: Parse document contents, including text, tables, images, and graphs, using Docling and store vectorized embeddings in Pinecone for scalable similarity search.
2. Automated Workflow with Airflow: Automate document parsing, embedding generation, and vector storage through a robust Airflow pipeline.
3. Multi-Agent System for Research: Enable document exploration, Arxiv-based paper searches, web-based contextual searches, and Q&A functionality using Langraph’s multi-agent capabilities.
4. Interactive User Interface: Provide a user-friendly interface with Coagents or Streamlit for document selection, querying, and real-time interaction.
5. Comprehensive Reports: Generate professional reports in PDF and Codelabs formats containing responses, images, and graphs relevant to user queries.
6. Efficient Workflow Management: Validate and store research notes, enabling incremental indexing and efficient future searches.



## Architecture Diagram
### 1. Core Application Pipeline
![Architecture Diagram]()



### 2. Airflow Pipeline
![Architecture Diagram](airflow_pipeline.png](https://github.com/BigDataIA-Fall2024-TeamB6/Assignment4/blob/diagram/airflow_pipeline.png)



## Project Goals
### Airflow Pipeline
#### 1. Objective
- Streamlined the process of parsing and extracting contents from documents, including text, tables, images, and graphs.
- Automated the document ingestion process by integrating Docling for parsing and Pinecone for storing vectorized embeddings of document contents.

#### 2. Tools
- Extraction of data from publications website - BeautifulSoup
- Database - Snowflake Database
- File storage - Amazon S3 (Simple Storage Service)
- Data Automation - Airflow
- 
#### 3. Output
- Extracted and structured document from S3 contents are stored as embeddings in Pinecone for efficient retrieval.
- Extracted textual data which are the details of the publication like title, brief summary, cover image url, pdf url are stored into table publications_info. Users information is being recorded in users table. All the responses to user queries are recorded in research_notes table. All the tables are stored in Snowflake Database

### Agent-Based Research System
#### 1. Objective
Create a multi-agent system using Langraph to enhance document-based research and interactive query resolution.
Implement various agents, including:
- Document Selection Agent: Enable users to select and explore only processed documents.
- Arxiv Agent: Retrieve related academic research papers.
- Web Search Agent: Fetch supplementary data from the internet for broader context.
- RAG (Retrieval-Augmented Generation) Agent: Enable Q/A functionality by combining Pinecone-stored embeddings and LLM capabilities.

#### 2. Tools
- Vector Storage: Pinecone for similarity search.
- Agents: Langraph for implementing multi-agent research workflows.
- LLM Integration: OpenAI API for generating context-aware responses to queries.

#### 3. Output
- Users can select documents, ask questions, and retrieve contextual answers with relevant text, tables, images, and graphs.
- Multi-agent capabilities enable comprehensive research with data from documents, Arxiv, and online searches.
- Responses are stored alongside user queries in a database for future reference and research continuity.

### FastAPI
#### 1. Objective
- Act as the backend service to integrate Pinecone, Langraph agents, and the user interface.
- Provide endpoints for document exploration, querying, and research interaction.
- Implement secure user authentication and data management protocols.

#### 2. Tools
- `fastapi[standard]` for building a standard FastAPI application *
- `python-multipart` for installing additional dependencies for the FastAPI application
- `snowflake-connector-python` for interacting with the Snowflake database
- `PyJWT` for authenticating and authorizing users with JSON Web Tokens (JWT)
- `openai` for prompting OpenAI's GPT-4o model to get LLM Response
- `tiktoken` for disintegrating prompts into tokens of known sizes
- `PyPDF2` for extracting text from the pdf files
- `langchain` for RAG implementation
- `unstructured[all-docs]` for text and image extraction from PDFs
- `cleanlab-studio` for generating trustworthy score

#### 3. Output
FastAPI provides a number of endpoints for interacting with the service:
- `GET` - `/health` - To check if the FastAPI application is setup and running
- `POST` - `/register` - To sign up new users to the service
- `POST` - `/login` - To sign in existing users
- `GET` - `/exploredocs` - *Protected* - To fetch 'x' number of documents from the database
- `GET` - `/load_docs/{document_id}` - *Protected* - To load publications information like title, brief summary, cover image url from the database
- `GET` - `/summary/{document_id}` - *Protected* - To generate on the fly summary of the document using NVIDIA services
- `POST` - `/chatbot/{document_id}` - *Protected* - Q/A interface for user to interact with the selected document

FastAPI ensures that every response is returned in a consistent JSON format with HTTP status, type (data type of the response content) message (response content), and additional fields if needed


### Coagents
#### 1. Objective
- Provide a user-friendly interface for document exploration, querying, and interactive research sessions.
- Allow users to ask detailed questions, generate summaries, and interact with selected documents.

#### 2. Tools
- Coagents (web application framework), Requests (API calls for data retrieval)

#### 3. Output
- Interactive Q/A functionality enables users to query documents and retrieve structured answers.
- Generated reports containing user queries, responses, images, and graphs are exportable in PDF and Codelabs formats.
- A seamless user experience that integrates multiple agents and backend functionalities.

### Deployment
- Containerization of FastAPI and Streamlit applications using Docker
- Deployment to a public cloud platform using Docker Compose
- Ensuring public accessibility of the deployed applications - coagents and FastAPI
- Providing clear instructions for users to interact with the RAG application and explore its functionalities
- The FastAPI and Streamlit are containerized using Docker, orchestrated through Docker compose, and the Docker images are pushed to Docker Hub. For deploying the Docker containers, we use an Amazon Web Services (AWS) EC2 instance within the t3-medium tier


## Data Source
1. CFA Institute Research Foundation Publications: https://rpc.cfainstitute.org/en/research-foundation/publications#sort=%40officialz32xdate%20descending&f:SeriesContent=%5BResearch%20Foundation%5D

## Amazon S3 Link
- s3://publications-info/{document_id}


## Technologies
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-FFD43B?style=for-the-badge&logo=python&logoColor=white)](https://www.crummy.com/software/BeautifulSoup/)
[![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![Amazon S3](https://img.shields.io/badge/Amazon%20S3-569A31?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/s3/)
[![Snowflake](https://img.shields.io/badge/Snowflake-29B1E5?style=for-the-badge&logo=snowflake&logoColor=white)](https://www.snowflake.com/)
[![Airflow](https://img.shields.io/badge/Airflow-17B3A8?style=for-the-badge&logo=apacheairflow&logoColor=white)](https://airflow.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)](https://www.postman.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-5A67D8?style=for-the-badge)](https://www.langchain.com/)
[![Cleanlab](https://img.shields.io/badge/Cleanlab-000000?style=for-the-badge&logo=cleanlab&logoColor=white)](https://cleanlab.ai/)
[![OpenAI](https://img.shields.io/badge/OpenAI-000000?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)

## Prerequisites
Software Installations required for the project
1. Python Environment
A Python environment allows you to create isolated spaces for your Python projects, managing dependencies and versions separately

2. Poetry Environment/ Python Virtual Environment
- Poetry is a dependency management tool that helps you manage your Python packages and projects efficiently where a user can install all the dependencies onto pyproject.toml file
- Python Virtual Environment helps you manage your Python packages efficiently where a user can include all the dependencies in requirements.txt file

4. Packages
```bash
pip install -r requirements.txt
```

4. Visual Studio Code
An integrated development environment (IDE) that provides tools and features for coding, debugging, and version control.

5. Docker
 Docker allows you to package applications and their dependencies into containers, ensuring consistent environments across different platforms. All the dependencies will be installed on docker-compose.yaml file with env file

6. Amazon S3 Bucket
Amazon S3 (Simple Storage Service) is a cloud storage solution from AWS used to store files and objects. It provides scalable, secure, and cost-effective storage for all extracted publication files, including images, PDFs, and JSON data, organized under unique document IDs. This bucket serves as the primary cloud storage for file data accessible by the application.

8. Coagents
Coagents is an advanced framework designed for building interactive, agent-driven applications. It enables the integration of multiple AI agents working collaboratively to provide dynamic, context-aware user experiences. With Coagents, developers can create conversational interfaces and workflows tailored for complex research and analysis tasks, leveraging the power of multi-agent systems for seamless interaction.

9. Snowflake Database
Snowflake is a cloud-based data warehousing and analytics service that supports structured data storage. This project uses Snowflake to store extracted textual data, such as titles, summaries, cover image URLs, and PDF URLs from CFA publications. Snowflake also hosts user data and stores responses to user queries, enabling efficient querying and data retrieval.

10. Pinecone Vector Database
Pinecone is a cloud-native vector database used for storing embeddings of parsed document content, such as text chunks, tables, images, and graphs, in your research tool. It enables efficient similarity search by comparing user query embeddings with stored document embeddings using cosine similarity.


## Project Structure
```
Assignment3/
├── airflow
│   ├── Dockerfile
│   ├── POC
│   │   ├── MultiModalRAG.ipynb
│   │   ├── Stage1.ipynb
│   │   ├── Stage2.ipynb
│   │   ├── Stage3.py
│   │   └── stage1.csv
│   ├── chromedriver
│   │   ├── LICENSE.chromedriver
│   │   ├── THIRD_PARTY_NOTICES.chromedriver
│   │   └── chromedriver.exe
│   ├── dags
│   │   └── airflow_pipeline.py
│   ├── docker-compose.yaml
│   ├── rag_pipeline.py
│   ├── requirements.txt
│   ├── scraper.py
│   ├── snowflakeDB.py
│   ├── upload_to_S3.py
│   └── webscrape.py
├── diagram
│   ├── AirflowPipeline.py
│   ├── airflow_pipeline.png
│   ├── core_app_architecture.py
│   ├── core_application_pipeline.png
│   └── images
│       ├── Chroma.png
│       ├── Download.png
│       ├── InMemoryStore.png
│       ├── Langchain.png
│       ├── MultiVectorRetriever.png
│       ├── Nvidia-Logo.png
│       ├── Nvidia.png
│       ├── OpenAI.png
│       ├── PDF_documents.png
│       ├── PNG.png
│       ├── Question.png
│       ├── Snowflake.png
│       ├── Streamlit.png
│       ├── Text.png
│       ├── Unstructured.png
│       ├── cfa-institute.png
│       └── cleanlabs.png
├── docker-compose.yml
├── fastapi
│   ├── Dockerfile
│   ├── connectDB.py
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   ├── routers.py
│   └── services.py
└── streamlit
    ├── Dockerfile
    ├── app.py
    ├── documentexplorer.py
    ├── homepage.py
    ├── loginpage.py
    ├── overview.py
    ├── qainterface.py
    ├── registerpage.py
    ├── requirements.txt
    └── summary.py

```

## How to run the application locally
1. **Clone the Repository**: Clone the repository onto your local machine and navigate to the directory within your terminal.

   ```bash
   git clone https://github.com/BigDataIA-Fall2024-TeamB6/Assignment3
   ```

2. **Install Docker**: Install docker and `docker compose` to run the application:

   - For Windows, Mac OS, simply download and install Docker Desktop from the official website to install docker and `docker compose` 
   [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

   - For Linux (Ubuntu based distributions), 
   ```bash
   # Add Docker's official GPG key:
   sudo apt-get update
   sudo apt-get install ca-certificates curl
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc

   # Add the repository to Apt sources:
   echo \
   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
   $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt-get update 

   # Install packages for Docker
   sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

   # Check to see if docker is running 
   sudo docker run hello-world

3. **Run the application:** In the terminal within the directory, run 
   ```bash
   docker-compose up

   # To run with logging disabled, 
   docker-compose up -d

4. In the browser, 
   - visit `localhost:8501` to view the Streamlit application
   - visit `localhost:8000/docs` to view the FastAPI endpoint docs
