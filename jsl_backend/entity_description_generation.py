import logging
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from langchain_groq import ChatGroq


# Define the output parser
class MedicalOutputParser(BaseOutputParser):
    def parse(self, text: str) -> dict:
        # Split the text to extract description and references
        lines = text.strip().split("\n")
        
        # Initialize description and references
        description = ""
        references = ""
        
        # Extract description if available
        if len(lines) > 0:
            description = lines[0].replace("Description: ", "").strip()
        
        # Extract references if available
        if len(lines) > 1:
            references = lines[1].replace("Medical References: ", "").strip()
        
        return {
            "description": description,
            "references": references
        }





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
            input_variables=["entity", "type"],
            template="""
            You are a medical expert. I will provide you with a clinical entity and its type. You can use this this given {context} 
            Please generate a concise description in and provide medical references only if its a medical entity.

            Clinical Entity: {entity}
            Type: {type}

            Description: 
            Medical References: 
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
        llm_chain = prompt_template | llm_groq_mixtral | MedicalOutputParser()
        logger.info("description generated successfully!")
        return llm_chain
    except Exception as e:
        logger.error("Error generating medical description:", exc_info=True)
        raise Exception("Error generating medical description") from e


def get_description_refrences(input_data, llm_chain):
    """
    Fetches medical information for a given entity using the LLM chain.

    Parameters:
        input_data (dict): A dictionary containing the 'entity' and 'type'. 
                           Example: {"entity": "Aspirin", "type": "Drug"}

    Returns:
        tuple: A tuple containing 'description' (str) and 'references' (list of str).
               Returns (None, None) if an error occurs.

    Example:
        input_data = {"entity": "Aspirin", "type": "Drug"}
        description, references = get_medical_info(input_data)
        print("Description:", description)
        print("Medical References:", references)
    """
    try:
        # Run the LLM chain with the provided input data
        output = llm_chain.invoke(input_data)

        # Extract description and references from the output
        description = output.get("description", "No description available.")
        references = output.get("references", [])

        return description, references

    except Exception as e:
        # Handle any errors that occur during the process
        print(f"An error occurred: {e}")
        return None, None

# Example usage
llm_chain = loadChain()
input_data = {"entity": "Aspirin", "type": "Drug", 'context': 'He has been advised Aspirin 81 milligrams QDay, insulin 50 units in a.m. HCTZ 50 mg QDay. Nitroglycerin 1/150 sublingually PRN chest pain.'}
description, references = get_description_refrences(input_data, llm_chain=llm_chain)

print("Description:", description)
print("Medical References:", references)
