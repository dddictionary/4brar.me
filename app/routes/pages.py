import json
import os

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

from app.data import NAV_ITEMS, get_education, get_hobbies, get_locations, get_work_experiences
from app.database import get_pool

router = APIRouter()

templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)
env.filters["json_encode"] = lambda v: json.dumps(v)


def render(template_name: str, **context) -> HTMLResponse:
    template = env.get_template(template_name)
    html = template.render(navigation=NAV_ITEMS, **context)
    return HTMLResponse(html)


@router.get("/", response_class=HTMLResponse)
async def index():
    url = os.environ.get("URL", "http://localhost:5000")
    return render("index.html", title="Abrar Habib", url=url, request_path="/")


@router.get("/aboutme", response_class=HTMLResponse)
async def aboutme():
    url = os.environ.get("URL", "http://localhost:5000")
    return render("aboutme.html", title="Abrar Habib \u2014 About Me", url=url, request_path="/aboutme")


@router.get("/work", response_class=HTMLResponse)
async def work():
    pool = await get_pool()
    work_items = await get_work_experiences(pool)
    url = os.environ.get("URL", "http://localhost:5000")
    return render("work.html", title="Abrar Habib \u2014 Work Experiences", url=url, request_path="/work", work=work_items)


@router.get("/education", response_class=HTMLResponse)
async def education():
    pool = await get_pool()
    edu_items = await get_education(pool)
    url = os.environ.get("URL", "http://localhost:5000")
    return render("education.html", title="Abrar Habib \u2014 Education", url=url, request_path="/education", education=edu_items)


@router.get("/hobbies", response_class=HTMLResponse)
async def hobbies():
    pool = await get_pool()
    hobby_items = await get_hobbies(pool)
    url = os.environ.get("URL", "http://localhost:5000")
    return render("hobbies.html", title="Abrar Habib \u2014 Hobbies", url=url, request_path="/hobbies", hobbies=hobby_items)


@router.get("/travels", response_class=HTMLResponse)
async def travels():
    pool = await get_pool()
    location_items = await get_locations(pool)
    url = os.environ.get("URL", "http://localhost:5000")
    return render("travel.html", title="Abrar Habib \u2014 Travels", url=url, request_path="/travels", locations=location_items)


@router.get("/timeline", response_class=HTMLResponse)
async def timeline():
    url = os.environ.get("URL", "http://localhost:5000")
    return render("timeline.html", title="Timeline", url=url, request_path="/timeline")
