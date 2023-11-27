from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, DuckDuckGoSearchResults, DuckDuckGoSearchRun
from langchain.schema.output_parser import StrOutputParser

from utils import summary_prompt_template
from pydantic import BaseModel, HttpUrl
from typing import List

from dotenv import load_dotenv
import re

# Load OpenAI_API_KEY from env
load_dotenv()

# Set llm to ChatOpenAI Model
llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo-1106"
)

# SetupDuckDuckGo searcher
MAX_RESULTS = 3
result_search = DuckDuckGoSearchResults()
page_search = DuckDuckGoSearchRun()

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
class WebWaddle(BaseTool):
    """
    A tool for performing searches using DuckDuckGo and summarizing the results.

    This tool is designed to search for information relevant to current events or to verify critical information. 
    It queries DuckDuckGo with a given search term, retrieves the results, and then summarizes these results to provide a concise overview.
    """
    name = "WebWaddle Searcher"
    description = "useful for when you need to answer questions about current events, or verify critical information"

    def _run(self, query: str) -> str:
        # Find web results of running the query
        results = self.run_search(query)

        # Summarize web results for use in prompt
        return self.summarize_results(results, query)
    
    def run_search(self, query: str) -> SearchResults:
        # Use DuckDuckGo to search for the query 
        raw_results = result_search.run(query)

        # Parse the string to extract relevant information
        pattern = r"snippet: (.*?), title: (.*?), link: (.*?)(?:, \[|$)"
        matches = re.findall(pattern, raw_results)

        processed_results = []
        for snippet, title, link in matches:
            page_content = page_search.run(title)

            updated_snippet = page_content  

            processed_results.append(SearchResult(snippet=updated_snippet, title=title, link=link))

        return SearchResults(results=processed_results)
    
    def summarize_results(self, search_results: SearchResults, query: str) -> str:
        # Gather and concatenate all search results
        snippets = [r.snippet for r in search_results.results]
        context = ' | Next Result | '.join(snippets)

        # Prepare the input for the scrape_and_summarize_chain
        chain_input = {
            'context': context, 
            'question': query,
        }

        # Attempt to summarize the context
        try:
            # Adjust prompt template
            summary_prompt_template.format(context=context, question=query)

            # Summarize the search results
            scrape_and_summarize_chain = summary_prompt_template | ChatOpenAI(model="gpt-3.5-turbo-1106") | StrOutputParser() 

            # Generate summary
            summary = scrape_and_summarize_chain.invoke(chain_input)
        except TypeError as e:
            print(f"Error generating summary: {e}")
            return "Error in generating summary."

        return summary

# For testing purposes  
tools = [WebWaddle()]
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent.run(
    "Who is the current CEO of OpenAI"
)
