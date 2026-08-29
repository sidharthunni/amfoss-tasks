use alabasta::config::AppConfig;
use alabasta::coordinator::Coordinator;
use assert_fs::fixture::{FileWriteStr, PathChild, PathCreateDir, TempDir};
use std::path::Path;

#[test]
fn application_config_loads() {
    let temp = TempDir::new().unwrap();
    let config_dir = temp.child("config");
    config_dir.create_dir_all().unwrap();
    let config_path = config_dir.child("application.toml");
    std::fs::write(
        config_path.path(),
        r#"[service]
host = "0.0.0.0"
port = 9010

[runtime]
data_dir = "data"
cache_dir = "cache"
assets_dir = "assets"
legacy_compat = true

[logging]
level = "info"
"#,
    )
    .unwrap();

    let config = AppConfig::load(config_path.path()).unwrap();
    assert_eq!(config.service.port, 9010);
}

#[test]
fn override_configuration_applies_port() {
    let temp = TempDir::new().unwrap();
    let config_dir = temp.child("config");
    config_dir.create_dir_all().unwrap();
    let config_path = config_dir.child("application.toml");
    std::fs::write(
        config_path.path(),
        r#"[service]
host = "0.0.0.0"
port = 9010

[runtime]
data_dir = "data"
cache_dir = "cache"
assets_dir = "assets"
legacy_compat = true

[logging]
level = "info"
"#,
    )
    .unwrap();
    let override_path = config_dir.child("override.toml");
    override_path.write_str(
        r#"[service]
port = 9011

[runtime]
cache_dir = "runtime-cache"

[logging]
level = "debug"
"#,
    )
    .unwrap();

    let config = AppConfig::load(config_path.path()).unwrap();
    assert_eq!(config.service.port, 9011);
    assert_eq!(config.runtime.cache_dir, "runtime-cache");
}

#[test]
fn coordinator_creates_cache_dir() {
    let temp = TempDir::new().unwrap();
    let config_dir = temp.child("config");
    config_dir.create_dir_all().unwrap();
    let config_path = config_dir.child("application.toml");
    std::fs::write(
        config_path.path(),
        r#"[service]
host = "0.0.0.0"
port = 9010

[runtime]
data_dir = "data"
cache_dir = "cache"
assets_dir = "assets"
legacy_compat = true

[logging]
level = "info"
"#,
    )
    .unwrap();

    let config = AppConfig::load(config_path.path()).unwrap();
    let coordinator = Coordinator::new(config, config_path.path()).unwrap();
    coordinator.initialize().unwrap();
    assert!(config_dir.child("cache").exists());
}
