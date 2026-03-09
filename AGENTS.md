# AGENTS.md

## Workflow

- **Never commit directly to `main`** unless it's an emergency hotfix.
- Create a feature branch off `main` (e.g., `feat/add-hobbies`, `fix/nginx-ssl`).
- Make your changes, commit, push, and open a PR against `main`.
- CI must pass before merging.

## Commits

- Keep commit messages short and descriptive (e.g., `feat: update work experiences`, `fix: correct nginx ssl paths`).
- Do not append "Co-Authored-By" or "Created by Claude" to commit messages.

## Project Structure

```
app/
  __init__.py          # All routes, models, and content (context processors)
  templates/           # Jinja2 templates (base.html + page templates)
  static/              # CSS, JS, images
tests/
  test_app.py          # Route tests
  test_db.py           # Timeline/database tests
monitoring/            # Prometheus + Grafana config and dashboards
user_conf.d/           # Nginx reverse proxy config
```

## Testing

Tests use Python `unittest` with an in-memory SQLite database (no MariaDB required).

```bash
# Set up environment (one-time)
python -m venv .venv
.venv/bin/pip install -r requirements.txt

# Run tests
TESTING=true .venv/bin/python -m unittest discover -v tests/
```

CI runs tests automatically on PRs to `main` via `.github/workflows/test.yml`. It also builds the Docker image to verify the build isn't broken.

## Deployment

Merging to `main` triggers `.github/workflows/deploy.yml`, which:
1. SSHs into the VPS
2. Pulls the latest `main`
3. Runs `docker compose -f docker-compose.prod.yml -f docker-compose.monitoring.yml down`
4. Rebuilds and starts all containers

Production stack:
- `docker-compose.prod.yml` — Flask app + MariaDB + Nginx (SSL via Let's Encrypt)
- `docker-compose.monitoring.yml` — Prometheus + Grafana + Node Exporter + cAdvisor

Site: `4brar.me` | Monitoring: `observe.4brar.me`

## Common Tasks

- **Update portfolio content**: Edit context processors in `app/__init__.py` (`work_experiences`, `education_experiences`, `hobby_items`, `travel_experiences`).
- **Change styling/layout**: Edit `app/templates/` and `app/static/styles/main.css`.
- **Add a new page**: Add a route in `app/__init__.py`, create a template extending `base.html`, add nav entry to `nav_items()`.
- **Modify infrastructure**: Docker Compose files at repo root, Nginx in `user_conf.d/`, Prometheus in `monitoring/`.
