from typing import TypedDict, List
from langchain_core.messages import BaseMessage

class GraphState(TypedDict):
    query: str
    specialist_results: List[str]
    patient_id: str
    analysis: str
    messages: List[BaseMessage]
    retry_count: int
