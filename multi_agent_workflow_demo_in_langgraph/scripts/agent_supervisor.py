import functools
import operator
import os
from typing import Annotated, Literal, Sequence, TypedDict

from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_experimental.tools import PythonREPLTool
from langchain_groq import ChatGroq
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Tools
tavily_tool = TavilySearch(max_results=5)
python_repl_tool = PythonREPLTool()

# Global LLM (only once)
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# Agent node function
def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {
        "messages": [
            HumanMessage(
                content=result["messages"][-1].content,
                name=name
            )
        ]
    }

# Workers
members = ["Researcher", "Coder"]
options = ["FINISH"] + members

# Response model
class RouteResponse(BaseModel):
    next: Literal["FINISH", "Researcher", "Coder"]

# Supervisor prompt
system_prompt = (
    "You are a supervisor managing workers: {members}. "
    "Given the user request decide which worker acts next. "
    "When the task is complete respond with FINISH."
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Who should act next? Choose one of: {options}",
        ),
    ]
).partial(options=str(options), members=", ".join(members))

# Graph state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

# Supervisor node
def supervisor_agent(state):
    supervisor_chain = prompt | llm.with_structured_output(RouteResponse)
    return supervisor_chain.invoke(state)

# Build graph
def create_supervisor_graph():

    research_agent = create_react_agent(llm, tools=[tavily_tool])
    research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")

    coder_agent = create_react_agent(llm, tools=[python_repl_tool])
    coder_node = functools.partial(agent_node, agent=coder_agent, name="Coder")

    workflow = StateGraph(AgentState)

    workflow.add_node("Researcher", research_node)
    workflow.add_node("Coder", coder_node)
    workflow.add_node("supervisor", supervisor_agent)

    for member in members:
        workflow.add_edge(member, "supervisor")

    conditional_map = {k: k for k in members}
    conditional_map["FINISH"] = END

    workflow.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        conditional_map
    )

    workflow.add_edge(START, "supervisor")

    return workflow.compile()

# Run example
def main():
    graph = create_supervisor_graph()

    print("\nExample 1: Coding Task\n")

    for step in graph.stream(
        {
            "messages": [
                HumanMessage(content="Write python code for hello world")
            ]
        }
    ):
        if "__end__" not in step:
            print(step)
            print("----")

    print("\nExample 2: Research Task\n")

    for step in graph.stream(
        {
            "messages": [
                HumanMessage(content="Write a short research report on pikas")
            ]
        },
        {"recursion_limit": 100},
    ):
        if "__end__" not in step:
            print(step)
            print("----")


if __name__ == "__main__":
    main()