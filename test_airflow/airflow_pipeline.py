# from airflow import DAG
# from airflow.operators.python_operator import PythonOperator
# from airflow.utils.dates import days_ago

import os
import boto3
import logging
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from docling.datamodel.base_models import InputFormat
from docling_core.types.doc import PictureItem, TableItem
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

import os 
import math
import uuid
import time
import base64
import openai
import logging
import pinecone
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv
from pinecone import ServerlessSpec
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from langchain.schema import HumanMessage

# Logger function
logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load Environment variables
load_dotenv()

def download_files_from_s3(bucket_name, document_id):
    logger.info(f"Ariflow - download_files_from_s3 - Downloading files from s3 with respect to document_id {document_id}")
    s3_client = boto3.client(
        's3',
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    local_folder_path = os.path.join(os.getcwd(), os.getenv("DOWNLOAD_DIRECTORY"))
    
    if not os.path.exists(local_folder_path):
        logger.info(f"Ariflow - download_files_from_s3 - Creating local directory to store files in {document_id}")
        os.makedirs(local_folder_path)
    else:
        logger.info(f"Ariflow - download_files_from_s3 - Local directory for document {document_id} already exists, skipping download ")

    try:
        # List all objects in the folder
        files = s3_client.list_objects_v2(Bucket = bucket_name, Prefix = document_id)
        if 'Contents' in files:
            for file in files['Contents']:
                file_key = file['Key']
                local_file_path = os.path.join(local_folder_path, file_key)
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                s3_client.download_file(bucket_name, file_key, local_file_path)
            logger.info(f"Ariflow - download_files_from_s3 - Downloaded all files from {document_id} successfully to {local_folder_path}")
        else:
            logger.info(f"Ariflow - download_files_from_s3 - No files found in folder {document_id}")


    except Exception as e:
        logger.error(f"Ariflow - download_files_from_s3 - Error downloading file {document_id}: {e}")
        raise e

def download_files_from_s3_driver_func():
    logger.info(f"Ariflow - download_files_from_s3_driver_func - Driver function to download files from s3")
    # Load environment variables
    bucket_name = os.getenv("S3_BUCKET_NAME")
    document_ids = ['68db7e4f057f494fb5b939ba258cefcd/', '97b6383e18bb48d1b7daceb27ad0a198/', '52af53cc2f5e42558253aa572a55b78a/']

    try:
        for document_id in document_ids:
            download_files_from_s3(bucket_name, document_id)
        logger.info(f"Ariflow - download_files_from_s3_driver_func - All files downloaded successfully from s3 to local")
    except Exception as e:
        logger.error(f"Ariflow - download_files_from_s3_driver_func - Error while downloading PDF documents from S3: {e}")
        raise e


def document_Parser(input_doc_path, output_dir):
    logger.info(f"Ariflow - document_Parser - Parsing through PDF file using Docling")

    logger.info(f"Ariflow - document_Parser - Initializing parameters for pipeline_options")
    # Parameters for pipeline
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = True
    pipeline_options.images_scale = 5.0
    pipeline_options.generate_table_images = True
    pipeline_options.generate_picture_images = True

    logger.info(f"Ariflow - document_Parser - All parameters set for the pipeline options")
    # Initializing document converter
    doc_converter = DocumentConverter(
        format_options = {
            InputFormat.PDF: PdfFormatOption(pipeline_options = pipeline_options)
        }
    )
    logger.info(f"Ariflow - document_Parser - Document converter initialized")

    # Store the result
    conv_result = doc_converter.convert(input_doc_path)
    logger.info(f"Ariflow - document_Parser - All contents extracted from PDF file successfully")
    
    # Store results in local directory
    doc_filename = conv_result.input.file.stem

    tables_ouput_dir = Path(os.path.join(output_dir, "tables"))
    tables_ouput_dir.mkdir(parents=True, exist_ok=True)

    images_output_dir = Path(os.path.join(output_dir, "images"))
    images_output_dir.mkdir(parents=True, exist_ok=True)

    csv_files_output_dir = Path(os.path.join(output_dir, "csv_files"))
    csv_files_output_dir.mkdir(parents=True, exist_ok=True)

    # Save images and tables in respective folder
    table_counter = 0
    image_counter = 0

    for element, _level in conv_result.document.iterate_items():
        # Storing all the tables
        if isinstance(element, TableItem):
            table_counter += 1
            table_filename =  Path(os.path.join( tables_ouput_dir, f"table-{table_counter}.png"))
            with table_filename.open("wb") as fp:
                element.image.pil_image.save(fp, "PNG")
        
        # Storing images
        if isinstance(element, PictureItem):
            image_counter += 1
            image_filename = Path(os.path.join(images_output_dir, f"picture-{image_counter}.png"))
            with image_filename.open("wb") as fp:
                element.image.pil_image.save(fp, "PNG")
    
    logger.info(f"Ariflow - document_Parser - All images and tables stored as PNG in images, tables folder")

    for table_ix, table in enumerate(conv_result.document.tables):
        table_df: pd.DataFrame = table.export_to_dataframe()
        csv_filename = Path(os.path.join(csv_files_output_dir, f"table-{table_ix+1}.csv"))
        table_df.to_csv(csv_filename)

    logger.info(f"Ariflow - document_Parser - All tables stored in CSV format in csv_files folder")
    
    with (Path(os.path.join(output_dir, f"{doc_filename}.md"))).open("w", encoding = "utf-8") as fp:
        fp.write(conv_result.document.export_to_markdown())

    logger.info(f"Ariflow - document_Parser - Text from PDF document is stored as markdown file")

def doc_parser_driver_func():
    logger.info(f"Ariflow - doc_parser_driver_func - Driver function to parse through every PDF document using Docling")
    download_dir = Path(os.path.join(os.getcwd(), os.getenv("DOWNLOAD_DIRECTORY")))

    # Loop through all subdirectories (document_id folders) in the DOWNLOAD_DIRECTORY
    logger.info(f"Ariflow - doc_parser_driver_func - Looping through all documents in {download_dir}")
    for document_id_dir in download_dir.iterdir():
        logger.info(f"Ariflow - doc_parser_driver_func - Listing all PDF files in {document_id_dir}")
        if document_id_dir.is_dir():

            # Initialize fname variable as None
            fname = None

            # Check if there's a PDF file inside the document_id directory
            dir_contents = os.listdir(document_id_dir)
            for file in dir_contents:
                if file.endswith(".pdf"):
                    fname = file
                    break  # Stop after the first PDF file is found

            # If a PDF file is found, proceed; otherwise, handle the error
            if fname:
                output_dir = Path(os.path.join(document_id_dir, "parsed_documents"))
                output_dir.mkdir(parents=True, exist_ok=True)
                input_dir = Path(os.path.join(document_id_dir, fname))
                logger.info(f"Ariflow - doc_parser_driver_func - Parsing document from {input_dir} and storing the parsed_document in {output_dir}")
                document_Parser(input_dir, output_dir)
            else:
                logger.info(f"Ariflow - doc_parser_driver_func - No PDF file found in {document_id_dir}")
        else:
            logger.info(f"Ariflow - doc_parser_driver_func - {document_id_dir} directory does not exist")


def encode_image_to_base64(image_path):
    try:
        with open(image_path, 'rb') as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        return img_base64
    except Exception as e:
        print(f"Error encoding image to base64: {e}")
        return None
    
def summarize_image_with_gpt(image_base64):
    try:
        prompt = f"You are an assistant tasked with summarizing image {image_base64} for retrieval via RAGs. These summaries will be embedded and used to retrieve the raw image via RAGs. Give a concise summary of the image that is well optimized for retrieval via RAGs."

        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Generate response from GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5  # Adjust as needed for consistency
        )

        summary = response['choices'][0]['message']['content'].strip()
        return summary
    except Exception as e:
        print(f"Error generating summary with GPT-4o: {e}")
        return None
    
def image_summarize(img_base64, prompt):
    chat = ChatOpenAI(
        model       = "gpt-4o", 
        max_tokens  = 1024,
        api_key     = os.getenv("OPEN_AI_API")
    )

    msg = chat.invoke(
        [
            HumanMessage(
                content=[
                    {
                        "type": "text", 
                        "text": prompt
                    },
                    {
                        "type"      : "image_url",
                        "image_url" : {"url": f"data:image/jpeg;base64,{img_base64}"},
                    },
                ]
            )
        ]
    )
    return msg.content


def process_images_and_tables(folder_path):
    summaries = []

    prompt = f"You are an assistant tasked with summarizing images for retrieval via RAGs. These summaries will be embedded and used to retrieve the raw image via RAGs. Give a concise summary of the image that is well optimized for retrieval via RAGs."


    for image_filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_filename)

        if os.path.isfile(image_path):
            print(f"Processing image {image_filename}")

            # Encode image to base64
            image_base64 = encode_image_to_base64(image_path)
            if image_base64:
                image_summary = image_summarize(image_base64, prompt)
                print(f"image {image_filename} and summary = {image_summary}")
                if image_summary:
                    summaries.append(image_summary)
                    summary_filename = os.path.splitext(image_filename)[0] + "_summary.txt"
                    summary_filedir = Path(os.path.join(folder_path, "summaries"))
                    summary_filedir.mkdir(parents=True, exist_ok=True)
                    summary_filepath = os.path.join(summary_filedir, summary_filename)
                    with open(summary_filepath, "w") as file:
                        file.write(image_summary)
                else:
                    summaries.append(f"Failed to summarize image: {image_filename}")
            else:
                summaries.append(f"Failed to encode image: {image_filename}")

    return summaries

def create_embeddings_in_batches(embedding_model, texts, batch_size = 5):
    all_embeddings = []
    total_batches = math.ceil(len(texts)/ batch_size)

    for i in range(total_batches):
        # Get the start and end indices for the current batch
        batch_texts = texts[i * batch_size: (i+1) * batch_size]
        
        # Generate embeddings for the current branch
        batch_embeddings = embedding_model.embed_documents(batch_texts)

        # Append the embeddings to the list of all embeddings
        all_embeddings.extend(batch_embeddings)

        print(f"Processed batch {i+1}/{total_batches} with {len(batch_texts)} texts.")

    return all_embeddings

def vectorDB_driver_func():
    # markdown_file_path = "/Users/deepthi/Documents/Courses/bigdata/Assignment4/test_airflow/downloads/68db7e4f057f494fb5b939ba258cefcd/parsed_documents/Revisiting-the-Equity-Risk-Premium.md"
    # images_folder_path = "/Users/deepthi/Documents/Courses/bigdata/Assignment4/test_airflow/downloads/68db7e4f057f494fb5b939ba258cefcd/parsed_documents/images"
    # tables_folder_path = "/Users/deepthi/Documents/Courses/bigdata/Assignment4/test_airflow/downloads/68db7e4f057f494fb5b939ba258cefcd/parsed_documents/tables"

    file_dir = Path(os.path.join(os.getcwd(), os.getenv("DOWNLOAD_DIRECTORY")))
    markdown_fname = None

    for document_id_dir in file_dir.iterdir():
        if document_id_dir.is_dir() and not document_id_dir.name.startswith('.'):
            parsed_document_dir = document_id_dir / "parsed_documents"
            if parsed_document_dir.is_dir():
                parsed_contents = os.listdir(parsed_document_dir)

                markdown_file_path = None
                images_folder_path = None
                tables_folder_path = None

                for file in parsed_contents:
                    file_path = parsed_document_dir / file

                    # Skip hidden files (like .DS_Store)
                    if file.startswith('.'):
                        continue
                    
                    if file.endswith(".md"):
                        markdown_fname = file
                        markdown_file_path = file_path
                        print(f"Markdown file found: {markdown_file_path}")
                
                    # Check for images folder
                    elif file == "images":
                        images_folder_path = file_path
                        print(f"Images folder found: {images_folder_path}")
                    
                    # Check for tables folder
                    elif file == "tables":
                        tables_folder_path = file_path
                        print(f"Tables folder found: {tables_folder_path}")


    # Load data from markdown file using Unstructured
    loader = UnstructuredMarkdownLoader(markdown_file_path, mode = "elements")
    data = loader.load()

    # Text splitter for splitting data into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 4000,
        chunk_overlap = 200
    )

    chunks = []
    # Process markdown text
    for element in data:
        text = element.page_content
        chunks.extend(text_splitter.create_documents([text]))
    
    image_summaries = process_images_and_tables(images_folder_path)
    table_summaries = process_images_and_tables(tables_folder_path)

    # Prepare text data for embedding (extract the actual text from chunks)
    texts = [chunk.page_content for chunk in chunks] + image_summaries + table_summaries

    embedding_model = OpenAIEmbeddings(model="text-embedding-3-large", api_key=os.getenv("OPENAI_API_KEY"))

    embeddings = create_embeddings_in_batches(embedding_model, texts)

    # Print the length of embeddings and the size of the first embedding vector
    print(f"Total embeddings generated: {len(embeddings)}")
    print(f"Size of first embedding: {len(embeddings[0])}")


    # Initialize Pinecone client
    pc = pinecone.Pinecone(api_key = os.getenv("PINECONE_API_KEY"))

    # Pinecone index name
    index_name = 'langchain-document-index'

    # Check if the index exists, delete if present, then create a new one
    if index_name in pc.list_indexes().names():
        pc.delete_index(index_name)
        print(f"Deleted existing index {index_name}.")

    # Create a spec for the index
    spec = ServerlessSpec(cloud="aws", region="us-east-1")

    pc.create_index(
        name=index_name,
        dimension=3072,
        metric='cosine',
        spec=spec
    )
    print(f"Created new index {index_name}.")

    # Wait for index to be initialized
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)

    # Connect to the index
    index = pc.Index(index_name)

    time.sleep(1)
    # view index stats
    index.describe_index_stats()

    # Create unique IDs for each document
    ids = [str(uuid.uuid4()) for _ in range(len(texts))]  # Use consistent IDs if overwriting is needed

    # Convert text data into Langchain Document objects
    docs = [Document(page_content=texts[i], metadata={"id": ids[i]}) for i in range(len(texts))]
    
    docsearch = PineconeVectorStore.from_documents(docs, embedding_model, index_name=index_name)
    print(f"Upserted vectors into Pinecone using PineconeVectorStore.")


def main():
    # download_files_from_s3_driver_func()
    # doc_parser_driver_func()
    vectorDB_driver_func()

if __name__ == '__main__':
    main()