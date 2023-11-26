from langchain.prompts import ChatPromptTemplate

# Query 
QUERY_PROMPT = """"Given the question: '{question}', write 3 unique Google search queries that will help 
in forming an objective opinion or understanding.\n
Ensure that your queries are diverse and cover different aspects or perspectives related to the question. 
Format your response in PROPER JSON FORMAT as it will be parsed using json.loads(). 
Respond with a list of strings in the following format: '["query 1", "query 2", "query 3"]. 
Please think carefully, the quality of these queries is crucial for my career."
"""
    
query_prompt_template = ChatPromptTemplate.from_template(QUERY_PROMPT)

# Summarize
