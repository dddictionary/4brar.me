use metrics_exporter_prometheus::PrometheusHandle;
use sqlx::MySqlPool;
use tera::Tera;

pub struct AppState {
    pub tera: Tera,
    pub db: MySqlPool,
    pub prometheus_handle: PrometheusHandle,
    pub url: String,
}
