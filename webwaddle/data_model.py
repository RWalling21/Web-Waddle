from pydantic import BaseModel, HttpUrl
from typing import List

# Search result
class SearchResult(BaseModel):
    snippet: str
    title: str
    link: HttpUrl

# List of search results 
class SearchResults(BaseModel):
    results: List[SearchResult]
