#!/usr/bin/env python

from langchain_community.tools.tavily_search import TavilySearchResults, TavilyAnswer
from langchain import hub


from typing import Any, AsyncIterator, Dict, List, Optional, cast

from fastapi import FastAPI
from langchain.agents import AgentExecutor, tool, load_tools, create_self_ask_with_search_agent
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.pydantic_v1 import BaseModel
from langchain.tools.render import format_tool_to_openai_function
from langchain.vectorstores import FAISS
from langchain_core.runnables import (
    ConfigurableField,
    ConfigurableFieldSpec,
    Runnable,
    RunnableConfig,
)
from langchain_core.runnables.utils import Input, Output

from langserve import add_routes
import os

from packages.research_assistant import chain as research_assistant_chain
app = FastAPI()
add_routes(app, research_assistant_chain, path="/research-assistant")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)