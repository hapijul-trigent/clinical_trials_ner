import logging
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser, BaseOutputParser
from io import StringIO
import pandas as pd

class CSVStringToDataFrameParser(BaseOutputParser):
    def __init__(self):
        pass

    def parse(self, output: str) -> pd.DataFrame:
        # Strip leading/trailing whitespace and newlines
        output = output.strip()

        # Use StringIO to treat the string as a file-like object
        csv_data = StringIO(output)

        # Read the CSV data into a DataFrame
        df = pd.read_csv(csv_data)
        df.drop_duplicates(subset=['EntityName'], inplace=True)

        return df

@st.cache_resource(show_spinner=False)
def loadChain() -> str:
    """
    Generate a medical description to a given Named Entity using a pre-trained GPT model.

    Args:
        entity (str): The medical Entity to description.

    Returns:
        str: The generated description.

    Raises:
        Exception: If there's an error during pipeline execution.
    """
    logger = logging.getLogger(__name__)
    logger.info("Generating medical description...")
    try:
        # Define the prompt template
        prompt_template = PromptTemplate(
            input_variables=['entities'],
            template="""
                Example input: [("Aspirin", "Drug"), ("Insulin", "Drug"), ("HCTZ", "Drug")]
                Format the output as CSV:
                EntityName, EntityType, A brief description of the entity,Relevant medical references for the entity
                EntityName, EntityType, A brief description of the entity,Relevant medical references for the entity

                Generate the CSV format output for the given input: {entities}
                """
                )
        # Initialize the ChatGroq model
        llm_groq_mixtral = ChatGroq(
            model="mixtral-8x7b-32768",
            temperature=0.3,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            groq_api_key='API'
        )

        # Create the LLM chain
        llm_chain = prompt_template | llm_groq_mixtral | CSVStringToDataFrameParser()
        logger.info("description generated successfully!")
        return llm_chain
    except Exception as e:
        logger.error("Error generating medical description:", exc_info=True)
        raise Exception("Error generating medical description") from e


def get_description_refrences(entities, llm_chain):
    """
    Fetches medical information for a given entity using the LLM chain.

    Parameters:
        entities (dict): A dictionary containing the 'entity' and 'type'. 
                           Example: {"entity": "Aspirin", "type": "Drug"}

    Returns:
        json: A tuple containing 'description' (str) and 'references' (list of str).
               Returns (None, None) if an error occurs.

    Example:
        entities = {"entity": "Aspirin", "type": "Drug"}
        description, references = get_medical_info(entities)
        print("Description:", description)
        print("Medical References:", references)
    """
    try:
        # Run the LLM chain with the provided input data
        output = llm_chain.invoke(entities)

        return output

    except Exception as e:
        # Handle any errors that occur during the process
        print(f"An error occurred in get_description_refrences: {e}")
        return None

# Example usage
# llm_chain = loadChain()
# entities = {"entities": '[("Aspirin","Drug"), ("Insulin", "Drug"}, ("HCTZ ", "Drug")]'}
# output = get_description_refrences(entities, llm_chain=llm_chain)
# import pprint
# pprint.pprint(output)
# print(type(output))
