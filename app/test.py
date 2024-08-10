import streamlit as st

st.title('Test')
html = """<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Vistol Regular:wght@300;400;500;600;700&display=swap');
    
    .spark-nlp-display-scroll-entities {
        border: 1px solid #E7EDF0;
        border-radius: 3px;
        text-align: justify;
        
    }
    .spark-nlp-display-scroll-entities span {  
        font-size: 14px;
        line-height: 24px;
        color: #536B76;
        font-family: 'Montserrat', sans-serif !important;
    }
    
    .spark-nlp-display-entity-wrapper{
    
        display: inline-grid;
        text-align: center;
        border-radius: 4px;
        margin: 0 2px 5px 2px;
        padding: 1px
    }
    .spark-nlp-display-entity-name{
        font-size: 14px;
        line-height: 24px;
        font-family: 'Montserrat', sans-serif !important;
        
        background: #f1f2f3;
        border-width: medium;
        text-align: center;
        
        font-weight: 400;
        
        border-radius: 5px;
        padding: 2px 5px;
        display: block;
        margin: 3px 2px;
    
    }
    .spark-nlp-display-entity-type{
        font-size: 14px;
        line-height: 24px;
        color: #ffffff;
        font-family: 'Montserrat', sans-serif !important;
        
        text-transform: uppercase;
        
        font-weight: 500;

        display: block;
        padding: 3px 5px;
    }
    
    .spark-nlp-display-entity-resolution{
        font-size: 14px;
        line-height: 24px;
        color: #ffffff;
        font-family: 'Vistol Regular', sans-serif !important;
        
        text-transform: uppercase;
        
        font-weight: 500;

        display: block;
        padding: 3px 5px;
    }
    
    .spark-nlp-display-others{
        font-size: 14px;
        line-height: 24px;
        font-family: 'Montserrat', sans-serif !important;
        
        font-weight: 400;
    }

</style>
 <span class="spark-nlp-display-others" style="background-color: white">The patient is a </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #ffe0ac"><span class="spark-nlp-display-entity-name">40-year-old </span><span class="spark-nlp-display-entity-type">Age</span></span><span class="spark-nlp-display-others" style="background-color: white"> </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #843B81"><span class="spark-nlp-display-entity-name">white </span><span class="spark-nlp-display-entity-type">Race_Ethnicity</span></span><span class="spark-nlp-display-others" style="background-color: white"> </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #ffacb7"><span class="spark-nlp-display-entity-name">male </span><span class="spark-nlp-display-entity-type">Gender</span></span><span class="spark-nlp-display-others" style="background-color: white"> who presents with a chief complaint of "</span><span class="spark-nlp-display-entity-wrapper" style="background-color: #098401"><span class="spark-nlp-display-entity-name">chest pain </span><span class="spark-nlp-display-entity-type">Symptom</span></span><span class="spark-nlp-display-others" style="background-color: white">". The patient is </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #044AC2"><span class="spark-nlp-display-entity-name">diabetic </span><span class="spark-nlp-display-entity-type">Diabetes</span></span><span class="spark-nlp-display-others" style="background-color: white"> and has a prior history of </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #6B736C"><span class="spark-nlp-display-entity-name">coronary artery disease </span><span class="spark-nlp-display-entity-type">Heart_Disease</span></span><span class="spark-nlp-display-others" style="background-color: white">. The patient presents </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #4AAEA2"><span class="spark-nlp-display-entity-name">today </span><span class="spark-nlp-display-entity-type">RelativeDate</span></span><span class="spark-nlp-display-others" style="background-color: white"> stating that </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #ffacb7"><span class="spark-nlp-display-entity-name">his </span><span class="spark-nlp-display-entity-type">Gender</span></span><span class="spark-nlp-display-others" style="background-color: white"> </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #098401"><span class="spark-nlp-display-entity-name">chest pain </span><span class="spark-nlp-display-entity-type">Symptom</span></span><span class="spark-nlp-display-others" style="background-color: white"> started </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #4AAEA2"><span class="spark-nlp-display-entity-name">yesterday </span><span class="spark-nlp-display-entity-type">RelativeDate</span></span><span class="spark-nlp-display-others" style="background-color: white"> </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #2C6053"><span class="spark-nlp-display-entity-name">evening </span><span class="spark-nlp-display-entity-type">RelativeTime</span></span><span class="spark-nlp-display-others" style="background-color: white"> and has been somewhat </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #8B475D"><span class="spark-nlp-display-entity-name">intermittent </span><span class="spark-nlp-display-entity-type">Modifier</span></span><span class="spark-nlp-display-others" style="background-color: white">. </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #ffacb7"><span class="spark-nlp-display-entity-name">He </span><span class="spark-nlp-display-entity-type">Gender</span></span><span class="spark-nlp-display-others" style="background-color: white"> has been advised </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #0D892D"><span class="spark-nlp-display-entity-name">Aspirin </span><span class="spark-nlp-display-entity-type">Drug_Ingredient</span></span><span class="spark-nlp-display-others" style="background-color: white"> </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #03B99F"><span class="spark-nlp-display-entity-name">81 milligrams </span><span class="spark-nlp-display-entity-type">Strength</span></span><span class="spark-nlp-display-others" style="background-color: white"> </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #1C7F50"><span class="spark-nlp-display-entity-name">QDay </span><span class="spark-nlp-display-entity-type">Frequency</span></span><span class="spark-nlp-display-others" style="background-color: white">, </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #0D892D"><span class="spark-nlp-display-entity-name">insulin </span><span class="spark-nlp-display-entity-type">Drug_Ingredient</span></span><span class="spark-nlp-display-others" style="background-color: white"> </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #03761B"><span class="spark-nlp-display-entity-name">50 units </span><span class="spark-nlp-display-entity-type">Dosage</span></span><span class="spark-nlp-display-others" style="background-color: white"> </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #1C7F50"><span class="spark-nlp-display-entity-name">in a.m </span><span class="spark-nlp-display-entity-type">Frequency</span></span><span class="spark-nlp-display-others" style="background-color: white">. </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #0D892D"><span class="spark-nlp-display-entity-name">HCTZ </span><span class="spark-nlp-display-entity-type">Drug_Ingredient</span></span><span class="spark-nlp-display-others" style="background-color: white"> </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #03B99F"><span class="spark-nlp-display-entity-name">50 mg </span><span class="spark-nlp-display-entity-type">Strength</span></span><span class="spark-nlp-display-others" style="background-color: white"> </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #1C7F50"><span class="spark-nlp-display-entity-name">QDay </span><span class="spark-nlp-display-entity-type">Frequency</span></span><span class="spark-nlp-display-others" style="background-color: white">. </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #0D892D"><span class="spark-nlp-display-entity-name">Nitroglycerin </span><span class="spark-nlp-display-entity-type">Drug_Ingredient</span></span><span class="spark-nlp-display-others" style="background-color: white"> </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #03B99F"><span class="spark-nlp-display-entity-name">1/150 </span><span class="spark-nlp-display-entity-type">Strength</span></span><span class="spark-nlp-display-others" style="background-color: white"> </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #A79AAC"><span class="spark-nlp-display-entity-name">sublingually </span><span class="spark-nlp-display-entity-type">Route</span></span><span class="spark-nlp-display-others" style="background-color: white"> </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #1C7F50"><span class="spark-nlp-display-entity-name">PRN </span><span class="spark-nlp-display-entity-type">Frequency</span></span><span class="spark-nlp-display-others" style="background-color: white"> </span><span class="spark-nlp-display-entity-wrapper" style="background-color: #098401"><span class="spark-nlp-display-entity-name">chest pain </span><span class="spark-nlp-display-entity-type">Symptom</span></span><span class="spark-nlp-display-others" style="background-color: white">.</span></div>

"""

st.markdown(
    f'<div class="scroll entities" style="overflow-x: auto;border: 1px solid rgb(230, 233, 239);border-radius: 0.25rem;padding: 1rem;margin-bottom: 2.5rem;white-space: pre-wrap;">{html}</div>'
    , unsafe_allow_html=True)