from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


def analyze_node(state):
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        f"""
            You are tasked with generating clear and executable Python code.
            Generate a python program that can fetch patient data required to 
            generate a recommendation letter while referring him to a cardiologist
             using FHIR API with the given patient id {{patient_id}}.
            If there are any missing reports or missing data for which a service order 
            can be created generate the required code to create the service orders.
            Print the details of the service order that is created.The patient details should be stored
            using the globals() function.
            Use the following FHIR Server URL in the code https://hapi.fhir.org/baseR4      
            The output should be Python code only, with no additional commentary or explanation.
            Ensure the code is executable without requiring additional modifications.
    """)
    chain = (
            prompt | model | StrOutputParser()
    )
    generated_code = chain.invoke({"patient_id": state["patient_id"]})
    code_to_execute = check_formatting(generated_code)
    print(code_to_execute)
    global_namespace = globals()
    exec(code_to_execute,global_namespace)
    patient_data = global_namespace.get("patient_data")
    print(patient_data)
    return {"clinical_data":  patient_data}


def check_formatting(code):
    # Check if the code contains markdown formatting with triple backticks
    if "```" in code:
        # Split the code by newlines
        lines = code.split('\n')
        # Filter out lines that start or end with triple backticks
        executable_lines = [line for line in lines if not line.strip().startswith('```')]
        # Join the remaining lines back into a single string
        return '\n'.join(executable_lines)
    else:
        # If no markdown formatting is detected, return the input as is
        return code

