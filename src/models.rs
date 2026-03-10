use chrono::NaiveDateTime;
use serde::Serialize;
use sqlx::MySqlPool;

#[derive(Debug, Clone, Serialize, sqlx::FromRow)]
pub struct TimelinePost {
    pub id: i32,
    pub name: String,
    pub email: String,
    pub content: String,
    pub created_at: NaiveDateTime,
}

pub async fn get_all_posts(pool: &MySqlPool) -> Result<Vec<TimelinePost>, sqlx::Error> {
    sqlx::query_as::<_, TimelinePost>("SELECT id, name, email, content, created_at FROM timelinepost ORDER BY created_at DESC")
        .fetch_all(pool)
        .await
}

pub async fn create_post(
    pool: &MySqlPool,
    name: &str,
    email: &str,
    content: &str,
) -> Result<TimelinePost, sqlx::Error> {
    let result = sqlx::query("INSERT INTO timelinepost (name, email, content) VALUES (?, ?, ?)")
        .bind(name)
        .bind(email)
        .bind(content)
        .execute(pool)
        .await?;

    let id = result.last_insert_id();

    sqlx::query_as::<_, TimelinePost>(
        "SELECT id, name, email, content, created_at FROM timelinepost WHERE id = ?",
    )
    .bind(id)
    .fetch_one(pool)
    .await
}
