import pandas as pd
import logging
from typing import List
from sparknlp.annotation import Annotation
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def ner_chunks_to_dataframe(ner_chunks: List[Annotation]) -> pd.DataFrame:
    """
    Converts a list of NER chunk annotations into a Pandas DataFrame.
    
    Args:
        ner_chunks (List[Annotation]): A list of NER chunk annotations.
        
    Returns:
        pd.DataFrame: A DataFrame containing the NER chunk data.
        
    Example:
        ner_chunks = [
            Annotation(chunk, 17, 27, '40-year-old', {'chunk': '0', 'confidence': '0.999', 'ner_source': 'ner_chunk', 'entity': 'Age', 'sentence': '0'}, []),
            Annotation(chunk, 29, 33, 'white', {'chunk': '1', 'confidence': '0.9983', 'ner_source': 'ner_chunk', 'entity': 'Race_Ethnicity', 'sentence': '0'}, []),
            ...
        ]
        df = ner_chunks_to_dataframe(ner_chunks)
    """
    logger = logging.getLogger(__name__)
    try:
        logger.info("Converting NER chunks to DataFrame")
        
        # Extract data from NER chunks
        data = []
        for chunk in ner_chunks:
            data.append({
                "chunk": chunk.result,
                "start": chunk.begin,
                "end": chunk.end,
                "confidence": float(chunk.metadata.get('confidence', 0.0)),
                "ner_source": chunk.metadata.get('ner_source', ''),
                "entity": chunk.metadata.get('entity', ''),
                "sentence": chunk.metadata.get('sentence', ''),
            })
        
        # Create DataFrame
        df = pd.DataFrame(data)
        logger.info("Conversion successful. DataFrame created with %d records.", len(df))
        
        return df
    
    except Exception as e:
        logger.error("Failed to convert NER chunks to DataFrame: %s", str(e))
        return pd.DataFrame()  # Return an empty DataFrame on failure


def dataframe_to_csv(df: pd.DataFrame) -> bytes:
    """
    Converts a DataFrame to CSV format.
    
    Args:
        df (pd.DataFrame): The DataFrame to convert.
    
    Returns:
        bytes: The CSV data in bytes.
    """
    logger = logging.getLogger(__name__)
    try:
        csv_data = df.to_csv(index=False).encode('utf-8')
        logger.info("DataFrame successfully converted to CSV format.")
        return csv_data
    except Exception as e:
        logger.error("Failed to convert DataFrame to CSV: %s", str(e))
        return b""


def dataframe_to_json(df: pd.DataFrame) -> bytes:
    """
    Converts a DataFrame to JSON format.
    
    Args:
        df (pd.DataFrame): The DataFrame to convert.
    
    Returns:
        bytes: The JSON data in bytes.
    """
    logger = logging.getLogger(__name__)
    try:
        json_data = df.to_json(orient='records').encode('utf-8')
        logger.info("DataFrame successfully converted to JSON format.")
        return json_data
    except Exception as e:
        logger.error("Failed to convert DataFrame to JSON: %s", str(e))
        return b""

def dataframe_to_pdf(df: pd.DataFrame) -> bytes:
    """
    Converts a DataFrame to PDF format.
    
    Args:
        df (pd.DataFrame): The DataFrame to convert.
    
    Returns:
        bytes: The PDF data in bytes.
    """
    logger = logging.getLogger(__name__)
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        table_data = [df.columns.tolist()] + df.values.tolist()
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements = [table]
        doc.build(elements)
        buffer.seek(0)
        logger.info("DataFrame successfully converted to PDF format.")
        return buffer.getvalue()
    except Exception as e:
        logger.error("Failed to convert DataFrame to PDF: %s", str(e))
        return b""

