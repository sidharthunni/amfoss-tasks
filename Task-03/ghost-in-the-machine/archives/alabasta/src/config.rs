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
    pub deployment: DeploymentConfig,
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
    #[serde(default)]
    pub legacy_compat: bool,
}

#[derive(Debug, Deserialize)]
pub struct DeploymentConfig {
    #[serde(default)]
    pub plan: String,
    #[serde(default = "DeploymentConfig::default_log_level")]
    pub log_level: String,
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
            deployment: DeploymentConfig::default(),
            logging: LoggingConfig::default(),
        }
    }
}

impl Default for ServiceConfig {
    fn default() -> Self {
        ServiceConfig {
            host: Self::default_host(),
            port: Self::default_port(),
            max_clients: None,
            keep_alive: true,
        }
    }
}

impl ServiceConfig {
    fn default_host() -> String {
        "127.0.0.1".to_string()
    }

    fn default_port() -> u16 {
        9010
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
            legacy_compat: true,
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

impl Default for DeploymentConfig {
    fn default() -> Self {
        DeploymentConfig {
            plan: "deployment/plan.yml".to_string(),
            log_level: Self::default_log_level(),
        }
    }
}

impl DeploymentConfig {
    fn default_log_level() -> String {
        "info".to_string()
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
    pub fn load<P: AsRef<Path>>(path: P) -> Result<Self> {
        let path: &Path = path.as_ref();
        let raw = fs::read_to_string(path)
            .with_context(|| format!("failed to read configuration from {}", path.display()))?;
        let mut config: AppConfig = toml::from_str(&raw)
            .with_context(|| format!("failed to parse configuration from {}", path.display()))?;

        if let Ok(override_raw) = fs::read_to_string(path.with_file_name("override.toml")) {
            let overrides: AppConfig = toml::from_str(&override_raw)
                .with_context(|| format!("failed to parse override configuration from {}", path.with_file_name("override.toml").display()))?;
            config = config.apply_overrides(overrides);
        }

        Ok(config)
    }

    fn apply_overrides(mut self, overrides: AppConfig) -> AppConfig {
        if overrides.service.port != ServiceConfig::default_port() {
            self.service.port = overrides.service.port;
        }
        if overrides.runtime.cache_dir != RuntimeConfig::default_cache_dir() {
            self.runtime.cache_dir = overrides.runtime.cache_dir;
        }
        if overrides.logging.level != LoggingConfig::default_level() {
            self.logging.level = overrides.logging.level;
        }
        self
    }

    pub fn effective_max_clients(&self) -> u32 {
        self.service.max_clients.unwrap_or(256)
    }
}
