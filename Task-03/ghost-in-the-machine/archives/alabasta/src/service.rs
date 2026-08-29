use crate::config::AppConfig;
use anyhow::Result;
use log::info;

pub struct Service {
    config: AppConfig,
}

impl Service {
    pub fn new(config: AppConfig) -> Self {
        Service { config }
    }

    pub fn start(&self) -> Result<()> {
        info!("service starting with host {} and port {}", self.config.service.host, self.config.service.port);
        info!("service max clients = {}", self.config.effective_max_clients());
        Ok(())
    }
}
