from fastapi import FastAPI, Response, Request
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from routers import users_router, posts_router, comments_likes_router
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os


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

# Set up Jinja2 templates directory
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/", response_class=HTMLResponse, tags=["Info"], summary="HTML Root", response_description="HTML welcome page")
def html_root(request: Request):
    """Root endpoint serving an HTML welcome page."""
    return templates.TemplateResponse("index.html", {"request": request, "my_var": "Welcome to the Social Media API!"})

@app.get("/api", tags=["Info"], summary="API Root", response_description="Welcome message")
def read_root():
    """Root endpoint for API health and welcome message (JSON)."""
    return {"message": "Welcome to the Social Media API!"}

@app.get("/metrics", tags=["Monitoring"], summary="Prometheus Metrics", response_description="Prometheus metrics for monitoring.")
def metrics():
    """Prometheus metrics endpoint for monitoring."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/test", response_class=HTMLResponse)
def test_page(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/create_post", response_class=HTMLResponse)
def create_post_page(request: Request):
    return templates.TemplateResponse("create_post.html", {"request": request})

@app.get("/post_detail", response_class=HTMLResponse)
def post_detail_page(request: Request):
    # Example: pass a placeholder post variable
    return templates.TemplateResponse("post_detail.html", {"request": request, "post": {"title": "Sample Post", "content": "This is a sample post."}})

app.include_router(users_router)
app.include_router(posts_router)
app.include_router(comments_likes_router) 

