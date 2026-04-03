from fastapi import APIRouter, Form, HTTPException
from prometheus_client import Counter, generate_latest

from app.database import get_pool
from app.models import create_post, get_all_posts

router = APIRouter()

POSTS_CREATED = Counter("timeline_posts_created_total", "Total timeline posts created")


@router.get("/api/timeline_post")
async def get_timeline_posts():
    pool = await get_pool()
    posts = await get_all_posts(pool)
    return {"timeline_posts": posts}


@router.post("/api/timeline_post")
async def post_timeline_post(
    name: str = Form(default=""),
    email: str = Form(default=""),
    content: str = Form(default=""),
):
    if not name.strip():
        raise HTTPException(status_code=400, detail="Invalid name")
    if not email.strip() or "@" not in email:
        raise HTTPException(status_code=400, detail="Invalid email")
    if not content.strip():
        raise HTTPException(status_code=400, detail="Invalid content")

    pool = await get_pool()
    post = await create_post(pool, name, email, content)
    POSTS_CREATED.inc()
    return post


@router.get("/api/test-ci")
async def test_ci():
    return "ci should be working and this endpoint should be reachable"


@router.get("/metrics")
async def metrics_handler():
    from fastapi.responses import PlainTextResponse

    return PlainTextResponse(generate_latest().decode())
