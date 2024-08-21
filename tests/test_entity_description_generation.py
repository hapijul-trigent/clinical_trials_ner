import pytest
import pandas as pd
from jsl_backend.entity_description_generation import loadChain, get_description_refrences
from jsl_backend.model_setup import setup_config
license = setup_config()
def test_load_chain():
    llm_chain = loadChain()
    
    assert llm_chain is not None

def test_get_description_refrences():
    llm_chain = loadChain()
    entities = [("Aspirin", "Drug"), ("Insulin", "Drug"), ("HCTZ", "Drug")]
    
    df = get_description_refrences(entities, llm_chain)
    
    assert df is not None
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
