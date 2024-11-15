import os
import logging
from dotenv import load_dotenv
from llama_index import PromptHelper, SimpleKeywordTableIndex, ServiceContext
from llama_index.llms import OpenAI
from llama_index.prompts.prompts import PromptTemplate
from llama_index.tools import Tool
from fastapi import status
from fastapi.responses import JSONResponse
import requests
from xml.etree import ElementTree

# Load environment variables from a .env file
load_dotenv()

# Configure logging to track application behavior and errors
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set logging level to INFO for detailed logs
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("llamaindex_services.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Initialize the OpenAI LLM and LlamaIndex ServiceContext
api_key = os.getenv("OPENAI_API_KEY")  # Get the OpenAI API key from environment variables
if not api_key:
    raise ValueError("Missing OPENAI_API_KEY in environment variables.")
llm = OpenAI(api_key=api_key, model="gpt-4")  # Use GPT-4 for LlamaIndex prompts
service_context = ServiceContext.from_defaults(llm=llm)  # Create a default ServiceContext




# Tool: Explore documents
@Tool(name="explore_documents", description="Fetches a list of documents from the indexed data.")
def explore_documents(prompt_count: int):
    """
    Fetches a list of documents based on predefined document IDs.

    Args:
        prompt_count (int): Number of prompts to include in the response.

    Returns:
        JSONResponse: A response with a list of documents or an error message.
    """
    logger.info("LlamaIndex - explore_documents() - Retrieving list of documents.")

    try:
        # Predefined list of document IDs
        document_ids = ['68db7e4f057f494fb5b939ba258cefcd', 
                        '97b6383e18bb48d1b7daceb27ad0a198', 
                        '52af53cc2f5e42558253aa572a55b78a']

        # Fetch documents from the index
        results = []
        for doc_id in document_ids:
            # Perform a keyword-based search on the index
            query_results = index.query(doc_id)
            for result in query_results:
                extra_info = result.extra_info
                results.append({
                    "document_id": extra_info["document_id"],
                    "title": extra_info["title"],
                    "image_url": extra_info["image_url"]
                })

        if not results:
            logger.info("LlamaIndex - explore_documents() - No documents found.")
            return JSONResponse({
                'status': status.HTTP_404_NOT_FOUND,
                'type': "string",
                'message': "No documents were found."
            })

        logger.info(f"LlamaIndex - explore_documents() - Retrieved documents: {results}")
        return JSONResponse({
            'status': status.HTTP_200_OK,
            'type': "json",
            'message': results,
            'length': prompt_count
        })
    except Exception as e:
        logger.error(f"LlamaIndex - explore_documents() encountered an error: {e}")
        return JSONResponse({
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'type': "string",
            'message': "An error occurred while fetching documents."
        })


#1
# Helper function to load a document
def load_document(document_id: str):
    """
    Load a document from the LlamaIndex using the document_id as the key.
    """
    logger.info(f"LlamaIndex Services - load_document() - Loading document with ID {document_id}")  # Log function entry
    
    try:
        # Query the index to retrieve the document
        logger.info(f"LlamaIndex Services - load_document() - Querying the index")  # Log the query attempt
        query = f"Find the document with ID {document_id}"  # Natural language query for the index
        service_context = ServiceContext.from_defaults()  # Create a default service context for querying
        response: Response = index.query(query, service_context=service_context)  # Query the index
        
        # Check if a response is found
        if response is None or len(response.source_nodes) == 0:  # Check if no documents are found
            logger.info(f"LlamaIndex Services - load_document() - Document not found in the index")  # Log missing doc
            return JSONResponse(  # Return a 404 Not Found response
                {
                    'status': status.HTTP_404_NOT_FOUND,
                    'type': 'string',
                    'message': f"Document with ID {document_id} not found."
                }
            )
        
        # Extract the document content
        document = response.source_nodes[0].node.text  # Assuming the first node is the desired document
        logger.info(f"LlamaIndex Services - load_document() - Document retrieved successfully")  # Log success
        
        return JSONResponse(  # Return the document in a structured JSON response
            {
                'status': status.HTTP_200_OK,  # HTTP status 200 indicates success
                'type': 'json',  # Specify that the response is JSON
                'message': document  # Include the document content
            }
        )
    
    except Exception as e:  # Catch any exceptions during the process
        logger.error(f"LlamaIndex Services - load_document() - Error occurred: {e}")  # Log the error
        return JSONResponse(  # Return a 500 Internal Server Error response
            {
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'type': 'string',
                'message': f"An error occurred while loading the document: {e}"
            }
        )

#2
# Extract relevant keywords from user's question using a GPT model
def extract_keywords_from_question(question: str) -> str:
    """
    Extracts 5 relevant keywords or topics from the user's question using LlamaIndex and OpenAI.
    """
    logger.info(f"LlamaIndex Services - extract_keywords_from_question() - Extracting keywords from question")
    
    # Define the prompt template for keyword extraction
    prompt_template = """
    Given the following question, return a list of 5 relevant keywords or topics to search in research papers:
    Question: {question}
    Relevant Keywords/Topics (5):
    """
    
    # Initialize the OpenAI LLM with the necessary API key and configuration
    logger.info(f"LlamaIndex Services - extract_keywords_from_question() - Initializing LlamaIndex OpenAI LLM")
    llm = OpenAI(model="gpt-4", api_key=os.getenv("OPENAI_API_KEY"))  # Replace with your actual API key
    
    # Create a prompt template
    prompt = PromptTemplate(input_variables=["question"], template=prompt_template)
    logger.info(f"LlamaIndex Services - extract_keywords_from_question() - Prompt template initialized successfully")
    
    # Format the prompt with the user's question
    formatted_prompt = prompt.format(question=question)
    logger.info(f"LlamaIndex Services - extract_keywords_from_question() - Prompt formatted: {formatted_prompt}")
    
    # Query the LLM to get the keywords
    response = llm.predict(formatted_prompt)
    logger.info(f"LlamaIndex Services - extract_keywords_from_question() - Response received from LLM")
    
    # Return the cleaned-up keywords
    return response.strip()  # Remove any extra whitespace from the response



#3
# Tool: Search Arxiv for relevant research papers
@Tool(name="search_arxiv", description="Searches Arxiv for papers based on extracted keywords.")
def search_arxiv(keywords: str, max_results: int = 5):
    """
    Searches Arxiv for papers related to the given keywords.

    Args:
        keywords (str): Keywords for the search query.
        max_results (int): Maximum number of results to fetch.

    Returns:
        List[Dict]: A list of articles with their metadata or None if no results.
    """
    logger.info("LlamaIndex - search_arxiv() - Starting search on Arxiv.")
    
    # Construct the Arxiv API URL with the search query
    search_url = f"http://export.arxiv.org/api/query?search_query=all:{keywords}&start=0&max_results={max_results}"
    
    # Send the request to Arxiv's API
    response = requests.get(search_url)
    if response.status_code == 200:
        logger.info("LlamaIndex - search_arxiv() - Successfully fetched results from Arxiv.")
        
        # Parse the XML response from the Arxiv API
        root = ElementTree.fromstring(response.content)
        namespaces = {'': 'http://www.w3.org/2005/Atom'}  # Define XML namespaces for parsing
        entries = root.findall('.//entry', namespaces)  # Find all research entries
        
        # Extract relevant metadata for each research article
        articles = []
        for entry in entries[:max_results]:
            articles.append({
                'title': entry.find('title', namespaces).text,
                'arxiv_id': entry.find('id', namespaces).text.split('/')[-1],
                'abstract': entry.find('summary', namespaces).text,
                'link': entry.find('id', namespaces).text
            })

        logger.info(f"LlamaIndex - search_arxiv() - Retrieved articles: {articles}")
        return articles  # Return the list of articles
    else:
        logger.error("LlamaIndex - search_arxiv() - Failed to fetch data from Arxiv.")
        return None  # Return None if the request fails


# Tool: Arxiv Agent to fetch and format research papers based on a user question
@Tool(name="arxiv_agent", description="Fetches relevant Arxiv papers based on a user question.")
def arxiv_agent(question: str):
    """
    Fetches relevant ArXiv papers based on a user question.

    Args:
        question (str): The user's research question.

    Returns:
        JSONResponse: A FastAPI-compatible response with the query results or error message.
    """
    logger.info("LlamaIndex - arxiv_agent() - Handling user question with Arxiv agent.")

    try:
        # Step 1: Extract keywords using a prompt
        prompt_template = """
        Given the following question, return a list of 5 relevant keywords or topics to search in research papers:
        Question: {question}
        Relevant Keywords/Topics (5):
        """
        prompt = PromptTemplate(template=prompt_template, input_variables=["question"])
        prompt_helper = PromptHelper.from_defaults()  # Use default settings for prompt execution
        keywords = prompt_helper.format_prompt(prompt, question=question).strip()  # Generate keywords
        
        if not keywords:
            logger.error("LlamaIndex - arxiv_agent() - No keywords extracted from question.")
            return JSONResponse({
                'status': status.HTTP_404_NOT_FOUND,
                'type': 'string',
                'message': f"Couldn't extract any relevant keywords from your question: {question}"
            })
        
        logger.info(f"LlamaIndex - arxiv_agent() - Extracted keywords: {keywords}")

        # Step 2: Search Arxiv using the extracted keywords
        results = search_arxiv(keywords)
        if not results:
            logger.info("LlamaIndex - arxiv_agent() - No articles found on Arxiv for the given keywords.")
            return JSONResponse({
                'status': status.HTTP_404_NOT_FOUND,
                'type': 'string',
                'message': f"No relevant papers found on ArXiv for your question: {question}"
            })

        # Step 3: Format results into a user-friendly JSON response
        formatted_results = [
            {
                "ArXiv ID": result['arxiv_id'],
                "Title": result['title'],
                "Abstract": result['abstract'],
                "Link": result['link']
            }
            for result in results
        ]

        logger.info(f"LlamaIndex - arxiv_agent() - Returning formatted results: {formatted_results}")
        return JSONResponse({
            'status': status.HTTP_200_OK,
            'type': 'json',
            'message': formatted_results
        })
    except Exception as e:
        # Log and return any exceptions encountered
        logger.error(f"LlamaIndex - arxiv_agent() encountered an error: {e}")
        return JSONResponse({
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'type': 'string',
            'message': f"An error occurred while processing the request: {str(e)}"
        })
