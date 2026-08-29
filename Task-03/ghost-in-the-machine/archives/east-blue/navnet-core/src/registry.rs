use anyhow::{Context, Result};
use log::{debug, warn};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StationMetadata {
    pub station_id: String,
    pub hostname: String,
    pub protocol: String,
    pub last_checked: String,
    pub labels: HashMap<String, String>,
}

#[derive(Debug)]
pub struct StationRegistry {
    pub stations: HashMap<String, StationMetadata>,
}

impl StationRegistry {
    pub fn new() -> Self {
        StationRegistry {
            stations: HashMap::new(),
        }
    }

    pub fn load<P: AsRef<Path>>(source: P) -> Result<Self> {
        let path = source.as_ref();
        let raw = fs::read_to_string(path)
            .with_context(|| format!("failed to read registry snapshot from {}", path.display()))?;
        let stations: Vec<StationMetadata> = serde_json::from_str(&raw)
            .with_context(|| format!("failed to parse registry snapshot {}", path.display()))?;

        let mut registry = StationRegistry::new();
        for station in stations {
            if station.station_id.is_empty() {
                warn!("skipping registry entry with empty station_id: {}", station.hostname);
                continue;
            }
            debug!("loaded registry entry: {} {}", station.station_id, station.hostname);
            registry.stations.insert(station.station_id.clone(), station);
        }

        Ok(registry)
    }

    pub fn get(&self, station_id: &str) -> Option<&StationMetadata> {
        self.stations.get(station_id)
    }

    pub fn add_station(&mut self, metadata: StationMetadata) -> Result<()> {
        if metadata.station_id.trim().is_empty() {
            anyhow::bail!("station_id cannot be empty")
        }

        if self.stations.contains_key(&metadata.station_id) {
            warn!("station already existed in registry: {}", metadata.station_id);
        }

        self.stations.insert(metadata.station_id.clone(), metadata);
        Ok(())
    }
}
