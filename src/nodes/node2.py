from langchain_openai import ChatOpenAI
from src.state.graph_state import GraphState
from langchain_core.messages import SystemMessage


analysis_tool = None
def analyze_node(state: GraphState):
    llm = ChatOpenAI(model="gpt-4o")

    system_prompt = SystemMessage(
        "Based on the provided recommendation letter template, perform a search to retrieve the relevant patient data."
        " Use the retrieved patient data, along with the provided recommendation letter template and doctor information, "
        "to generate a complete recommendation letter for the specialist. Additionally, draft a professional email that "
        "can be sent to the patient, informing them about the recommendation and providing relevant details.")

    tools = [analysis_tool]

    llm_with_tools = llm.bind_tools(tools)

    analysis = llm_with_tools.invoke([system_prompt]+state['research_results'])
    
    return {
        "analysis": analysis.content,
        "messages": [analysis]
    }