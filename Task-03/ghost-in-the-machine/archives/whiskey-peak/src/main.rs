use anyhow::Result;
use log::info;
use std::path::Path;
use whiskey_peak::config::AppConfig;
use whiskey_peak::runtime::RuntimeApp;

fn main() -> Result<()> {
    env_logger::init();

    let config_path = Path::new("config/application.toml");
    let config = AppConfig::load(config_path)?;
    let runtime = RuntimeApp::from_config(config, config_path)?;
    runtime.initialize()?;

    info!("whiskey peak service booted");
    Ok(())
}
