# arxiv_search.py

from llama_index import GPTIndex, QueryTool

class ArxivAgent:
    """Agent for academic paper searches."""

    def __init__(self):
        self.index = GPTIndex(schema={"title": str, "abstract": str, "arxiv_id": str})
        self.query_tool = QueryTool(index=self.index)

    def search_papers(self, keywords: str):
        return self.query_tool.query({"keywords": keywords})

"""
This file contains the `ArxivAgent` class for searching academic papers using keywords,
helping locate relevant research in an indexed dataset.
"""
