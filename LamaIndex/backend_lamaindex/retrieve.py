# retrieve.py

from llama_index import GPTIndex

class RetrieveAgent:
    """Retrieves documents by keywords."""

    def __init__(self):
        self.index = GPTIndex(schema={"keywords": str, "document_id": str})

    def retrieve_document(self, keywords):
        return self.index.query({"keywords": keywords})

"""
This file contains a `RetrieveAgent` class that retrieves documents by keywords,
using an index to store and locate documents based on keyword search.
"""
