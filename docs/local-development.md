# Local Development

## Option A — Native (recommended for development)

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (`brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- MySQL-compatible server — MariaDB or Percona via Homebrew

### 1. Set up Python environment

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Test dependencies
uv pip install pytest pytest-asyncio httpx
```

### 2. Set up the database

Install MariaDB (or use an existing MySQL-compatible server like Percona):

```bash
brew install mariadb
brew services start mariadb
```

> **Note:** If you already have `percona-server@8.0` or another MySQL server installed, you can use that instead — just `brew services start percona-server@8.0`.

Create the database and set a password:

```bash
mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'secret';"
mysql -u root -psecret -e "CREATE DATABASE IF NOT EXISTS portfolio;"
```

### 3. Configure environment

```bash
cp example.env .env
```

Edit `.env`:

```
URL=localhost:5000
MYSQL_HOST=127.0.0.1
MYSQL_USER=root
MYSQL_PASSWORD=secret
MYSQL_DATABASE=portfolio
```

### 4. Start the app

```bash
source .venv/bin/activate
uvicorn app.main:app --port 5000 --reload
```

The app runs migrations automatically on startup (from `migrations/`). Open [http://localhost:5000](http://localhost:5000).

### 5. Run tests

Tests mock the database — no MySQL needed:

```bash
python -m pytest tests/ -v
```

---

## Option B — Docker Compose

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose

### 1. Configure environment

```bash
cp example.env .env
```

Edit `.env`:

```
URL=localhost:5000
MYSQL_HOST=mysql
MYSQL_USER=dev
MYSQL_PASSWORD=dev
MYSQL_DATABASE=portfolio
MARIADB_ROOT_PASSWORD=rootpass
```

> **Note:** `MYSQL_HOST=mysql` refers to the Docker service name, not localhost.

### 2. Build and start

```bash
docker compose up --build
```

### 3. Stop

```bash
docker compose down

# To also wipe the database volume:
docker compose down -v
```

---

## Verifying It Works

Once the app is running, check these routes:

| Route | What to look for |
|-------|-----------------|
| `/` | Hero section with name and bio |
| `/aboutme` | About me content |
| `/work` | Work experience cards |
| `/education` | Education card |
| `/hobbies` | Hobby cards with images |
| `/travels` | Interactive map with location markers |
| `/timeline` | Post form + feed |
| `/metrics` | Prometheus metrics output |

Test the timeline API:

```bash
# Create a post
curl -X POST http://localhost:5000/api/timeline_post \
  -d "name=Test&email=test@example.com&content=Hello"

# List posts
curl http://localhost:5000/api/timeline_post
```

## Adding Content

Create a new SQL migration file in `migrations/`:

```bash
cat > migrations/003_add_new_job.sql << 'EOF'
INSERT IGNORE INTO work_experiences (title, role, startdate, enddate, description)
VALUES ('New Company', 'Software Engineer', 'Jan 2026', 'Present', 'Description here.');
EOF
```

Migrations run automatically on startup. `INSERT IGNORE` ensures they're idempotent — restarting the app won't duplicate data.
