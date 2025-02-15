from langgraph.graph import StateGraph,START, END
from state.graph_state import GraphState
from nodes import communication_node, patient_node,specialist_node


def create_graph():
    workflow = StateGraph(GraphState)
    
    workflow.add_node("specialist", specialist_node.search)
    workflow.add_node("analyze", patient_node.collect_clinical_data)
    workflow.add_node("generate", communication_node.generate_letter)

    workflow.add_edge(START, "specialist")
    workflow.add_edge("specialist", "analyze")
    workflow.add_edge("analyze", "generate")
    workflow.add_edge("generate", END)
    
    return workflow.compile()