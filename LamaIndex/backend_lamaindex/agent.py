# agent.py

# Import necessary modules from LlamaIndex
from llama_index import VectorStoreIndex, Document 
from llama_index.query_tools import QueryTool
from typing import Dict

# Define a class to manage multiple agents
class MultiAgentManager:
    """Manages multiple agents with LlamaIndex to handle various tasks."""

    # Initialize the manager with four types of agents
    def __init__(self):
        self.agents = {
            "explore_docs": self._create_explore_docs_agent(),
            "load_document": self._create_load_document_agent(),
            "arxiv_search": self._create_arxiv_search_agent(),
            "web_search": self._create_web_search_agent()
        }

    # Define an agent for exploring documents
    def _create_explore_docs_agent(self):
        schema = {"document_id": str, "title": str, "summary": str}
        index = GPTIndex(schema=schema)
        return QueryTool(index=index)

    # Define an agent for loading specific documents
    def _create_load_document_agent(self):
        schema = {"document_id": str, "content": str}
        index = GPTIndex(schema=schema)
        return QueryTool(index=index)

    # Define an agent for searching Arxiv academic papers
    def _create_arxiv_search_agent(self):
        schema = {"title": str, "keywords": str, "abstract": str}
        index = GPTIndex(schema=schema)
        return QueryTool(index=index)

    # Define an agent for general web searches
    def _create_web_search_agent(self):
        schema = {"title": str, "url": str, "snippet": str}
        index = GPTIndex(schema=schema)
        return QueryTool(index=index)

    # Method to send a user query to the appropriate agent
    def route_request(self, agent_name: str, query: Dict):
        if agent_name not in self.agents:
            raise ValueError(f"No agent found with name {agent_name}")
        return self.agents[agent_name].query(query)

"""
This file defines a `MultiAgentManager` class that manages multiple agents, 
each performing a specific type of task. The setup organizes agents for document exploration,
loading, academic paper searches, and web searches, allowing them to handle various types of queries.
"""
