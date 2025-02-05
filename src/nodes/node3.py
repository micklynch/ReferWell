from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import json


def generate_node(state):
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        f"""
            Generate a recommendation letter for the specialist 
            using the patient data and the referrer doctor details
            {{clinical_data}}
        
""")

    chain = (
            prompt | model | StrOutputParser()
    )
    print('node 3 data: ' ,state['clinical_data'])
    referral_letter = chain.invoke({"clinical_data": state['clinical_data'] })
    print(referral_letter)
    return {"referral_letter":  referral_letter}

