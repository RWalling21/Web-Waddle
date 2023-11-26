from typing import List
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, DuckDuckGoSearchResults

from dotenv import load_dotenv

# Load OpenAI_API_KEY from env
load_dotenv()

# Set llm to ChatOpenAI Model
llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo-1106"
)

# Set search to DuckDuckGo
search = DuckDuckGoSearchResults(backend="Educational")

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
        def run_search(query: str):
            # Use DuckDuckGo to search for the query
            return search.run(query)
        
        results = run_search(query)
        print(results)

        summary = summarize_results(results)
        print(summary)

        def summarize_results(self, results: List[dict]) -> str:
            # Gather and concatinate all search results
            snippets = [result['snippet'] for result in results]
            context = ' | Next Page | '.join(snippets)

            #Summarize the search results.
            summary = llm.generate(
                summary_prompt_template,
                context=context,
                question=query,
                max_tokens=750,
            )

            return summary

        return run_search

# For testing purposes  
tools = [SearchTool()]
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent.run(
    "Who is the current CEO of OpenAI?"
)