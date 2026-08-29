use anyhow::Result;
use log::info;
use reverse_mountain::config::AppConfig;
use reverse_mountain::runtime::RuntimeApp;
use std::path::Path;

fn main() -> Result<()> {
    env_logger::init();

    let config_path = Path::new("config/application.toml");
    let config = AppConfig::load(config_path)?;
    let runtime = RuntimeApp::from_config(config, config_path)?;
    runtime.initialize()?;

    info!("reverse mountain runtime boot completed");
    Ok(())
}
