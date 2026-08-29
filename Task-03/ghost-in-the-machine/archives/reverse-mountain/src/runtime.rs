use crate::config::AppConfig;
use anyhow::{Context, Result};
use log::{debug, info, warn};
use std::{fs, path::{Path, PathBuf}};

#[derive(Debug)]
pub struct RuntimeApp {
    pub config: AppConfig,
    pub cache_dir: PathBuf,
    pub assets_dir: PathBuf,
}

impl RuntimeApp {
    pub fn from_config(config: AppConfig, config_path: &Path) -> Result<Self> {
        let working_dir = std::env::current_dir().context("failed to determine current working directory")?;
        let config_dir = config_path
            .parent()
            .unwrap_or_else(|| Path::new("."));

        let cache_dir = working_dir.join(&config.runtime.cache_dir);
        let assets_dir = config_dir.join(&config.runtime.assets_dir);

        debug!("cache_dir resolved from working directory: {}", cache_dir.display());
        debug!("assets_dir resolved from config directory: {}", assets_dir.display());

        Ok(RuntimeApp {
            config,
            cache_dir,
            assets_dir,
        })
    }

    pub fn initialize(&self) -> Result<()> {
        if !self.assets_dir.exists() {
            warn!("asset directory does not exist: {}", self.assets_dir.display());
        }

        if !self.cache_dir.exists() {
            warn!("cache directory missing; creating fallback at {}", self.cache_dir.display());
            fs::create_dir_all(&self.cache_dir)
                .with_context(|| format!("failed to create cache directory {}", self.cache_dir.display()))?;
        }

        info!("service starting on {}:{}", self.config.service.host, self.config.service.port);
        info!("effective max clients = {}", self.config.effective_max_clients());
        info!("data directory = {}", self.config.runtime.data_dir);

        Ok(())
    }
}
