use crate::DomainError;
use std::fmt::{self, Debug, Formatter};

/// UTF-8 text whose byte length is bounded at construction time.
///
/// `Debug` output is intentionally redacted. Consumers that legitimately need
/// the accepted text must opt in through [`Self::as_str`].
#[derive(Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct BoundedText<const MAX_BYTES: usize> {
    value: String,
}

impl<const MAX_BYTES: usize> BoundedText<MAX_BYTES> {
    /// Validate and own externally supplied UTF-8 text.
    ///
    /// # Errors
    ///
    /// Returns [`DomainError::ZeroTextLimit`] when `MAX_BYTES` is zero and
    /// [`DomainError::TextTooLong`] when the value exceeds the byte limit.
    pub fn try_new(value: impl Into<String>) -> Result<Self, DomainError> {
        if MAX_BYTES == 0 {
            return Err(DomainError::ZeroTextLimit);
        }

        let value = value.into();
        let actual = value.len();
        if actual > MAX_BYTES {
            Err(DomainError::TextTooLong {
                max: MAX_BYTES,
                actual,
            })
        } else {
            Ok(Self { value })
        }
    }

    /// Borrow the validated text.
    #[must_use]
    pub fn as_str(&self) -> &str {
        &self.value
    }

    /// Return the accepted UTF-8 byte length.
    #[must_use]
    pub fn len(&self) -> usize {
        self.value.len()
    }

    /// Report whether the accepted text is empty.
    #[must_use]
    pub fn is_empty(&self) -> bool {
        self.value.is_empty()
    }
}

impl<const MAX_BYTES: usize> Debug for BoundedText<MAX_BYTES> {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("BoundedText")
            .field("bytes", &self.value.len())
            .field("redacted", &true)
            .finish()
    }
}

/// Bounded display name used by bootstrap, entity and container events.
pub type NameText = BoundedText<64>;
