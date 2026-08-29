use anyhow::Result;
use alabasta::config::AppConfig;
use alabasta::coordinator::Coordinator;
use alabasta::service::Service;
use env_logger::{Builder, Env};
use log::info;
use std::path::Path;

fn main() -> Result<()> {
    Builder::from_env(Env::default().filter_or("ALABASTA_LOG", "info")).init();

    let config_path = Path::new("config/application.toml");
    let config = AppConfig::load(config_path)?;

    let coordinator = Coordinator::new(config, config_path)?;
    coordinator.initialize()?;

    let service = Service::new(coordinator.into_config());
    service.start()?;

    info!("alabasta service startup complete");
    Ok(())
}
