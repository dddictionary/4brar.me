mod data;
mod models;
mod routes;
mod state;

use std::sync::Arc;
use std::time::Instant;

use axum::extract::MatchedPath;
use axum::http::Request;
use axum::middleware::{self, Next};
use axum::response::IntoResponse;
use axum::routing::get;
use axum::Router;
use metrics_exporter_prometheus::PrometheusBuilder;
use sqlx::mysql::MySqlPoolOptions;
use tera::Tera;
use tower_http::services::ServeDir;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

use crate::state::AppState;

async fn track_metrics(req: Request<axum::body::Body>, next: Next) -> impl IntoResponse {
    let start = Instant::now();
    let method = req.method().clone().to_string();
    let path = req
        .extensions()
        .get::<MatchedPath>()
        .map(|mp| mp.as_str().to_string())
        .unwrap_or_else(|| req.uri().path().to_string());

    let response = next.run(req).await;

    let duration = start.elapsed().as_secs_f64();
    let status = response.status().as_u16().to_string();

    let labels = [
        ("method", method),
        ("path", path),
        ("status", status),
    ];

    metrics::histogram!("http_request_duration_seconds", &labels).record(duration);
    metrics::counter!("http_requests_total", &labels).increment(1);

    response
}

#[tokio::main]
async fn main() {
    dotenvy::dotenv().ok();

    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::try_from_default_env().unwrap_or_else(|_| {
            "backend=debug,tower_http=debug".into()
        }))
        .with(tracing_subscriber::fmt::layer())
        .init();

    let tera = Tera::new("app/templates/**/*").expect("Failed to initialize Tera templates");

    let mysql_user = std::env::var("MYSQL_USER").expect("MYSQL_USER must be set");
    let mysql_password = std::env::var("MYSQL_PASSWORD").expect("MYSQL_PASSWORD must be set");
    let mysql_host = std::env::var("MYSQL_HOST").expect("MYSQL_HOST must be set");
    let mysql_database = std::env::var("MYSQL_DATABASE").expect("MYSQL_DATABASE must be set");

    let database_url = format!(
        "mysql://{}:{}@{}/{}",
        mysql_user, mysql_password, mysql_host, mysql_database
    );

    let pool = MySqlPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await
        .expect("Failed to create MySQL connection pool");

    sqlx::migrate!("./migrations")
        .run(&pool)
        .await
        .expect("Failed to run database migrations");

    tracing::info!("Database migrations completed successfully");

    let prometheus_handle = PrometheusBuilder::new()
        .install_recorder()
        .expect("Failed to install Prometheus recorder");

    let url = std::env::var("URL").unwrap_or_else(|_| "http://localhost:5000".to_string());

    let state = Arc::new(AppState {
        tera,
        db: pool,
        prometheus_handle,
        url,
    });

    let app = Router::new()
        .route("/", get(routes::pages::index))
        .route("/aboutme", get(routes::pages::aboutme))
        .route("/work", get(routes::pages::work))
        .route("/education", get(routes::pages::education))
        .route("/hobbies", get(routes::pages::hobbies))
        .route("/travels", get(routes::pages::travels))
        .route("/timeline", get(routes::pages::timeline))
        .route(
            "/api/timeline_post",
            get(routes::api::get_timeline_posts).post(routes::api::post_timeline_post),
        )
        .route("/api/test-ci", get(routes::api::test_ci))
        .route("/healthz", get(routes::api::healthz))
        .route("/metrics", get(routes::api::metrics_handler))
        .nest_service("/static", ServeDir::new("app/static"))
        .layer(middleware::from_fn(track_metrics))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:5000")
        .await
        .expect("Failed to bind to port 5000");

    tracing::info!("Server listening on 0.0.0.0:5000");

    axum::serve(listener, app)
        .await
        .expect("Server failed");
}
