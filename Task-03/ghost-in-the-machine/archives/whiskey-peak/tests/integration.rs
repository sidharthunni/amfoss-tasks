use assert_fs::fixture::{PathChild, PathCreateDir, TempDir};
use whiskey_peak::config::AppConfig;
use whiskey_peak::runtime::RuntimeApp;
use std::fs;
use std::path::Path;

#[test]
fn application_config_loads() {
    let config = AppConfig::load(Path::new("config/application.toml")).unwrap();
    assert_eq!(config.service.port, 9002);
}

#[test]
fn runtime_initializes_with_cache_creation() {
    let temp = TempDir::new().unwrap();
    let config_dir = temp.child("config");
    config_dir.create_dir_all().unwrap();
    let config_path = config_dir.child("application.toml");
    fs::write(
        config_path.path(),
        r#"[service]
host = "127.0.0.1"
port = 9003
max_clients = 20
keep_alive = true

[runtime]
data_dir = "data"
cache_dir = "cache"
assets_dir = "assets"
legacy_mode = false

[logging]
level = "info"
"#,
    )
    .unwrap();

    let original_dir = std::env::current_dir().unwrap();
    std::env::set_current_dir(temp.path()).unwrap();
    let config = AppConfig::load(Path::new("config/application.toml")).unwrap();
    let runtime = RuntimeApp::from_config(config, Path::new("config/application.toml")).unwrap();
    runtime.initialize().unwrap();
    assert!(temp.child("cache").exists());
    std::env::set_current_dir(original_dir).unwrap();
}

#[test]
fn legacy_mode_is_preserved_for_backward_compatibility() {
    let config = AppConfig::load(Path::new("config/application.toml")).unwrap();
    assert!(config.runtime.legacy_mode);
}
