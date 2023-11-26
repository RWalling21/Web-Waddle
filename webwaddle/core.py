from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, DuckDuckGoSearchResults

from dotenv import load_dotenv

load_dotenv()

# Set llm to ChatOpenAI Model
llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo-1106"
)
# Set search to DuckDuckGo
search = DuckDuckGoSearchResults()

from utils import query_prompt_template

class SearchTool(BaseTool):
    name = "search"
    description = "useful for when you need to answer questions about current events, or verify critical information"

    def _run(self, query: str) -> str:
        """Use the tool."""
        def run_search(query: str):
            search.run(query)

        return query_prompt_template | run_search

# For testing purposes  
tools = [SearchTool()]
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent.run(
    "Who is the current CEO of OpenAI?"
)