use crate::DomainError;
use oteryn_foundation::SessionGeneration;

/// Capability token fencing gameplay values to one replaceable session lifetime.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct SessionToken(SessionGeneration);

impl SessionToken {
    /// Construct a gameplay session token from the shared technical generation.
    #[must_use]
    pub const fn new(generation: SessionGeneration) -> Self {
        Self(generation)
    }

    /// Return the technical generation carried by this token.
    #[must_use]
    pub const fn generation(self) -> SessionGeneration {
        self.0
    }

    /// Verify that this token belongs to the caller's current session.
    ///
    /// # Errors
    ///
    /// Returns [`DomainError::StaleSession`] when generations differ.
    pub fn ensure_current(self, current: SessionGeneration) -> Result<(), DomainError> {
        if self.0 == current {
            Ok(())
        } else {
            Err(DomainError::StaleSession {
                expected: current,
                actual: self.0,
            })
        }
    }
}
