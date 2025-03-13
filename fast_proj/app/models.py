from pydantic import BaseModel, Field
from typing import Optional

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)

class QueryResponse(BaseModel):
    message: str
    query: str

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=100, max_length=10000)
    max_length: Optional[int] = Field(default=130, ge=30, le=500)
    min_length: Optional[int] = Field(default=30, ge=10, le=100)

class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int