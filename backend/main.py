from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from routers import users_router, posts_router, comments_likes_router

app = FastAPI(
    title="Social Media API",
    version="1.0.0",
    description="A FastAPI-based social media backend with user and post management, ML hashtag/mention extraction, and monitoring.",
    openapi_tags=[
        {
            "name": "Users",
            "description": "Operations with users: create, read, update, delete, and list posts by user."
        },
        {
            "name": "Posts",
            "description": "Operations with posts: create, read, update, delete, filter, and paginate posts."
        },
        {
            "name": "Likes & Comments",
            "description": "Like/unlike posts and add/edit/delete comments."
        }
    ]
)

@app.get("/", tags=["Info"], summary="API Root", response_description="Welcome message")
def read_root():
    """Root endpoint for API health and welcome message."""
    return {"message": "Welcome to the Social Media API!"}

@app.get("/metrics", tags=["Monitoring"], summary="Prometheus Metrics", response_description="Prometheus metrics for monitoring.")
def metrics():
    """Prometheus metrics endpoint for monitoring."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

app.include_router(users_router)
app.include_router(posts_router)
app.include_router(comments_likes_router) 