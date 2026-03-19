import functools
import operator
import os
from typing import Annotated, Literal, Sequence, TypedDict

from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL
from langchain_groq import ChatGroq
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode

# Load environment variables
load_dotenv()

# Disable LangSmith tracing to avoid API error
os.environ["LANGCHAIN_TRACING_V2"] = "false"

# ---------------- TOOLS ---------------- #

tavily_tool = TavilySearch(max_results=5)
repl = PythonREPL()

@tool
def python_repl(code: str):
    """Execute Python code for calculations or charts."""
    try:
        result = repl.run(code)
    except Exception as e:
        return f"Execution failed: {repr(e)}"

    return f"Executed code:\n```python\n{code}\n```\nOutput:\n{result}"

# ---------------- AGENT CREATOR ---------------- #

def create_agent(llm, tools, system_message: str):

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an AI assistant collaborating with other assistants.\n"
                "Use tools when needed.\n"
                "If the task is finished respond with FINAL ANSWER.\n"
                "Available tools: {tool_names}\n"
                "{system_message}",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    prompt = prompt.partial(
        tool_names=", ".join([tool.name for tool in tools]),
        system_message=system_message,
    )

    return prompt | llm.bind_tools(tools)

# ---------------- STATE ---------------- #

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str

# ---------------- AGENT NODE ---------------- #

def agent_node(state, agent, name):

    result = agent.invoke(state)

    if isinstance(result, ToolMessage):
        return {"messages": [result], "sender": name}

    result = AIMessage(**result.model_dump(exclude={"type", "name"}), name=name)

    return {
        "messages": [result],
        "sender": name,
    }

# ---------------- ROUTER ---------------- #

def router(state) -> Literal["call_tool", "__end__", "continue"]:

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "call_tool"

    if "FINAL ANSWER" in last_message.content:
        return "__end__"

    return "continue"

# ---------------- GRAPH ---------------- #

def create_multi_agent_graph():

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    research_agent = create_agent(
        llm,
        [tavily_tool],
        "Provide accurate GDP data.",
    )

    chart_agent = create_agent(
        llm,
        [python_repl],
        "Generate charts using Python.",
    )

    research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")
    chart_node = functools.partial(agent_node, agent=chart_agent, name="ChartGenerator")

    tool_node = ToolNode([tavily_tool, python_repl])

    workflow = StateGraph(AgentState)

    workflow.add_node("Researcher", research_node)
    workflow.add_node("ChartGenerator", chart_node)
    workflow.add_node("call_tool", tool_node)

    workflow.add_conditional_edges(
        "Researcher",
        router,
        {
            "continue": "ChartGenerator",
            "call_tool": "call_tool",
            "__end__": END,
        },
    )

    workflow.add_conditional_edges(
        "ChartGenerator",
        router,
        {
            "continue": "Researcher",
            "call_tool": "call_tool",
            "__end__": END,
        },
    )

    workflow.add_conditional_edges(
        "call_tool",
        lambda x: x["sender"],
        {
            "Researcher": "Researcher",
            "ChartGenerator": "ChartGenerator",
        },
    )

    workflow.add_edge(START, "Researcher")

    return workflow.compile()

# ---------------- MAIN ---------------- #

def main():

    graph = create_multi_agent_graph()

    print("\nExample: UK GDP Analysis\n")

    events = graph.stream(
        {
            "messages": [
                HumanMessage(
                    content="UK GDP last 2 years. Create line chart."
                )
            ]
        },
        {"recursion_limit": 100},
    )

    for step in events:
        print(step)
        print("----")

if __name__ == "__main__":
    main()