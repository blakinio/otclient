use std::fmt::{self, Display, Formatter};

/// Identifies which technical generation reached its maximum value.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GenerationKind {
    /// Generation of a client process lifetime.
    Process,
    /// Generation of a replaceable session lifetime.
    Session,
    /// Generation of a replaceable task or operation lifetime.
    Task,
}

impl Display for GenerationKind {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        let name = match self {
            Self::Process => "process",
            Self::Session => "session",
            Self::Task => "task",
        };
        formatter.write_str(name)
    }
}

/// Failure produced by checked technical-generation operations.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GenerationError {
    /// The generation is already at `u64::MAX` and cannot advance.
    Exhausted(GenerationKind),
}

impl Display for GenerationError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::Exhausted(kind) => write!(formatter, "{kind} generation is exhausted"),
        }
    }
}

impl std::error::Error for GenerationError {}

macro_rules! generation_type {
    ($name:ident, $kind:expr, $description:literal) => {
        #[doc = $description]
        #[derive(Debug, Default, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
        pub struct $name(u64);

        impl $name {
            /// The initial generation.
            pub const ZERO: Self = Self(0);

            /// The largest representable generation.
            pub const MAX: Self = Self(u64::MAX);

            /// Construct a generation from an explicit technical value.
            #[must_use]
            pub const fn new(value: u64) -> Self {
                Self(value)
            }

            /// Return the stored technical value.
            #[must_use]
            pub const fn get(self) -> u64 {
                self.0
            }

            /// Advance by one without allowing wraparound.
            ///
            /// # Errors
            ///
            /// Returns [`GenerationError::Exhausted`] at [`Self::MAX`].
            pub fn checked_next(self) -> Result<Self, GenerationError> {
                self.0
                    .checked_add(1)
                    .map(Self)
                    .ok_or(GenerationError::Exhausted($kind))
            }
        }

        impl Display for $name {
            fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
                Display::fmt(&self.0, formatter)
            }
        }
    };
}

generation_type!(
    ProcessGeneration,
    GenerationKind::Process,
    "Generation fencing results that belong to one client-process lifetime."
);
generation_type!(
    SessionGeneration,
    GenerationKind::Session,
    "Generation fencing results that belong to one replaceable session lifetime."
);
generation_type!(
    TaskGeneration,
    GenerationKind::Task,
    "Generation fencing results that belong to one replaceable task or operation."
);

#[cfg(test)]
mod tests {
    use super::*;
    use std::any::TypeId;

    #[test]
    fn generation_newtypes_are_distinct_public_types() {
        assert_ne!(
            TypeId::of::<ProcessGeneration>(),
            TypeId::of::<SessionGeneration>()
        );
        assert_ne!(
            TypeId::of::<ProcessGeneration>(),
            TypeId::of::<TaskGeneration>()
        );
        assert_ne!(
            TypeId::of::<SessionGeneration>(),
            TypeId::of::<TaskGeneration>()
        );
    }

    #[test]
    fn generations_are_ordered_and_advance_without_wraparound() -> Result<(), GenerationError> {
        let current = SessionGeneration::new(41);
        let next = current.checked_next()?;

        assert!(next > current);
        assert_eq!(next.get(), 42);
        assert_eq!(SessionGeneration::ZERO.get(), 0);
        Ok(())
    }

    #[test]
    fn each_generation_reports_its_own_exhaustion() {
        assert_eq!(
            ProcessGeneration::MAX.checked_next(),
            Err(GenerationError::Exhausted(GenerationKind::Process))
        );
        assert_eq!(
            SessionGeneration::MAX.checked_next(),
            Err(GenerationError::Exhausted(GenerationKind::Session))
        );
        assert_eq!(
            TaskGeneration::MAX.checked_next(),
            Err(GenerationError::Exhausted(GenerationKind::Task))
        );
    }

    #[test]
    fn generation_errors_are_deterministic_and_non_secret() {
        let error = GenerationError::Exhausted(GenerationKind::Task);

        assert_eq!(error.to_string(), "task generation is exhausted");
        assert_eq!(format!("{error:?}"), "Exhausted(Task)");
    }
}
