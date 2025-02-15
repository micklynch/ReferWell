from astrapy import DataAPIClient
from typing import List
from utils.console_config import pretty_print_json, print_ruler, print_section_header
import os

# Initialize the client
client = DataAPIClient(os.getenv("ASTRA_DB_API_KEY"))
db = client.get_database_by_api_endpoint(os.getenv("ASTRA_DB_URL"))
collection = db.get_collection("specialists_taxonomy")

print_ruler()
print_section_header(f"Specialist Type from {db.list_collection_names()}", "green")

def find_specialist_type(reason: str, result_size: int=3) -> List[str]:
    """
    Finds the most appropriate specialists codes based on reasons
    Example Output: 
    [
        {
            "Code": "2080P0202X", 
            "Display Name": "Pediatric Critical Care Medicine"
        }, 
        {
            "Code": "2080P0205X", 
            "Display Name": "Pediatric Emergency Medicine"
        }, 
        {
            "Code": "207RC0000X", 
            "Display Name": "Cardiovascular Disease"
        }
    ]
    """
    specialists_type = list(collection.find(
    sort={"$vectorize": reason},
    limit=result_size,
    ))
    specialists_code_name = [{"Code": item['Code'], "Display Name": item['Display_Name']} for item in specialists_type]
    pretty_print_json(specialists_code_name)

    return specialists_code_name
