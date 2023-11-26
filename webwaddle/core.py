from typing import List
from langchain.agents import AgentType, AgentExecutor, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, DuckDuckGoSearchResults, DuckDuckGoSearchRun
from pydantic import BaseModel, HttpUrl
from dotenv import load_dotenv
import re

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
# Search result
class SearchResult(BaseModel):
    snippet: str
    title: str
    link: HttpUrl

# List of search results 
class SearchResults(BaseModel):
    results: List[SearchResult]

# Summary prompt input
class SummaryInput(BaseModel):
    snippets: List[str]
    context: str
    question: str

# Define the tool
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
        results = self.run_search(query)
        print(results)

        summary = self.summarize_results(results)
        print(summary)

        return summary
    
    def run_search(self, query: str) -> SearchResults:
        # Use DuckDuckGo to search for the query 
        raw_results = search.run(query)

        print("RAW: " + raw_results)

        # Parse the string to extract relevant information
        pattern = r"snippet: (.*?), title: (.*?), link: (.*?)(?:, \[|$)"
        matches = re.findall(pattern, raw_results)

        print(matches)

        processed_results = []
        for snippet, title, link in matches:
            try:
                processed_results.append(SearchResult(snippet=snippet, title=title, link=link))
            except TypeError as e:
                print(f"Error processing result: {e}")

        return SearchResults(results=processed_results)
    
    def summarize_results(self, search_results: SearchResults) -> str:
        # Gather and concatenate all search results
        snippets = [r.snippet for r in search_results.results]
        context = ' | Next Page | '.join(snippets)

        # Summarize the search results
        summary_input = SummaryInput(snippets=snippets, context=context, question="Who is the current CEO of OpenAI?")
        try:
            summary = llm.generate(
                summary_prompt_template,
                context=summary_input.context,
                question=summary_input.question,
                max_tokens=750,
            )
        except TypeError as e:
            print(f"Error generating summary: {e}")
            return "Error in generating summary."

        return summary

# For testing purposes  
tools = [SearchTool()]
search_agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True
)

search_agent.invoke({"input": "Who is the current CEO of OpenAI?"})