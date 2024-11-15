# search.py

from llama_index import GPTIndex

class SearchAgent:
    """Performs searches on indexed content."""

    def __init__(self):
        self.index = GPTIndex(schema={"title": str, "summary": str})

    def search(self, query: str):
        return self.index.query({"title": query})

"""
This file defines a `SearchAgent` class to perform searches on indexed content,
retrieving results based on a title query.
"""
