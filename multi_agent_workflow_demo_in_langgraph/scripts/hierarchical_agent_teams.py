import functools
import operator
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Annotated, Dict, List, Optional, TypedDict

from dotenv import load_dotenv

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.tools.tavily_search import TavilySearchResults

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool

from langchain_experimental.utilities import PythonREPL

from langchain_groq import ChatGroq

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import create_react_agent


def create_team_supervisor(llm: ChatGroq, system_prompt: str, members: List[str]):
    """Create a supervisor agent for a team."""
    options = ["FINISH"] + members

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Given the conversation above, who should act next?"
                " Or should we FINISH? Select one of: {options}"
                "\nRespond with ONLY the name of the next role or FINISH.",
            ),
        ]
    ).partial(options=str(options), team_members=", ".join(members))

    def parse_output(message) -> dict:
        """Parse the output to get the next role."""
        if hasattr(message, "content"):
            output = message.content.strip()
        else:
            output = str(message).strip()

        if output not in options:
            print(f"Warning: Invalid output '{output}', defaulting to FINISH")
            return {"next": "FINISH"}
        return {"next": output}

    chain = prompt | llm | parse_output
    return chain