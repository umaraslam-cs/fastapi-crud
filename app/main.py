from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Union

app = FastAPI()

# Request model (no 'id' field)
class ArticleCreate(BaseModel):
    name: str
    price: float

# Response model (includes 'id' field)
class Article(ArticleCreate):
    id: int

# Response structure for all endpoints
class ResponseModel(BaseModel):
    success: bool
    data: Union[List[Article], Article, None]  # Can be a list, a single article, or None
    message: Union[str, None] = None  # Optional message

# Initialize an empty list to store articles
articles = []

# Initialize an id counter
current_id = 1

# Step 4: Create routes and CRUD handlers

# Read all articles
@app.get("/articles", response_model=ResponseModel)
async def read_articles():
    return ResponseModel(success=True, data=articles, message="Articles fetched successfully")

# Create a new article (id is auto-generated here)
@app.post("/articles", response_model=ResponseModel)
async def create_article(article: ArticleCreate):
    global current_id  # Use the global counter for id generation
    
    # Create the new article with an auto-generated ID
    new_article = {**article.model_dump(), "id": current_id}
    
    # Append the new article to the list
    articles.append(new_article)
    
    # Increment the ID counter for the next article
    current_id += 1
    
    return ResponseModel(success=True, data=new_article, message="Article created successfully")

# Update an existing article
@app.put("/articles/{article_id}", response_model=ResponseModel)
async def update_article(article_id: int, article: ArticleCreate):
    # Find the article by id and update it
    for index, existing_article in enumerate(articles):
        if existing_article["id"] == article_id:
            articles[index] = {**article.model_dump(), "id": article_id}  # Keep the same ID
            return ResponseModel(success=True, data=articles[index], message="Article updated successfully")
    return ResponseModel(success=False, data=None, message="Article not found")

# Delete an article
@app.delete("/articles/{article_id}", response_model=ResponseModel)
async def delete_article(article_id: int):
    # Find the article by id and delete it
    for index, existing_article in enumerate(articles):
        if existing_article["id"] == article_id:
            del articles[index]
            return ResponseModel(success=True, data=None, message="Article deleted successfully")
    return ResponseModel(success=False, data=None, message="Article not found")
