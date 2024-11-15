
from pydantic import BaseModel

class DocumentRequest(BaseModel):
    query: str
    max_results: int = 5

class DocumentResponse(BaseModel):
    document_id: str
    title: str
    content: str
