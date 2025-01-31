from src.graphs.my_graph import create_graph
from dotenv import load_dotenv

load_dotenv()

def main():
    graph = create_graph()
    initial_state = {
        "query": "Find a cardiologist for Patient with ID 54321",
        "research_results": [],
        "analysis": "",
        "messages": [],
        "retry_count": 0
    }
    
    result = graph.invoke(initial_state)
    print(result['analysis'])

if __name__ == "__main__":
    main()