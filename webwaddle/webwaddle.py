from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, DuckDuckGoSearchResults, DuckDuckGoSearchRun
from langchain.schema.output_parser import StrOutputParser
# Import Prompt template
from webwaddle.prompts import summary_prompt_template
# Import Pydantic data structures
from data_model import SearchResult, SearchResults, SummaryInput
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
result_search = DuckDuckGoSearchResults()
page_search = DuckDuckGoSearchRun()

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
        except TypeError as E:
            print(f"Error generating summary: {E}")
            return "Error in generating summary."

        return summary
