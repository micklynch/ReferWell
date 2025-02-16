from state.graph_state import GraphState
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from utils.patient_demographics import get_patient_demographics
from utils.specialist_code_vector_search import find_specialist_type
from langgraph.types import interrupt

def search(state: GraphState):
    # Find the type of specialist
    # returns an array of specialist codes and display names
    #     Example Output: 
    # [
    #     {
    #         "Code": "2080P0202X", 
    #         "Display Name": "Pediatric Critical Care Medicine"
    #     }, 
    #     {
    #         "Code": "2080P0205X", 
    #         "Display Name": "Pediatric Emergency Medicine"
    #     }, 
    #     {
    #         "Code": "207RC0000X", 
    #         "Display Name": "Cardiovascular Disease"
    #     }
    # ]
    speciality_type_list = find_specialist_type(state['reason'], 3)
    
    csv_file = "specialists.csv"
    df = pd.read_csv(csv_file)

    patient_address = get_patient_demographics(state['patient_id'])['address']
    value = interrupt(
        {
            "specialty_type":  speciality_type_list
        }
    )

    ## TODO: I'm just picking the first one of the list, but we should interupt here to ask the user to select one
    required_specialty = speciality_type_list[value-1]['Display Name']
    state['specialty_type'] = required_specialty
    print(required_specialty)

    #closest_specialist = find_nearest_specialist(df, patient_address, required_specialty)
    closest_specialist = [
        {
            'Doctor Name': 'Dr. Alice Johnson',
            'Specialty': 'Cardiologist',
            'Address': '1001 Madison St, Seattle, WA, 98199',
            'Distance': 3.690930006315589
        },
        {
            'Doctor Name': 'Dr. Bob Smith',
            'Specialty': 'Neurologist',
            'Address': '202 Pine St, Seattle, WA, 98101',
            'Distance': 5.123456789
        },
        {
            'Doctor Name': 'Dr. Carol Lee',
            'Specialty': 'Orthopedic Surgeon',
            'Address': '303 Oak Ave, Bellevue, WA, 98004',
            'Distance': 7.891011121314
        }
    ]

    print(closest_specialist)
    value = interrupt(
        {
            "specialist_data": closest_specialist
        }
    )
    print(state)
    return {
        "specialist_data": closest_specialist[value-1],
        "specialty_type": required_specialty
    }


# Function to get latitude and longitude for an address
def get_coordinates(address):
    geolocator = Nominatim(user_agent="geo_search")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None


# Function to filter specialists by specialty
def filter_specialists_by_specialty(df, required_specialty):
    """Filters the DataFrame based on the required specialty."""
    return df[df["Specialty"].str.lower() == required_specialty.lower()]


# Function to find the nearest specialist
def find_nearest_specialist(df, patient_address, required_specialty):
    """
    Finds the nearest specialist to the patient based on address and specialty.
    Returns the closest specialist's details.
    """
    patient_coords = get_coordinates(patient_address)
    if not patient_coords:
        raise ValueError("Invalid patient address, unable to fetch coordinates.")

    # Filter specialists based on the required specialty
    filtered_df = filter_specialists_by_specialty(df, required_specialty)

    # Compute distance for each specialist
    specialists_with_distance = []
    for _, row in filtered_df.iterrows():
        doctor_address = row["Address"]
        doctor_coords = get_coordinates(doctor_address)

        if doctor_coords:
            distance = geodesic(patient_coords, doctor_coords).miles
            specialists_with_distance.append({
                "Doctor Name": row["Doctor Name"],
                "Specialty": row["Specialty"],
                "Address": doctor_address,
                "Distance": distance
            })

    specialists_with_distance.sort(key=lambda x: x["Distance"])

    return specialists_with_distance if specialists_with_distance else None
