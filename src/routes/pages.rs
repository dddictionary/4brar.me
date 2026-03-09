use std::sync::Arc;

use axum::extract::State;
use axum::response::Html;

use crate::data;
use crate::state::AppState;

pub async fn index(State(state): State<Arc<AppState>>) -> Html<String> {
    let mut ctx = tera::Context::new();
    ctx.insert("navigation", &data::nav_items());
    ctx.insert("title", "Abrar Habib");
    ctx.insert("url", &state.url);
    ctx.insert("request_path", "/");

    let rendered = state.tera.render("index.html", &ctx).unwrap_or_else(|e| {
        tracing::error!("Template render error: {e}");
        "Internal Server Error".to_string()
    });
    Html(rendered)
}

pub async fn aboutme(State(state): State<Arc<AppState>>) -> Html<String> {
    let mut ctx = tera::Context::new();
    ctx.insert("navigation", &data::nav_items());
    ctx.insert("title", "Abrar Habib \u{2014} About Me");
    ctx.insert("url", &state.url);
    ctx.insert("request_path", "/aboutme");

    let rendered = state
        .tera
        .render("aboutme.html", &ctx)
        .unwrap_or_else(|e| {
            tracing::error!("Template render error: {e}");
            "Internal Server Error".to_string()
        });
    Html(rendered)
}

pub async fn work(State(state): State<Arc<AppState>>) -> Html<String> {
    let work = data::get_work_experiences(&state.db).await.unwrap_or_default();

    let mut ctx = tera::Context::new();
    ctx.insert("navigation", &data::nav_items());
    ctx.insert("title", "Abrar Habib \u{2014} Work Experiences");
    ctx.insert("url", &state.url);
    ctx.insert("request_path", "/work");
    ctx.insert("work", &work);

    let rendered = state.tera.render("work.html", &ctx).unwrap_or_else(|e| {
        tracing::error!("Template render error: {e}");
        "Internal Server Error".to_string()
    });
    Html(rendered)
}

pub async fn education(State(state): State<Arc<AppState>>) -> Html<String> {
    let education = data::get_education(&state.db).await.unwrap_or_default();

    let mut ctx = tera::Context::new();
    ctx.insert("navigation", &data::nav_items());
    ctx.insert("title", "Abrar Habib \u{2014} Education");
    ctx.insert("url", &state.url);
    ctx.insert("request_path", "/education");
    ctx.insert("education", &education);

    let rendered = state
        .tera
        .render("education.html", &ctx)
        .unwrap_or_else(|e| {
            tracing::error!("Template render error: {e}");
            "Internal Server Error".to_string()
        });
    Html(rendered)
}

pub async fn hobbies(State(state): State<Arc<AppState>>) -> Html<String> {
    let hobbies = data::get_hobbies(&state.db).await.unwrap_or_default();

    let mut ctx = tera::Context::new();
    ctx.insert("navigation", &data::nav_items());
    ctx.insert("title", "Abrar Habib \u{2014} Hobbies");
    ctx.insert("url", &state.url);
    ctx.insert("request_path", "/hobbies");
    ctx.insert("hobbies", &hobbies);

    let rendered = state
        .tera
        .render("hobbies.html", &ctx)
        .unwrap_or_else(|e| {
            tracing::error!("Template render error: {e}");
            "Internal Server Error".to_string()
        });
    Html(rendered)
}

pub async fn travels(State(state): State<Arc<AppState>>) -> Html<String> {
    let locations = data::get_locations(&state.db).await.unwrap_or_default();

    let mut ctx = tera::Context::new();
    ctx.insert("navigation", &data::nav_items());
    ctx.insert("title", "Abrar Habib \u{2014} Travels");
    ctx.insert("url", &state.url);
    ctx.insert("request_path", "/travels");
    ctx.insert("locations", &locations);

    let rendered = state
        .tera
        .render("travel.html", &ctx)
        .unwrap_or_else(|e| {
            tracing::error!("Template render error: {e}");
            "Internal Server Error".to_string()
        });
    Html(rendered)
}

pub async fn timeline(State(state): State<Arc<AppState>>) -> Html<String> {
    let mut ctx = tera::Context::new();
    ctx.insert("navigation", &data::nav_items());
    ctx.insert("title", "Timeline");
    ctx.insert("url", &state.url);
    ctx.insert("request_path", "/timeline");

    let rendered = state
        .tera
        .render("timeline.html", &ctx)
        .unwrap_or_else(|e| {
            tracing::error!("Template render error: {e}");
            "Internal Server Error".to_string()
        });
    Html(rendered)
}
