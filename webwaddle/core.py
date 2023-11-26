from typing import List
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, DuckDuckGoSearchResults
from pydantic import BaseModel, HttpUrl
from dotenv import load_dotenv

# Load OpenAI_API_KEY from env
load_dotenv()

# Set llm to ChatOpenAI Model
llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo-1106"
)

# Set search to DuckDuckGo
search = DuckDuckGoSearchResults()

# Type definitions 
class SearchResult(BaseModel):
    snippet: str
    title: str
    link: HttpUrl

class SearchResults(BaseModel):
    results: List[SearchResult]

class SummaryInput(BaseModel):
    snippets: List[str]
    context: str
    question: str

from utils import summary_prompt_template
class SearchTool(BaseTool):
    """
    A tool for performing searches using DuckDuckGo and summarizing the results.

    This tool is designed to search for information relevant to current events or to verify critical information. 
    It queries DuckDuckGo with a given search term, retrieves the results, and then summarizes these results to provide a concise overview.
    """
    name = "search"
    description = "useful for when you need to answer questions about current events, or verify critical information"

    def _run(self, query: str) -> str:
        """Use the tool."""
        def run_search(self, query: str) -> SearchResults:
            # Use DuckDuckGo to search for the query
            raw_results = search.run(query)
            return SearchResults(results=[SearchResult(**result) for result in raw_results])
        
        def summarize_results(self, search_results: SearchResults) -> str:
            # Gather and concatenate all search results
            snippets = [r.snippet for r in search_results.results]
            context = ' | Next Page | '.join(snippets)

            # Summarize the search results
            summary_input = SummaryInput(snippets=snippets, context=context, question=query)
            summary = llm.generate(
                summary_prompt_template,
                context=summary_input.context,
                question=summary_input.question,
                max_tokens=750,
            )

            return summary
        
        results = run_search(query)
        print(results)

        summary = summarize_results(results)
        print(summary)

        return run_search

# For testing purposes  
tools = [SearchTool()]
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent.run(
    "Who is the current CEO of OpenAI?"
)