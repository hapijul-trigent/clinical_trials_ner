import streamlit as st
import PyPDF2
from docx import Document
from typing import Union

def upload_file() -> Union[object, None]:
    """
    File uploader widget for clinical trial documents.

    Returns:
        st.UploadedFile or None: The uploaded file object if a file is uploaded,
        otherwise None.
    """
    st.sidebar.title('Upload Trial Document')
    uploaded_file = st.sidebar.file_uploader("", type=["pdf", "docx", "txt"])
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
        reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extractText()
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif file.type == "text/plain":
        text = file.read().decode("utf-8")
    else:
        raise ValueError(f"Unsupported file type: {file.type}")
    return text