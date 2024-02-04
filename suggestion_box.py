from pydantic import BaseModel, Field, EmailStr
from uuid import uuid4
from typing import Optional
from pprint import pprint
from datetime import datetime

from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import pytz

chat = ChatOpenAI(temperature=0)

class Suggestion(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4().hex))
    created_at: str = Field(default_factory=lambda: datetime.now(pytz.timezone('America/Los_Angeles')).strftime("%Y-%m-%d %H:%M:%S"))
    suggestion: str
    proposed_solution: str = "No solution proposed"
    plan_is_ready: bool = False
    suggestor_name: Optional[str] = "Anonymous"
    suggestor_email: Optional[EmailStr] = "Anonymous@whatever.com"
    analysis: Optional[str] = "Analysis not yet performed"
    motivation: Optional[str] = "Motivation not yet performed"
    estimated_resources: Optional[str] = "Estimated resources not yet performed"

prompt = """You are an Aritificially Intelligent Employee Suggestion Box, Suggestion Analyzer, and Suggestion Implementer.
You are to evaluate the following suggestion and provide one unique proposed solution.
The proposed solution must be short and concise with 4 sections: Analysis (analysis of the quality of the suggestion to include completeness and the level of the suggestors involvement in the solution.), Motivation (Try to analyize the suggestors motivations), Proposed Solution, and Estimated Resources. 
Your output must be in JSON format with the named sections as keys and the proposed solution as the value.
You must base your analysis strictly on the following context:
{context}

Suggestion:
{suggestion}

"""
suggestion = Suggestion(suggestion="Add more seating")

def get_solution_prompt(suggestion: Suggestion, context: str) -> str:
    return prompt.format(context=context, suggestion=suggestion.suggestion)


def get_solution(suggestion: Suggestion, context: str) -> str:
    prompt = get_solution_prompt(suggestion, context)
    response = chat.invoke(prompt) 
    return response.content

def combine_suggestion_and_solution(suggestion: Suggestion, solution: str) -> Suggestion:
    solution_dict = json.loads(solution)
    suggestion.analysis = solution_dict["Analysis"]
    suggestion.motivation = solution_dict["Motivation"]
    suggestion.proposed_solution = solution_dict["Proposed Solution"]
    suggestion.estimated_resources = solution_dict["Estimated Resources"]
    suggestion.plan_is_ready = True
    return suggestion

def main():
    context = "The restaurant is often full and people have to wait for a table. Management has tried in the past to expand, but the developer says it's not possible. We have not looked into reservation systems, wether simple or computer based."
    solution = get_solution(suggestion, context)
    # print(solution)
    combined = combine_suggestion_and_solution(suggestion, solution)
    pprint(combined.dict())

if __name__ == "__main__":
    main()
