from typing import TypedDict, Dict,Any


class GraphState(TypedDict):
    patient_id: str
    referrer_details: str
    specialty_type: str
    reason: str
    clinical_data: Dict[str,Any]
    referral_letter: str