from langchain_openai import ChatOpenAI
from src.state.graph_state import GraphState

def analyze_node(state: GraphState):
    model = ChatOpenAI(model="gpt-4o")
    research_results = state['research_results']
    
    analysis = model.invoke(f"Analyze these research results: {research_results}")
    
    return {
        "analysis": analysis.content,
        "messages": [analysis]
    }