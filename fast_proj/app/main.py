from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
import asyncio
from app.services.summarizer import TextSummarizer
from app.utils.logger import setup_logger
from app.models import QueryRequest, SummarizeRequest, QueryResponse, SummarizeResponse

logger = setup_logger()

app = FastAPI(
    title="AI Text Summarization API",
    description="A FastAPI microservice for text summarization using open-source AI models",
    version="1.0.0"
)

# Thread-safe storage for queries
queries: List[str] = []
queries_lock = asyncio.Lock()  # Prevent concurrent modification issues

summarizer = TextSummarizer()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        logger.info(f"Processing query request: {request.query}")

        async with queries_lock:
            queries.append(request.query)  # Store the query safely

        return QueryResponse(
            message="Query processed successfully",
            query=request.query
        )
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize_text(request: SummarizeRequest):
    try:
        logger.info(f"Processing summarization request, text length: {len(request.text)}")
        
        if len(request.text) < 100:
            raise HTTPException(status_code=400, detail="Text too short for summarization")
            
        summary = await summarizer.summarize(
            request.text,
            max_length=request.max_length or 130,
            min_length=request.min_length or 30
        )
        
        return SummarizeResponse(
            original_length=len(request.text),
            summary_length=len(summary),
            summary=summary
        )
    except Exception as e:
        logger.error(f"Error during summarization: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/queries", response_model=List[str])
async def get_all_queries():
    try:
        logger.info("Fetching all stored queries")
        
        async with queries_lock:
            if queries is None:  # Safety check
                raise HTTPException(status_code=500, detail="Query list is uninitialized")
            
            if not queries:
                return []  # Return an empty list instead of throwing an error
        
        return queries  # Return stored queries
    except Exception as e:
        logger.error(f"Error fetching queries: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving queries")
