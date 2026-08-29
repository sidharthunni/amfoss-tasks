use crate::registry::StationMetadata;
use anyhow::{Context, Result};
use log::info;
use serde::Deserialize;
use std::collections::HashMap;
use std::fs;
use std::path::Path;

#[derive(Debug, Deserialize)]
struct LegacyStationRecord {
    #[serde(rename = "id")]
    pub station_id: String,
    pub host: String,
    pub proto: String,
    pub labels: Option<HashMap<String, String>>,
}

pub fn upgrade_legacy_snapshot<P: AsRef<Path>>(source: P) -> Result<Vec<StationMetadata>> {
    let path = source.as_ref();
    let raw = fs::read_to_string(path)
        .with_context(|| format!("failed to read legacy snapshot {}", path.display()))?;

    let legacy: Vec<LegacyStationRecord> = serde_yaml::from_str(&raw)
        .with_context(|| format!("failed to deserialize legacy snapshot {}", path.display()))?;

    info!("upgrading legacy station snapshot: {} records from {}", legacy.len(), path.display());

    let stations = legacy
        .into_iter()
        .map(|record| StationMetadata {
            station_id: record.station_id,
            hostname: record.host,
            protocol: record.proto,
            last_checked: "1970-01-01T00:00:00Z".to_string(),
            labels: record.labels.unwrap_or_default(),
        })
        .collect();

    Ok(stations)
}
