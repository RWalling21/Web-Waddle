# WebWaddle

WebWaddle is a cost-free, open-source alternative to premium web scraping solutions. This tool democratizes web data extraction, offering a powerful and accessible option for comprehensive online data gathering. Leveraging the capabilities of DuckDuckGo for searching and OpenAI's GPT-3.5 for summarizing, WebWaddle provides an efficient means to extract and condense information from the web.

## Features

- **Comprehensive Search**: Utilizes DuckDuckGo to fetch relevant information from the web.
- **Advanced Summarization**: Leverages OpenAI's GPT-3.5 model to create concise and informative summaries of the search results.
- **Customizable and Extensible**: Easily adaptable to various web scraping and data summarization needs.

## Installation

Clone the repository:

\```bash
git clone https://github.com/RWalling21/Web-Waddle.git
cd Web-Waddle
\```

Install dependencies:

\```bash
pip install -r requirements.txt
\```

## Usage

To use WebWaddle, simply import the tool and call its methods in your Python scripts. Here is a basic example:

\```python
# Import WedWaddle
from webwaddle import WebWaddle
# Import Langchain Agents 
from langchain.agents import AgentType, initialize_agent

# Initialize the tool
tools = [WebWaddle]

# Initialize your agent 
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# Perform a search and summarize the results
agent.run(
    "Who is the current CEO of OpenAI?"
) 

"""
> Entering new AgentExecutor chain...
I should search for the current CEO of OpenAI.
Action: search
Action Input: "current CEO of OpenAI"
Observation: Sam Altman, the former CEO of OpenAI, was fired from his role at ChatGPT-maker OpenAI but has since returned to his post as chief executive, ending a boardroom drama that has transfixed Silicon Valley. The company is currently on its third CEO in three days, with Emmett Shear being appointed as interim CEO less than 72 hours after Altman's ouster. The board that forced Altman out has agreed to bring him back as CEO, and also agreed in principle to partly reconstitute its board. The "new initial board" will consist of Adam D'Angelo, Larry Summers, and Bret Taylor, with more board members reportedly to be added. The company is based in San Francisco and has been undergoing significant leadership changes in recent days. The information was sourced from https://www.npr.org/2023/11/22/1048490681/sam-altman-returns-as-openai-ceo.
Thought:I now know the final answer
Final Answer: Sam Altman is the current CEO of OpenAI
"""
\```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/RWalling21/Web-Waddle/LICENSE) file for details.

## Contact

For any inquiries, please reach out to me at rhw8246@rit.edu.