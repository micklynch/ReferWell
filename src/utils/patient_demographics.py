# use type hints to specify the return type of the function
from typing import Dict
import requests

FHIR_SERVER_URL = "https://hapi.fhir.org/baseR4"

# Function to get patient name and address, given a patient ID
def get_patient_demographics(patient_id) -> Dict[str, str]:
    url = f"{FHIR_SERVER_URL}/Patient/{patient_id}"
    response = requests.get(url)
    patient = response.json()

    return {
        "name": f"{patient['name'][0]['given'][0]} {patient['name'][0]['family']}",
        "address": f"{patient['address'][0]['line'][0]}, {patient['address'][0]['city']}, {patient['address'][0]['state']} {patient['address'][0]['postalCode']}"
    }

# dunder name check
if __name__ == "__main__":
    print(get_patient_demographics("46085643"))