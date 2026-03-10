# Local Development

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- (Optional) [Rust toolchain](https://rustup.rs/) if you want to build outside Docker

## Quick Start

1. Create a `.env` file at the repo root:

```
MYSQL_DATABASE=portfolio
MYSQL_USER=dev
MYSQL_PASSWORD=dev
MYSQL_HOST=mysql
MARIADB_ROOT_PASSWORD=rootpass
URL=localhost:5000
```

2. Build and start everything:

```bash
docker compose up --build
```

3. Open [http://localhost:5000](http://localhost:5000) in your browser.

The app and MariaDB will start together. Database tables are created and seeded automatically via the migration files in `migrations/`.

## Verifying It Works

Once the app is running, check these routes:

| Route | What to look for |
|-------|-----------------|
| `/` | Hero section with name and bio |
| `/aboutme` | About me content |
| `/work` | Work experience cards (pulled from DB) |
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

## Building Without Docker

If you have Rust installed locally, you can build and run the binary directly. You'll need a running MariaDB instance.

```bash
# Build
cargo build --release

# Set env vars (point to your local MariaDB)
export MYSQL_USER=dev
export MYSQL_PASSWORD=dev
export MYSQL_HOST=127.0.0.1
export MYSQL_DATABASE=portfolio
export URL=localhost:5000

# Run
./target/release/backend
```

## Adding Content

To add new content (hobby, job, location, etc.), create a new SQL migration file:

```bash
# Example: adding a new work experience
cat > migrations/003_add_new_job.sql << 'EOF'
INSERT IGNORE INTO work_experiences (title, role, startdate, enddate, description)
VALUES ('New Company', 'Software Engineer', 'Jan 2026', 'Present', 'Description here.');
EOF
```

Migrations run automatically on startup. The `INSERT IGNORE` ensures they're idempotent — restarting the app won't duplicate data.

## Stopping

```bash
docker compose down
```

Add `-v` to also wipe the database volume:

```bash
docker compose down -v
```
