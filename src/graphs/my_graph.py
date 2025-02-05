from langgraph.graph import StateGraph,START, END
from state.graph_state import GraphState
from nodes import node1, node2,node3


def create_graph():
    workflow = StateGraph(GraphState)
    
    """workflow.add_node("specialist", node1.specialist_search)"""
    workflow.add_node("analyze", node2.analyze_node)
    workflow.add_node("generate", node3.generate_node)

    workflow.add_edge(START, "analyze")
    workflow.add_edge("analyze", "generate")
    workflow.add_edge("generate", END)
    
    return workflow.compile()