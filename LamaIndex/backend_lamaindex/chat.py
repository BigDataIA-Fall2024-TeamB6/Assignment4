# chat.py

from llama_index import GPTIndex, Document
from llama_index.query_tools import QueryTool

class ChatAgent:
    """Handles chat-based interactions."""

    def __init__(self):
        self.index = GPTIndex(schema={"question": str, "response": str})
        self.query_tool = QueryTool(index=self.index)

    def chat_response(self, question: str):
        query = {"question": question}
        return self.query_tool.query(query)

"""
This file contains a `ChatAgent` class to handle user chat interactions using stored questions
and responses, providing FAQ-style responses efficiently.
"""
