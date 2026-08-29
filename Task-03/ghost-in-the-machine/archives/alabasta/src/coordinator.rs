use crate::config::AppConfig;
use anyhow::{Context, Result};
use log::{debug, info};
use std::{fs, path::{Path, PathBuf}};

#[derive(Debug)]
pub struct Coordinator {
    config: AppConfig,
    data_dir: PathBuf,
    cache_dir: PathBuf,
    assets_dir: PathBuf,
}

impl Coordinator {
    pub fn new(config: AppConfig, config_path: &Path) -> Result<Self> {
        let root_dir = config_path.parent().unwrap_or_else(|| Path::new("."));
        let data_dir = root_dir.join(&config.runtime.data_dir);
        let cache_dir = root_dir.join(&config.runtime.cache_dir);
        let assets_dir = root_dir.join(&config.runtime.assets_dir);

        debug!("resolved data_dir={}", data_dir.display());
        debug!("resolved cache_dir={}", cache_dir.display());
        debug!("resolved assets_dir={}", assets_dir.display());

        Ok(Coordinator {
            config,
            data_dir,
            cache_dir,
            assets_dir,
        })
    }

    pub fn initialize(&self) -> Result<()> {
        if !self.assets_dir.exists() {
            info!("assets directory not found, using fallback behavior");
        }

        if !self.cache_dir.exists() {
            info!("cache directory not found, creating {}", self.cache_dir.display());
            fs::create_dir_all(&self.cache_dir)
                .with_context(|| format!("failed to create cache directory {}", self.cache_dir.display()))?;
        }

        if self.config.runtime.legacy_compat {
            info!("legacy compatibility enabled for runtime integration");
        }

        info!("coordinator initialization complete");
        Ok(())
    }

    pub fn into_config(self) -> AppConfig {
        self.config
    }
}
