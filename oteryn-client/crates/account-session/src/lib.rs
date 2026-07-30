//! Non-secret account-session correlation identity for the W7 technical-login flow.
//!
//! [`AccountSessionId`] is allocated by the client to identify one authenticated
//! account context and reject stale completions. It is not an external account
//! identifier, bearer token or authorization credential.

use std::error::Error;
use std::fmt::{self, Display, Formatter};
use std::num::NonZeroU64;

/// Client-local opaque identity for one authenticated account context.
///
/// Values are non-zero, deterministic and safe to include in diagnostics. They
/// never identify an Oteryn account outside the client process and grant no
/// authority by themselves.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct AccountSessionId(NonZeroU64);

impl AccountSessionId {
    /// Construct a client-local account-session identity.
    ///
    /// # Errors
    ///
    /// Returns [`AccountSessionIdError::Zero`] when `value` is zero.
    pub fn new(value: u64) -> Result<Self, AccountSessionIdError> {
        NonZeroU64::new(value)
            .map(Self)
            .ok_or(AccountSessionIdError::Zero)
    }

    /// Return the non-zero client-local numeric value.
    #[must_use]
    pub const fn get(self) -> u64 {
        self.0.get()
    }
}

impl TryFrom<u64> for AccountSessionId {
    type Error = AccountSessionIdError;

    fn try_from(value: u64) -> Result<Self, Self::Error> {
        Self::new(value)
    }
}

impl From<AccountSessionId> for u64 {
    fn from(value: AccountSessionId) -> Self {
        value.get()
    }
}

impl Display for AccountSessionId {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        write!(formatter, "account-session:{}", self.get())
    }
}

/// Stable validation failure for [`AccountSessionId`].
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AccountSessionIdError {
    /// Zero cannot identify an active account-session generation.
    Zero,
}

impl Display for AccountSessionIdError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str("account session ID must be non-zero")
    }
}

impl Error for AccountSessionIdError {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn account_session_id_rejects_zero() {
        assert_eq!(AccountSessionId::new(0), Err(AccountSessionIdError::Zero));
    }

    #[test]
    fn account_session_id_round_trips_and_formats_safely() -> Result<(), AccountSessionIdError> {
        let id = AccountSessionId::new(17)?;

        assert_eq!(id.get(), 17);
        assert_eq!(u64::from(id), 17);
        assert_eq!(id.to_string(), "account-session:17");
        assert_eq!(format!("{id:?}"), "AccountSessionId(17)");
        Ok(())
    }
}
