use whiskey_peak::config::AppConfig;
use std::path::Path;

#[test]
fn effective_max_clients_defaults_to_100() {
    let config = AppConfig::load(Path::new("config/application.toml")).unwrap();
    assert_eq!(config.effective_max_clients(), 120);
}
