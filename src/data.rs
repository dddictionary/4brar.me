use serde::Serialize;
use sqlx::mysql::MySqlPool;
use sqlx::FromRow;

#[derive(Debug, Clone, Serialize)]
pub struct NavItem {
    pub href: String,
    pub caption: String,
}

#[derive(Debug, Clone, Serialize, FromRow)]
pub struct HobbyItem {
    #[serde(skip_serializing)]
    #[allow(dead_code)]
    pub id: i32,
    pub title: String,
    pub description: String,
    pub source: String,
}

#[derive(Debug, Clone, Serialize, FromRow)]
pub struct WorkItem {
    #[serde(skip_serializing)]
    #[allow(dead_code)]
    pub id: i32,
    pub title: String,
    pub role: String,
    pub startdate: String,
    pub enddate: String,
    pub description: String,
}

#[derive(Debug, Clone, Serialize, FromRow)]
pub struct EducationItem {
    #[serde(skip_serializing)]
    #[allow(dead_code)]
    pub id: i32,
    pub title: String,
    pub startdate: String,
    pub enddate: String,
    pub description: String,
}

#[derive(Debug, Clone, Serialize, FromRow)]
pub struct Location {
    #[serde(skip_serializing)]
    #[allow(dead_code)]
    pub id: i32,
    pub name: String,
    pub lat: f64,
    pub lng: f64,
}

pub fn nav_items() -> Vec<NavItem> {
    vec![
        NavItem {
            href: "/aboutme".to_string(),
            caption: "About Me".to_string(),
        },
        NavItem {
            href: "/work".to_string(),
            caption: "Work Experiences".to_string(),
        },
        NavItem {
            href: "/hobbies".to_string(),
            caption: "Hobbies".to_string(),
        },
        NavItem {
            href: "/education".to_string(),
            caption: "Education".to_string(),
        },
        NavItem {
            href: "/travels".to_string(),
            caption: "Travels".to_string(),
        },
        NavItem {
            href: "/timeline".to_string(),
            caption: "Timeline".to_string(),
        },
    ]
}

pub async fn get_hobbies(pool: &MySqlPool) -> Result<Vec<HobbyItem>, sqlx::Error> {
    sqlx::query_as::<_, HobbyItem>("SELECT * FROM hobbies ORDER BY id")
        .fetch_all(pool)
        .await
}

pub async fn get_work_experiences(pool: &MySqlPool) -> Result<Vec<WorkItem>, sqlx::Error> {
    sqlx::query_as::<_, WorkItem>("SELECT * FROM work_experiences ORDER BY id")
        .fetch_all(pool)
        .await
}

pub async fn get_education(pool: &MySqlPool) -> Result<Vec<EducationItem>, sqlx::Error> {
    sqlx::query_as::<_, EducationItem>("SELECT * FROM education ORDER BY id")
        .fetch_all(pool)
        .await
}

pub async fn get_locations(pool: &MySqlPool) -> Result<Vec<Location>, sqlx::Error> {
    sqlx::query_as::<_, Location>("SELECT * FROM locations ORDER BY id")
        .fetch_all(pool)
        .await
}
