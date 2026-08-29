use reverse_mountain::config::AppConfig;
use reverse_mountain::runtime::RuntimeApp;
use std::path::Path;

#[test]
fn load_default_config() {
    let config = AppConfig::load(Path::new("config/application.toml")).unwrap();
    assert_eq!(config.service.port, 8080);
}

#[test]
fn runtime_initializes_with_missing_asset_dir() {
    let config = AppConfig::load(Path::new("config/application.toml")).unwrap();
    let runtime = RuntimeApp::from_config(config, Path::new("config/application.toml")).unwrap();
    assert!(runtime.initialize().is_ok());
}

#[test]
fn asset_directory_is_expected_in_config_tree() {
    let config = AppConfig::load(Path::new("config/application.toml")).unwrap();
    let runtime = RuntimeApp::from_config(config, Path::new("config/application.toml")).unwrap();
    assert!(runtime.assets_dir.exists(), "expected configured asset directory to exist");
}
