from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities import RequestsWrapper
import json
from utils.console_config import pretty_print_python_code_in_panel, pretty_print_json, print_section_header, print_ruler


FHIR_BASE_URL = "https://hapi.fhir.org/baseR4"

def collect_clinical_data(state):
    if "patient_id" not in state or "specialty_type" not in state:
        print("Error: Required state variables missing")
        return {"clinical_data": None}
        
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        """
        You are a medical data retrieval specialist preparing information for a referral to a {{specialty_type}}. 
        Your task is to gather comprehensive patient information from a FHIR server for patient ID {{patient_id}}.

        Use the following function to retrieve patient data:
        - get_fhir_resources(resource_type, params): Makes GET requests to FHIR server

        Required steps:
        1. Retrieve the patient's basic information
        2. Fetch all clinically relevant resources for a {{specialty_type}} referral:
           - Patient demographics
           - Active and historical conditions
           - Current medications
           - Recent observations and vital signs
           - Diagnostic reports
           - Recent procedures
           - Relevant allergies
        3. Store all retrieved data in the clinical_data dictionary

        Generate executable Python code that:
        - Uses proper error handling
        - Stores complete resource bundles
        - Includes all relevant resource types
        - Maintains data relationships
        
        Return ONLY executable Python code without any explanations or markdown. 
        Ensure the code is executable without requiring additional modifications.


        Code Start:

        # Initialize data storage
        clinical_data = {{"patient_id": patient_id, "specialty_type": specialty_type}}

        # 1. Get Patient Resource
        patient_data = get_fhir_resources("Patient/" + patient_id)
        if not patient_data:
            print("Error: Could not find patient with ID " + patient_id)
            clinical_data['error'] = "Patient not found"
        else:
            clinical_data['patient'] = patient_data

            # 2. Get Clinical Resources
            resource_types = [
                "Condition",
                "MedicationStatement",
                "MedicationRequest",
                "Observation",
                "DiagnosticReport",
                "Procedure",
                "AllergyIntolerance"
            ]

            for resource_type in resource_types:
                try:
                    resource_data = get_fhir_resources(
                        resource_type,
                        {{"patient": patient_id}}
                    )
                    if resource_data and 'entry' in resource_data:
                        clinical_data[resource_type.lower() + 's'] = resource_data
                        print("Found " + str(len(resource_data.get('entry', []))) + " " + resource_type + " resources")
                    else:
                        print("No " + resource_type + " resources found for patient " + patient_id)
                except Exception as e:
                    print("Error fetching " + resource_type + ": " + str(e))
                    continue


        """)
    
    chain = (prompt | model | StrOutputParser())
    generated_code = chain.invoke({
        "patient_id": state["patient_id"],
        "specialty_type": state["specialty_type"]
    })
    code_to_execute = check_formatting(generated_code)
    print_section_header("GENERATED CODE", "green")
    pretty_print_python_code_in_panel(code_to_execute)
    print_ruler()
    # Create namespace with required functions and variables
    global_namespace = {
        'get_fhir_resources': get_fhir_resources,
        'print': print,
        'patient_id': state["patient_id"],
        'specialty_type': state["specialty_type"]
    }
    print_section_header("Code Outputs", "yellow")
    exec(code_to_execute, global_namespace)
    print_ruler()

    clinical_data = global_namespace.get("clinical_data", {})
    print_section_header("CLINICAL DATA", "blue")
    print_ruler()
    pretty_print_json(clinical_data)
    print_ruler()

    return {"clinical_data": clinical_data}

def check_formatting(code):
    if "```" in code:
        lines = code.split('\n')
        executable_lines = [line for line in lines if not line.strip().startswith('```')]
        return '\n'.join(executable_lines)
    return code


def get_fhir_resources(resource_type, params=None):
    """Function to make GET requests to FHIR server
    
    Args:
        resource_type (str): The FHIR resource type (e.g., Patient, Condition)
        params (dict, optional): Query parameters for the request
        
    Returns:
        dict: The FHIR resource bundle if successful, None otherwise
    """
    url = f"{FHIR_BASE_URL}/{resource_type}"
    requests_wrapper = RequestsWrapper()  # Create an instance
    response = requests_wrapper.get(url, params=params)  # Use .get() from the wrapper.
    return json.loads(response)
