from langchain_openai import ChatOpenAI
from src.state.graph_state import GraphState

def specialist_search(state: GraphState):
    model = ChatOpenAI(model="gpt-4o")
    query = state['query']
    
    specialist_result = model.invoke(f"specialist: {query}")
    
    return {
        "research_results": [specialist_result.content],
        "messages": [specialist_result]
    }

