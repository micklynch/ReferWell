from langchain_openai import ChatOpenAI
from src.state.graph_state import GraphState
from langchain_core.messages import SystemMessage

research_tool=None
def specialist_search(state: GraphState):
    llm = ChatOpenAI(model="gpt-4o")
    system_prompt = SystemMessage(
        "Based on the provided doctor’s notes, perform a search to identify the "
        "most suitable specialist and the corresponding template for generating a "
        "recommendation letter")

    tools = [research_tool]

    llm_with_tools = llm.bind_tools(tools)

    specialist_result = llm_with_tools.invoke([system_prompt]+state['messages'])
    
    return {
        "research_results": [specialist_result.content],
        "messages": [specialist_result]
    }

