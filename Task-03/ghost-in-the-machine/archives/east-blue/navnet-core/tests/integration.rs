use navnet_core::compat::{CompatibilityLayer, CompatibilityPolicy, ProtocolVersion};
use navnet_core::registry::{StationMetadata, StationRegistry};

#[test]
fn registry_loads_and_retrieves_entries() {
    let mut registry = StationRegistry::new();
    let entry = StationMetadata {
        station_id: "station-23".to_string(),
        hostname: "navnet-23.internal".to_string(),
        protocol: "v2".to_string(),
        last_checked: "2026-06-01T09:00:00Z".to_string(),
        labels: vec![("deployment-zone".to_string(), "east".to_string())]
            .into_iter()
            .collect(),
    };

    registry.add_station(entry.clone()).unwrap();
    let loaded = registry.get("station-23").expect("station should exist");
    assert_eq!(loaded.hostname, "navnet-23.internal");
}

#[test]
fn compatibility_layer_rejects_legacy_for_v2_target() {
    let entry = StationMetadata {
        station_id: "station-31".to_string(),
        hostname: "navnet-31.internal".to_string(),
        protocol: "v1".to_string(),
        last_checked: "2026-06-01T09:00:00Z".to_string(),
        labels: vec![("deployment-zone".to_string(), "west".to_string())]
            .into_iter()
            .collect(),
    };

    let policy = CompatibilityLayer::new(ProtocolVersion::V2);
    assert!(policy.enforce(&entry).is_err());
}
