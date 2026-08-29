use anyhow::{Context, Result};
use serde::Deserialize;
use std::{fs, path::Path};

#[derive(Debug, Deserialize)]
pub struct AppConfig {
    #[serde(default)]
    pub service: ServiceConfig,
    #[serde(default)]
    pub runtime: RuntimeConfig,
    #[serde(default)]
    pub logging: LoggingConfig,
}

#[derive(Debug, Deserialize)]
pub struct ServiceConfig {
    #[serde(default = "ServiceConfig::default_host")]
    pub host: String,
    #[serde(default = "ServiceConfig::default_port")]
    pub port: u16,
    #[serde(default)]
    pub timeout_seconds: Option<u64>,
    pub max_clients: Option<u32>,
    #[serde(default = "ServiceConfig::default_keep_alive")]
    pub keep_alive: bool,
}

#[derive(Debug, Deserialize)]
pub struct RuntimeConfig {
    #[serde(default = "RuntimeConfig::default_data_dir")]
    pub data_dir: String,
    #[serde(default = "RuntimeConfig::default_cache_dir")]
    pub cache_dir: String,
    #[serde(default = "RuntimeConfig::default_assets_dir")]
    pub assets_dir: String,
}

#[derive(Debug, Deserialize)]
pub struct LoggingConfig {
    #[serde(default = "LoggingConfig::default_level")]
    pub level: String,
}

impl Default for AppConfig {
    fn default() -> Self {
        AppConfig {
            service: ServiceConfig::default(),
            runtime: RuntimeConfig::default(),
            logging: LoggingConfig::default(),
        }
    }
}

impl Default for ServiceConfig {
    fn default() -> Self {
        ServiceConfig {
            host: Self::default_host(),
            port: Self::default_port(),
            timeout_seconds: Some(60),
            max_clients: Some(64),
            keep_alive: true,
        }
    }
}

impl ServiceConfig {
    fn default_host() -> String {
        "127.0.0.1".to_string()
    }

    fn default_port() -> u16 {
        9090
    }

    fn default_keep_alive() -> bool {
        true
    }
}

impl Default for RuntimeConfig {
    fn default() -> Self {
        RuntimeConfig {
            data_dir: Self::default_data_dir(),
            cache_dir: Self::default_cache_dir(),
            assets_dir: Self::default_assets_dir(),
        }
    }
}

impl RuntimeConfig {
    fn default_data_dir() -> String {
        "./data".to_string()
    }

    fn default_cache_dir() -> String {
        "./cache".to_string()
    }

    fn default_assets_dir() -> String {
        "./assets".to_string()
    }
}

impl Default for LoggingConfig {
    fn default() -> Self {
        LoggingConfig {
            level: Self::default_level(),
        }
    }
}

impl LoggingConfig {
    fn default_level() -> String {
        "info".to_string()
    }
}

impl AppConfig {
    pub fn load<P: AsRef<Path>>(source: P) -> Result<Self> {
        let path: &Path = source.as_ref();
        let raw = fs::read_to_string(path)
            .with_context(|| format!("failed to read application config from {}", path.display()))?;
        let config: AppConfig = toml::from_str(&raw)
            .with_context(|| format!("failed to parse application config from {}", path.display()))?;
        Ok(config)
    }

    pub fn effective_max_clients(&self) -> u32 {
        self.service.max_clients.unwrap_or(64)
    }
}
