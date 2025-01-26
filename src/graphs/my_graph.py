from langgraph.graph import StateGraph, END
from src.state.graph_state import GraphState
from src.nodes import node1, node2

def create_graph():
    workflow = StateGraph(GraphState)
    
    workflow.add_node("specialist", node1.specialist_search)
    workflow.add_node("analyze", node2.analyze_node)
    
    workflow.set_entry_point("specialist")
    workflow.add_edge("specialist", "analyze")
    workflow.add_edge("analyze", END)
    
    return workflow.compile()
