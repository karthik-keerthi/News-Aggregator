#News_Api.py

from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import csv
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Enable CORS to allow cross-origin requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers in requests
)

# Define the Article model for the API
class Article(BaseModel):
    id: int
    title: str
    summary: str
    url: str
    source: str
    publication_date: str
    category: str

# List to hold all the articles after loading from CSV
articles = []

def load_articles():
    """
    Load articles from the 'categorized_news_articles.csv' file
    and populate the 'articles' list.
    """
    with open('categorized_news_articles.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader, start=1):
            articles.append(Article(id=idx, **row))  # Append each article as an Article object

# Event hook to load articles when the app starts up
@app.on_event("startup")
async def startup_event():
    load_articles()  # Load articles into memory when the API starts

# Endpoint to get all articles or filter based on category and/or date range
@app.get("/articles", response_model=List[Article])
async def get_articles(
    category: Optional[str] = None,  # Optional category filter
    start_date: Optional[str] = None,  # Optional start date filter (YYYY-MM-DD)
    end_date: Optional[str] = None  # Optional end date filter (YYYY-MM-DD)
):
    filtered_articles = articles  # Start with all articles

    # Filter by category if provided
    if category:
        filtered_articles = [a for a in filtered_articles if a.category.lower() == category.lower()]
    
    # Filter by start date if provided
    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        filtered_articles = [a for a in filtered_articles if datetime.strptime(a.publication_date, "%Y-%m-%d") >= start]
    
    # Filter by end date if provided
    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d")
        filtered_articles = [a for a in filtered_articles if datetime.strptime(a.publication_date, "%Y-%m-%d") <= end]

    return filtered_articles  # Return the filtered articles list

# Endpoint to get a single article by its ID
@app.get("/articles/{article_id}", response_model=Article)
async def get_article(article_id: int):
    """
    Get a specific article by its ID.
    Raise a 404 error if the article is not found.
    """
    for article in articles:
        if article.id == article_id:  # Find the article by its ID
            return article
    raise HTTPException(status_code=404, detail="Article not found")  # Return 404 if not found

# Endpoint to search articles based on a query string
@app.get("/search", response_model=List[Article])
async def search_articles(q: str = Query(..., min_length=3)):
    """
    Search articles based on the query string.
    It searches both the title and summary fields.
    """
    results = [
        article for article in articles
        if q.lower() in article.title.lower() or q.lower() in article.summary.lower()
    ]
    return results  # Return the search results

# Main entry point to run the FastAPI app using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Run the app on localhost, port 8000
