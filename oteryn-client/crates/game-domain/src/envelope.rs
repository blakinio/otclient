use crate::DomainError;

/// Closed version marker for gameplay command and event envelopes.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct EnvelopeVersion(u16);

impl EnvelopeVersion {
    /// Initial gameplay contract version.
    pub const V1: Self = Self(1);

    /// Validate a numeric envelope version.
    ///
    /// # Errors
    ///
    /// Returns [`DomainError::UnsupportedEnvelopeVersion`] for values not
    /// implemented by this crate revision.
    pub fn try_new(value: u16) -> Result<Self, DomainError> {
        if value == Self::V1.0 {
            Ok(Self::V1)
        } else {
            Err(DomainError::UnsupportedEnvelopeVersion(value))
        }
    }

    /// Return the stable numeric version.
    #[must_use]
    pub const fn get(self) -> u16 {
        self.0
    }
}
