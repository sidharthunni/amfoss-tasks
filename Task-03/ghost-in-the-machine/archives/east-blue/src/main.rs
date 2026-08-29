use anyhow::Result;
use log::{info, warn};
use navnet_core::compat::{CompatibilityLayer, CompatibilityPolicy, ProtocolVersion};
use navnet_core::migration::upgrade_legacy_snapshot;
use navnet_core::registry::StationRegistry;

fn main() -> Result<()> {
    env_logger::init();

    let mut registry = StationRegistry::new();
    info!("East Blue registry bootstrap initialized");

    let legacy_path = "../../legacy-stations.yml";
    let stations = upgrade_legacy_snapshot(legacy_path)?;

    let compat = CompatibilityLayer::new(ProtocolVersion::V1);

    for station in stations {
        if let Err(e) = compat.enforce(&station) {
            warn!("station {} failed compatibility check: {}", station.station_id, e);
            continue;
        }
        registry.add_station(station)?;
    }

    info!("East Blue bootstrap completed with {} stations", registry.stations.len());
    Ok(())
}


