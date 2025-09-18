from typing import Annotated,Literal, Optional
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
    num: Optional[int]
    
    
def first_node(state: State):
    print("\n\nStarting of the Node")    
    return {"messages": ["First Node"]}

def conditional_node(state: State)->Literal["secondA","secondB"]:
    num = state.get("num")
    print(f"\n\nConditional Node :{num}")
    if num == 1:
        return "secondA"
    else:
        return "secondB"

def second_a(state: State):
    print("\n\nSecond A")
    return { "messages": ["Message from Second A"]}

def second_b(state: State):
    print("\n\n Second B")
    return { "messages": ["Message from Second B"] }

def last_node(state: State):
    print("\n\nEnd Node")
    return {"messages": ["Last Node Message"]}
    

graph_builder = StateGraph(State)

graph_builder.add_node("first", first_node)
graph_builder.add_node("conditional", conditional_node)
graph_builder.add_node("secondA", second_a)
graph_builder.add_node("secondB", second_b)
graph_builder.add_node("last", last_node)

graph_builder.add_edge(START, "first")
graph_builder.add_conditional_edges("first", conditional_node)
graph_builder.add_edge("secondA","last")
graph_builder.add_edge("secondB","last")
graph_builder.add_edge("last",END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages":["Hi This is the starting message Second A"],"num":2}))
print(f"updated_state:{updated_state}")
