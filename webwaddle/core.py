from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, DuckDuckGoSearchResults
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from utils import summary_prompt_template

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
wrapper = DuckDuckGoSearchAPIWrapper(region="de-de", time="d", max_results=MAX_RESULTS)
search = DuckDuckGoSearchResults(wrapper=wrapper)

# Import Pydantic types
from utils import SearchResult, SearchResults, SummaryInput

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

        summary = self.summarize_results(results, query)
        print(summary)

        return summary
    
    def run_search(self, query: str) -> SearchResults:
        # Use DuckDuckGo to search for the query 
        raw_results = search.run(query)

        # Parse the string to extract relevant information
        pattern = r"snippet: (.*?), title: (.*?), link: (.*?)(?:, \[|$)"
        matches = re.findall(pattern, raw_results)

        processed_results = []
        for snippet, title, link in matches:
            try:
                processed_results.append(SearchResult(snippet=snippet, title=title, link=link))
            except TypeError as e:
                print(f"Error processing result: {e}")

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
tools = [SearchTool()]
search_agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True
)

search_agent.invoke({"input": "Who is the current CEO of OpenAI?"})