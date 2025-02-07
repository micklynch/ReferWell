from typing import TypedDict, Dict,Any


class GraphState(TypedDict):
    patient_id: str
    referrer_details: str
    specialty_type: str
    specialist_data: str
    reason: str
    clinical_data: Dict[str,Any]
    referral_letter: str