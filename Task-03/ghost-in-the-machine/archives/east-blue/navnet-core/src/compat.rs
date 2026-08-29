use crate::registry::StationMetadata;
use thiserror::Error;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProtocolVersion {
    Legacy,
    V1,
    V2,
}

impl ProtocolVersion {
    pub fn from_str(value: &str) -> Self {
        match value {
            "v2" | "2" => ProtocolVersion::V2,
            "v1" | "1" => ProtocolVersion::V1,
            _ => ProtocolVersion::Legacy,
        }
    }
}

#[derive(Debug, Error)]
pub enum CompatibilityError {
    #[error("station {station_id} requires unsupported protocol {protocol}")]
    UnsupportedProtocol { station_id: String, protocol: String },

    #[error("station {station_id} is missing required compatibility label")] 
    MissingLabel { station_id: String },
}

pub trait CompatibilityPolicy {
    fn is_compatible(&self, metadata: &StationMetadata) -> bool;
    fn enforce(&self, metadata: &StationMetadata) -> Result<(), CompatibilityError>;
}

pub struct CompatibilityLayer {
    target: ProtocolVersion,
}

impl CompatibilityLayer {
    pub fn new(target: ProtocolVersion) -> Self {
        CompatibilityLayer { target }
    }
}

impl CompatibilityPolicy for CompatibilityLayer {
    fn is_compatible(&self, metadata: &StationMetadata) -> bool {
        let version = ProtocolVersion::from_str(&metadata.protocol);
        match self.target {
            ProtocolVersion::V2 => version == ProtocolVersion::V2,
            ProtocolVersion::V1 => version == ProtocolVersion::V1 || version == ProtocolVersion::Legacy,
            ProtocolVersion::Legacy => true,
        }
    }

    fn enforce(&self, metadata: &StationMetadata) -> Result<(), CompatibilityError> {
        let version = ProtocolVersion::from_str(&metadata.protocol);
        if self.target == ProtocolVersion::V2 && version != ProtocolVersion::V2 {
            return Err(CompatibilityError::UnsupportedProtocol {
                station_id: metadata.station_id.clone(),
                protocol: metadata.protocol.clone(),
            });
        }

        if metadata.labels.get("deployment-zone").is_none() {
            return Err(CompatibilityError::MissingLabel {
                station_id: metadata.station_id.clone(),
            });
        }

        Ok(())
    }
}
