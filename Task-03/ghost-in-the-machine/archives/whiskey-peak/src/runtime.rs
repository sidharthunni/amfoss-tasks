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

        debug!("resolved cache_dir={}", cache_dir.display());
        debug!("resolved assets_dir={}", assets_dir.display());

        Ok(RuntimeApp {
            config,
            cache_dir,
            assets_dir,
        })
    }

    pub fn initialize(&self) -> Result<()> {
        if self.config.runtime.validate_assets {
            if !self.assets_dir.exists() {
                warn!("asset path missing: {}", self.assets_dir.display());
            }
        }

        if !self.cache_dir.exists() {
            warn!("cache directory missing; creating {}", self.cache_dir.display());
            fs::create_dir_all(&self.cache_dir)
                .with_context(|| format!("failed to create cache dir {}", self.cache_dir.display()))?;
        }

        info!("starting service on {}:{}", self.config.service.host, self.config.service.port);
        info!("max clients = {}", self.config.effective_max_clients());
        if self.config.runtime.legacy_mode {
            info!("legacy_mode enabled");
        }
        Ok(())
    }
}
