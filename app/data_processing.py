import streamlit as st
import PyPDF2
from docx import Document
from typing import Union, Tuple
from utils import dataframe_to_csv, dataframe_to_json, dataframe_to_pdf
import logging

def upload_file(location) -> Tuple:
    """
    File uploader widget for clinical trial documents.
    params:
    location streamlit: sidebar
    Returns:
        st.UploadedFile or None: The uploaded file object if a file is uploaded,
        otherwise None.
    """
    uploaded_file = location.file_uploader("Upload Trial File", type=["pdf", "docx", "txt"])
    return uploaded_file

def extract_text(file) -> Union[str, None]:
    """
    Extracts text content from the uploaded file.

    This function supports PDF, DOCX, and TXT file formats. It uses different
    methods to extract text based on the file type.

    Args:
        file (streamlit.UploadedFile): The uploaded file object.

    Returns:
        str: The extracted text content from the file.

    Raises:
        ValueError: If an unsupported file type is provided.
    """
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif file.type == "text/plain":
        text = file.read().decode("utf-8")
    else:
        raise ValueError(f"Unsupported file type: {file.type}")
    return text



def process_dataframe(df, output_queue):
    """
    Process a DataFrame and convert it to CSV, JSON, and PDF formats.

    This function takes a DataFrame and converts it to three different formats:
    CSV, JSON, and PDF. The results are then put into the provided output queue.

    Args:
        df (pandas.DataFrame): The input DataFrame to be processed.
        output_queue (queue.Queue): A queue to store the output data.

    Returns:
        None

    Raises:
        Exception: If any error occurs during the conversion process.
    """
    logger = logging.getLogger(__name__)
    try:
        logger.info("Starting DataFrame processing")

        csv_data = dataframe_to_csv(df)
        logger.info("CSV conversion completed")

        json_data = dataframe_to_json(df)
        logger.info("JSON conversion completed")

        pdf_data = dataframe_to_pdf(df)
        logger.info("PDF conversion completed")

        output_queue.put({
            'csv': csv_data,
            'json': json_data,
            'pdf': pdf_data
        })
        logger.info("Data successfully added to output queue")

    except Exception as e:
        logger.error(f"An error occurred while processing the DataFrame: {str(e)}")
        raise