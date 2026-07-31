//! Bounded binary protocol helpers shared by protocol adapters.
//!
//! This crate owns no Canary constants, opcodes, transport policy or domain
//! identifiers. Every read, write and allocation is checked against an explicit
//! caller-provided limit.

use std::error::Error;
use std::fmt::{self, Display, Formatter};
use std::str;

/// Largest buffer accepted by the first bounded protocol-core contract.
pub const MAX_PROTOCOL_BUFFER_BYTES: usize = u16::MAX as usize;

/// Closed protocol parsing and encoding failure categories.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProtocolErrorKind {
    /// The input ended before the requested field was complete.
    Truncated,
    /// An input, output or field exceeded its configured bound.
    Oversized,
    /// A length or configured limit was invalid.
    InvalidLength,
    /// A string field was not valid UTF-8.
    InvalidUtf8,
    /// Bytes remained after a parser that requires complete consumption.
    TrailingData,
    /// A closed field contained an unsupported value.
    UnknownValue,
    /// Checked offset or length arithmetic overflowed.
    ArithmeticOverflow,
}

/// Stable non-secret protocol error.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ProtocolError {
    kind: ProtocolErrorKind,
}

impl ProtocolError {
    /// Construct one stable protocol error category.
    #[must_use]
    pub const fn new(kind: ProtocolErrorKind) -> Self {
        Self { kind }
    }

    /// Return the closed failure category.
    #[must_use]
    pub const fn kind(self) -> ProtocolErrorKind {
        self.kind
    }
}

impl Display for ProtocolError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        let message = match self.kind {
            ProtocolErrorKind::Truncated => "protocol input is truncated",
            ProtocolErrorKind::Oversized => "protocol value exceeds its size limit",
            ProtocolErrorKind::InvalidLength => "protocol length is invalid",
            ProtocolErrorKind::InvalidUtf8 => "protocol string is not valid UTF-8",
            ProtocolErrorKind::TrailingData => "protocol input contains trailing data",
            ProtocolErrorKind::UnknownValue => "protocol value is unsupported",
            ProtocolErrorKind::ArithmeticOverflow => "protocol length arithmetic overflowed",
        };
        formatter.write_str(message)
    }
}

impl Error for ProtocolError {}

/// Policy applied when a bounded reader reaches a logical message boundary.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TrailingDataPolicy {
    /// Reject every unread byte.
    Reject,
    /// Permit unread bytes for a caller-owned outer parser.
    Allow,
}

/// Checked cursor over one already-bounded byte slice.
#[derive(Debug, Clone)]
pub struct BoundedReader<'a> {
    input: &'a [u8],
    position: usize,
}

impl<'a> BoundedReader<'a> {
    /// Construct a reader after validating the complete input size.
    ///
    /// # Errors
    ///
    /// Returns a stable error for a zero/unsupported limit or oversized input.
    pub fn new(input: &'a [u8], max_bytes: usize) -> Result<Self, ProtocolError> {
        validate_limit(max_bytes)?;
        if input.len() > max_bytes {
            return Err(ProtocolError::new(ProtocolErrorKind::Oversized));
        }
        Ok(Self { input, position: 0 })
    }

    /// Return the number of unread bytes.
    #[must_use]
    pub const fn remaining(&self) -> usize {
        self.input.len() - self.position
    }

    /// Return whether no unread bytes remain.
    #[must_use]
    pub const fn is_empty(&self) -> bool {
        self.remaining() == 0
    }

    /// Read one byte.
    ///
    /// # Errors
    ///
    /// Returns [`ProtocolErrorKind::Truncated`] at end of input.
    pub fn read_u8(&mut self) -> Result<u8, ProtocolError> {
        Ok(self.read_exact(1)?[0])
    }

    /// Read one little-endian unsigned 16-bit integer.
    ///
    /// # Errors
    ///
    /// Returns a truncation or arithmetic error for malformed input.
    pub fn read_u16_le(&mut self) -> Result<u16, ProtocolError> {
        let bytes = self.read_exact(2)?;
        Ok(u16::from_le_bytes([bytes[0], bytes[1]]))
    }

    /// Read one little-endian unsigned 32-bit integer.
    ///
    /// # Errors
    ///
    /// Returns a truncation or arithmetic error for malformed input.
    pub fn read_u32_le(&mut self) -> Result<u32, ProtocolError> {
        let bytes = self.read_exact(4)?;
        Ok(u32::from_le_bytes([bytes[0], bytes[1], bytes[2], bytes[3]]))
    }

    /// Read one little-endian unsigned 64-bit integer.
    ///
    /// # Errors
    ///
    /// Returns a truncation or arithmetic error for malformed input.
    pub fn read_u64_le(&mut self) -> Result<u64, ProtocolError> {
        let bytes = self.read_exact(8)?;
        Ok(u64::from_le_bytes([
            bytes[0], bytes[1], bytes[2], bytes[3], bytes[4], bytes[5], bytes[6], bytes[7],
        ]))
    }

    /// Read an exact borrowed byte field.
    ///
    /// # Errors
    ///
    /// Returns a checked arithmetic or truncation error.
    pub fn read_exact(&mut self, length: usize) -> Result<&'a [u8], ProtocolError> {
        let end = self
            .position
            .checked_add(length)
            .ok_or_else(|| ProtocolError::new(ProtocolErrorKind::ArithmeticOverflow))?;
        if end > self.input.len() {
            return Err(ProtocolError::new(ProtocolErrorKind::Truncated));
        }
        let field = &self.input[self.position..end];
        self.position = end;
        Ok(field)
    }

    /// Read a little-endian `u16` length-prefixed UTF-8 string.
    ///
    /// # Errors
    ///
    /// Rejects oversized, truncated and invalid UTF-8 fields.
    pub fn read_u16_string(&mut self, max_bytes: usize) -> Result<String, ProtocolError> {
        validate_limit(max_bytes)?;
        let length = usize::from(self.read_u16_le()?);
        if length > max_bytes {
            return Err(ProtocolError::new(ProtocolErrorKind::Oversized));
        }
        let bytes = self.read_exact(length)?;
        let value = str::from_utf8(bytes)
            .map_err(|_| ProtocolError::new(ProtocolErrorKind::InvalidUtf8))?;
        Ok(value.to_owned())
    }

    /// Apply the selected trailing-data policy.
    ///
    /// # Errors
    ///
    /// Rejects unread bytes when the policy is [`TrailingDataPolicy::Reject`].
    pub fn finish(self, policy: TrailingDataPolicy) -> Result<(), ProtocolError> {
        if policy == TrailingDataPolicy::Reject && !self.is_empty() {
            return Err(ProtocolError::new(ProtocolErrorKind::TrailingData));
        }
        Ok(())
    }
}

/// Checked bounded binary writer.
#[derive(Debug, Clone)]
pub struct BoundedWriter {
    output: Vec<u8>,
    max_bytes: usize,
}

impl BoundedWriter {
    /// Construct an empty writer with one explicit maximum size.
    ///
    /// # Errors
    ///
    /// Returns an invalid-length error for zero or unsupported limits.
    pub fn new(max_bytes: usize) -> Result<Self, ProtocolError> {
        validate_limit(max_bytes)?;
        Ok(Self {
            output: Vec::new(),
            max_bytes,
        })
    }

    /// Return the current encoded length.
    #[must_use]
    pub fn len(&self) -> usize {
        self.output.len()
    }

    /// Return whether no bytes have been encoded.
    #[must_use]
    pub fn is_empty(&self) -> bool {
        self.output.is_empty()
    }

    /// Append one byte.
    ///
    /// # Errors
    ///
    /// Rejects output that would exceed the configured limit.
    pub fn write_u8(&mut self, value: u8) -> Result<(), ProtocolError> {
        self.write_bytes(&[value])
    }

    /// Append one little-endian unsigned 16-bit integer.
    ///
    /// # Errors
    ///
    /// Rejects output that would exceed the configured limit.
    pub fn write_u16_le(&mut self, value: u16) -> Result<(), ProtocolError> {
        self.write_bytes(&value.to_le_bytes())
    }

    /// Append one little-endian unsigned 32-bit integer.
    ///
    /// # Errors
    ///
    /// Rejects output that would exceed the configured limit.
    pub fn write_u32_le(&mut self, value: u32) -> Result<(), ProtocolError> {
        self.write_bytes(&value.to_le_bytes())
    }

    /// Append one little-endian unsigned 64-bit integer.
    ///
    /// # Errors
    ///
    /// Rejects output that would exceed the configured limit.
    pub fn write_u64_le(&mut self, value: u64) -> Result<(), ProtocolError> {
        self.write_bytes(&value.to_le_bytes())
    }

    /// Append one exact byte field.
    ///
    /// # Errors
    ///
    /// Rejects checked arithmetic overflow, allocation failure or oversized output.
    pub fn write_bytes(&mut self, bytes: &[u8]) -> Result<(), ProtocolError> {
        let next_length = self
            .output
            .len()
            .checked_add(bytes.len())
            .ok_or_else(|| ProtocolError::new(ProtocolErrorKind::ArithmeticOverflow))?;
        if next_length > self.max_bytes {
            return Err(ProtocolError::new(ProtocolErrorKind::Oversized));
        }
        self.output
            .try_reserve(bytes.len())
            .map_err(|_| ProtocolError::new(ProtocolErrorKind::Oversized))?;
        self.output.extend_from_slice(bytes);
        Ok(())
    }

    /// Append a little-endian `u16` length-prefixed UTF-8 string.
    ///
    /// # Errors
    ///
    /// Rejects a string outside the field or output bounds.
    pub fn write_u16_string(&mut self, value: &str, max_bytes: usize) -> Result<(), ProtocolError> {
        validate_limit(max_bytes)?;
        if value.len() > max_bytes {
            return Err(ProtocolError::new(ProtocolErrorKind::Oversized));
        }
        let length = u16::try_from(value.len())
            .map_err(|_| ProtocolError::new(ProtocolErrorKind::InvalidLength))?;
        self.write_u16_le(length)?;
        self.write_bytes(value.as_bytes())
    }

    /// Consume the writer and return its bounded output.
    #[must_use]
    pub fn into_inner(self) -> Vec<u8> {
        self.output
    }
}

fn validate_limit(max_bytes: usize) -> Result<(), ProtocolError> {
    if max_bytes == 0 || max_bytes > MAX_PROTOCOL_BUFFER_BYTES {
        return Err(ProtocolError::new(ProtocolErrorKind::InvalidLength));
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn bounded_reader_writer_round_trip_is_deterministic() -> Result<(), ProtocolError> {
        let mut writer = BoundedWriter::new(128)?;
        writer.write_u8(7)?;
        writer.write_u16_le(0x1234)?;
        writer.write_u32_le(0xA1B2_C3D4)?;
        writer.write_u64_le(0x0102_0304_0506_0708)?;
        writer.write_u16_string("synthetic", 32)?;
        let bytes = writer.into_inner();

        let mut reader = BoundedReader::new(&bytes, 128)?;
        assert_eq!(reader.read_u8()?, 7);
        assert_eq!(reader.read_u16_le()?, 0x1234);
        assert_eq!(reader.read_u32_le()?, 0xA1B2_C3D4);
        assert_eq!(reader.read_u64_le()?, 0x0102_0304_0506_0708);
        assert_eq!(reader.read_u16_string(32)?, "synthetic");
        reader.finish(TrailingDataPolicy::Reject)
    }

    #[test]
    fn malformed_lengths_and_strings_fail_closed() -> Result<(), ProtocolError> {
        let oversized = [5_u8, 0, b'a', b'b', b'c', b'd', b'e'];
        let mut oversized_reader = BoundedReader::new(&oversized, 32)?;
        assert_eq!(
            oversized_reader.read_u16_string(4),
            Err(ProtocolError::new(ProtocolErrorKind::Oversized))
        );

        let truncated = [4_u8, 0, b'a'];
        let mut truncated_reader = BoundedReader::new(&truncated, 32)?;
        assert_eq!(
            truncated_reader.read_u16_string(8),
            Err(ProtocolError::new(ProtocolErrorKind::Truncated))
        );

        let invalid_utf8 = [2_u8, 0, 0xC3, 0x28];
        let mut invalid_reader = BoundedReader::new(&invalid_utf8, 32)?;
        assert_eq!(
            invalid_reader.read_u16_string(8),
            Err(ProtocolError::new(ProtocolErrorKind::InvalidUtf8))
        );
        Ok(())
    }

    #[test]
    fn complete_consumption_policy_rejects_trailing_data() -> Result<(), ProtocolError> {
        let bytes = [1_u8, 2];
        let mut strict = BoundedReader::new(&bytes, 8)?;
        assert_eq!(strict.read_u8()?, 1);
        assert_eq!(
            strict.finish(TrailingDataPolicy::Reject),
            Err(ProtocolError::new(ProtocolErrorKind::TrailingData))
        );

        let mut permissive = BoundedReader::new(&bytes, 8)?;
        assert_eq!(permissive.read_u8()?, 1);
        permissive.finish(TrailingDataPolicy::Allow)
    }

    #[test]
    fn output_limits_are_checked_before_growth() -> Result<(), ProtocolError> {
        let mut writer = BoundedWriter::new(4)?;
        writer.write_u32_le(7)?;
        assert_eq!(
            writer.write_u8(1),
            Err(ProtocolError::new(ProtocolErrorKind::Oversized))
        );
        assert_eq!(writer.len(), 4);
        Ok(())
    }

    #[test]
    fn arbitrary_bounded_malformed_input_never_panics_and_is_repeatable() {
        for length in 0..=256 {
            let input = vec![0xFF; length];
            let first = classify_synthetic_record(&input);
            let second = classify_synthetic_record(&input);
            assert_eq!(first, second);
        }
    }

    fn classify_synthetic_record(input: &[u8]) -> Result<(), ProtocolError> {
        let mut reader = BoundedReader::new(input, 256)?;
        let tag = reader.read_u8()?;
        if tag > 3 {
            return Err(ProtocolError::new(ProtocolErrorKind::UnknownValue));
        }
        let _value = reader.read_u32_le()?;
        let _label = reader.read_u16_string(32)?;
        reader.finish(TrailingDataPolicy::Reject)
    }
}
