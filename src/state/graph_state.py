from typing import TypedDict, List


class GraphState(TypedDict):
    patient_id: str
    referrer_id: str
    specialty_type: str
    reason: str
    clinical_data: List[str]