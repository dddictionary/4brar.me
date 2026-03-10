use std::sync::Arc;

use axum::extract::{Form, State};
use axum::http::StatusCode;
use axum::response::{IntoResponse, Json};
use serde::Deserialize;
use serde_json::json;

use crate::models;
use crate::state::AppState;

pub async fn get_timeline_posts(
    State(state): State<Arc<AppState>>,
) -> Result<impl IntoResponse, (StatusCode, String)> {
    let posts = models::get_all_posts(&state.db)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?;

    Ok(Json(json!({ "timeline_posts": posts })))
}

#[derive(Debug, Deserialize)]
pub struct PostForm {
    pub name: Option<String>,
    pub email: Option<String>,
    pub content: Option<String>,
}

pub async fn post_timeline_post(
    State(state): State<Arc<AppState>>,
    Form(form): Form<PostForm>,
) -> Result<impl IntoResponse, (StatusCode, String)> {
    let name = form.name.unwrap_or_default();
    if name.trim().is_empty() {
        return Err((StatusCode::BAD_REQUEST, "Invalid name".to_string()));
    }

    let email = form.email.unwrap_or_default();
    if email.trim().is_empty() || !email.contains('@') {
        return Err((StatusCode::BAD_REQUEST, "Invalid email".to_string()));
    }

    let content = form.content.unwrap_or_default();
    if content.trim().is_empty() {
        return Err((StatusCode::BAD_REQUEST, "Invalid content".to_string()));
    }

    let post = models::create_post(&state.db, &name, &email, &content)
        .await
        .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()))?;

    metrics::counter!("timeline_posts_created_total").increment(1);

    Ok(Json(serde_json::to_value(post).unwrap()))
}

pub async fn test_ci() -> Json<serde_json::Value> {
    Json(json!("ci should be working and this endpoint should be reachable"))
}

pub async fn healthz(
    State(state): State<Arc<AppState>>,
) -> Result<impl IntoResponse, (StatusCode, String)> {
    sqlx::query("SELECT 1")
        .execute(&state.db)
        .await
        .map_err(|e| (StatusCode::SERVICE_UNAVAILABLE, e.to_string()))?;

    Ok(Json(json!({ "status": "ok" })))
}

pub async fn metrics_handler(
    State(state): State<Arc<AppState>>,
) -> String {
    state.prometheus_handle.render()
}
