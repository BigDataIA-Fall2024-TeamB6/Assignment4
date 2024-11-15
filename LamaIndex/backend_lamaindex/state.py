# state.py

from typing import List, TypedDict

class Resource(TypedDict):
    url: str
    title: str
    description: str

class Log(TypedDict):
    message: str
    done: bool

class AgentState:
    model: str
    research_question: str
    report: str
    resources: List[Resource]
    logs: List[Log]

"""
This file defines data structures for `Resource`, `Log`, and `AgentState` to
store state information such as resources, logs, and other operational data.
"""
