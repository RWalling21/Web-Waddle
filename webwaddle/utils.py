from langchain.prompts import ChatPromptTemplate

# Query 
SUMMARY_PROMPT = """"{context}

------------
Based on the provided context, write a clear, concise, in-debth, and well-structured summary that includes all relevant factual information, numbers, and statistics. The summary should be specifically tailored to answer the following question:

> {question}

------------
You MUST summarize the text in a well written and clear way. Include all factual information, numbers, stats etc if available. Write as much as is necessary to fully summarize the context, but DO NOT repeat yourself.
YOU MUST cite every fact, number, stat, etc with the URL of the page that the content was taken from. YOU MUST ensure that all summarized information is the most up to date possible.
"""
    
summary_prompt_template = ChatPromptTemplate.from_template(SUMMARY_PROMPT)