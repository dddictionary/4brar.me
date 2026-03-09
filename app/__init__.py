import os
from datetime import datetime

from dotenv import load_dotenv  # type: ignore
from flask import Flask, render_template, request, jsonify  # type: ignore
from peewee import *
from playhouse.shortcuts import model_to_dict

from prometheus_flask_exporter import PrometheusMetrics  # type: ignore

load_dotenv()
app = Flask(__name__)
metrics = PrometheusMetrics(app)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )

print(mydb)


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])

# In test mode, keep the connection open — SQLite in-memory DB loses all
# data (including tables) when the last connection closes.
# In production, close the startup connection and manage connections
# per-request so MariaDB receives a clean COM_QUIT after each request,
# preventing "Aborted connection" warnings in the logs.
if os.getenv("TESTING") != "true":
    mydb.close()

    @app.before_request
    def before_request():
        mydb.connect(reuse_if_open=True)

    @app.teardown_request
    def teardown_request(exc):
        if not mydb.is_closed():
            mydb.close()


@app.context_processor
def nav_items():
    navitems = [
        # {"href": "/", "caption": "About"},
        {"href": "/aboutme", "caption": "About Me"},
        {"href": "/work", "caption": "Work Experiences"},
        {"href": "/hobbies", "caption": "Hobbies"},
        {"href": "/education", "caption": "Education"},
        {"href": "/travels", "caption": "Travels"},
        {"href": "/timeline", "caption": "Timeline"},
    ]
    return {"navigation": navitems}


@app.context_processor
def hobby_items():
    hobbyitems = [
        {
            "title": "Soccer",
            "description": "Whether it's a pickup game or watching a match, soccer has always been my go-to sport. Nothing beats the flow of a good game.",
            "source": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=500&h=500&fit=crop",
        },
        {
            "title": "Rock Climbing",
            "description": "Bouldering is my favorite way to problem-solve off the keyboard. Every route is a puzzle that demands both strength and strategy.",
            "source": "https://images.unsplash.com/photo-1522362485439-83fcff4673f0?w=500&h=500&fit=crop",
        },
        {
            "title": "Driving",
            "description": "Long drives with good music are underrated. There's something about the open road that clears the mind.",
            "source": "https://images.unsplash.com/photo-1449965408869-ebd13bc9e5a8?w=500&h=500&fit=crop",
        },
        {
            "title": "Coding",
            "description": "Building things in my free time is how I stay sharp and explore new ideas. This website is one of those projects.",
            "source": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=500&h=500&fit=crop",
        },
    ]
    return {"hobbies": hobbyitems}


@app.context_processor
def work_experiences():
    work_data = [
        {
            "title": "Shopify",
            "role": "Engineering Intern",
            "startdate": "Sep 2025",
            "enddate": "Present",
            "description": "Led Tier 1 migration of transactional messaging pipeline from single-region to dual-region using Kubernetes overlay architecture. Developed static analysis tooling that identified 40+ security vulnerabilities across 330K+ lines of Ruby code.",
        },
        {
            "title": "Meta",
            "role": "Production Engineering Fellow",
            "startdate": "Jun 2025",
            "enddate": "Sep 2025",
            "description": "Deployed containerized web application using Docker and Nginx reverse proxy for production workloads. Implemented monitoring and alerting stack with Prometheus and Grafana.",
        },
        {
            "title": "ACM CCNY",
            "role": "Backend Engineer & Teaching Assistant",
            "startdate": "Jun 2024",
            "enddate": "Aug 2025",
            "description": "Built fault-tolerant Node.js backend handling 10GB+ across 5+ databases with automated daily backups. Led team of 5 to deliver MERN MVP in 8 weeks using sprint planning and agile workflows.",
        },
    ]
    return {"work": work_data}


@app.context_processor
def education_experiences():
    education_data = [
        {
            "title": "CUNY City College of New York",
            "startdate": "Aug 2022",
            "enddate": "Dec 2025",
            "description": "Bachelor of Science in Computer Science. Relevant coursework in Data Structures, Algorithms, Operating Systems, Computer Networks, and Database Systems.",
        },
    ]
    return {"education": education_data}


@app.context_processor
def travel_experiences():
    locations = [
        {"name": "Paris, France", "lat": 48.8566, "lng": 2.3522},
        {"name": "New York, USA", "lat": 40.7128, "lng": -74.0060},
        {"name": "Tokyo, Japan", "lat": 35.6895, "lng": 139.6917},
        {"name": "London, UK", "lat": 51.5074, "lng": -0.1278},
        {"name": "Los Angeles, USA", "lat": 34.0522, "lng": -118.2437},
        {"name": "São Paulo, Brazil", "lat": -23.5505, "lng": -46.6333},
        {"name": "Cairo, Egypt", "lat": 30.0444, "lng": 31.2357},
        {"name": "Dubai, UAE", "lat": 25.2048, "lng": 55.2708},
        {"name": "Istanbul, Turkey", "lat": 41.0082, "lng": 28.9784},
        {"name": "Bangkok, Thailand", "lat": 13.7563, "lng": 100.5018},
        {"name": "Seoul, South Korea", "lat": 37.5665, "lng": 126.9780},
        {"name": "Sydney, Australia", "lat": -33.8688, "lng": 151.2093},
        {"name": "Mexico City, Mexico", "lat": 19.4326, "lng": -99.1332},
    ]
    return {"locations": locations}


@app.route("/")
def index():
    return render_template("index.html", title="Abrar Habib", url=os.getenv("URL"))


@app.route("/hobbies")
def hobbies():
    return render_template(
        "hobbies.html", title="Abrar Habib —Hobbies", url=os.getenv("URL")
    )


@app.route("/aboutme")
def aboutme():
    return render_template(
        "aboutme.html", title="Abrar Habib —About Me", url=os.getenv("URL")
    )


@app.route("/work")
def work():
    return render_template(
        "work.html", title="Abrar Habib —Work Experiences", url=os.getenv("URL")
    )


@app.route("/education")
def education():
    return render_template(
        "education.html", title="Abrar Habib —Education", url=os.getenv("URL")
    )


@app.route("/travels")
def travels():
    return render_template(
        "travel.html", title="Abrar Habib —Travels", url=os.getenv("URL")
    )


@app.route("/api/timeline_post", methods=["POST"])
def post_timeline_post():
    name = request.form.get("name")
    email = request.form.get("email")
    content = request.form.get("content")
    if (
        (not email)
        or (not isinstance(email, str))
        or (len(email) <= 0)
        or ("@" not in email)
    ):
        return "Invalid email", 400
    if (not name) or (not isinstance(name, str)) or (len(name) <= 0):
        return "Invalid name", 400
    if (not content) or (not isinstance(content, str)) or (len(content) <= 0):
        return "Invalid content", 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route("/api/timeline_post", methods=["GET"])
def get_timeline_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route("/timeline")
def timeline():
    return render_template("timeline.html", title="Timeline")

@app.route("/api/test-ci", methods=["GET"])
def test_ci():
    return jsonify("ci should be working and this endpoint should be reachable")


# TODO: Add a delete endpoint here and write logic for it here.
