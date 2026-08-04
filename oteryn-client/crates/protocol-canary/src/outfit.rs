use oteryn_protocol_core::{BoundedReader, ProtocolError, ProtocolErrorKind};

/// Decode one exact Current non-OTCR outfit payload.
///
/// Visible outfits preserve the producer's `lookType`, five color/addon
/// bytes and optional mounted color payload. Invisible or ghost creatures
/// use the exact default `Outfit_t` layout: zero `lookType`, zero
/// `lookTypeEx` and zero mount. Nonzero extended-look or default-branch
/// mount values fail closed.
pub(crate) fn decode_current_non_otcr_outfit(
    reader: &mut BoundedReader<'_>,
) -> Result<(), ProtocolError> {
    let look_type = reader.read_u16_le()?;
    if look_type == 0 {
        if reader.read_u16_le()? != 0 || reader.read_u16_le()? != 0 {
            return Err(unknown_value());
        }
        return Ok(());
    }

    let _colors_and_addons = reader.read_exact(5)?;
    if reader.read_u16_le()? != 0 {
        let _mount_colors = reader.read_exact(4)?;
    }
    Ok(())
}

const fn unknown_value() -> ProtocolError {
    ProtocolError::new(ProtocolErrorKind::UnknownValue)
}

#[cfg(test)]
mod tests {
    use super::*;
    use oteryn_protocol_core::TrailingDataPolicy;

    fn decode(input: &[u8]) -> Result<(), ProtocolError> {
        let mut reader = BoundedReader::new(input, 64)?;
        decode_current_non_otcr_outfit(&mut reader)?;
        reader.finish(TrailingDataPolicy::Reject)
    }

    #[test]
    fn accepts_visible_without_mount() {
        assert_eq!(decode(&[0x80, 0, 1, 2, 3, 4, 0, 0, 0]), Ok(()));
    }

    #[test]
    fn accepts_visible_with_mount_colors() {
        assert_eq!(
            decode(&[0x80, 0, 1, 2, 3, 4, 0, 7, 0, 8, 9, 10, 11]),
            Ok(())
        );
    }

    #[test]
    fn accepts_exact_default_invisible_outfit() {
        assert_eq!(decode(&[0, 0, 0, 0, 0, 0]), Ok(()));
    }

    #[test]
    fn rejects_nonzero_default_extended_look_or_mount() {
        assert_eq!(decode(&[0, 0, 1, 0, 0, 0]), Err(unknown_value()));
        assert_eq!(decode(&[0, 0, 0, 0, 1, 0]), Err(unknown_value()));
    }

    #[test]
    fn rejects_every_truncated_prefix() {
        for accepted in [
            &[0x80, 0, 1, 2, 3, 4, 0, 0, 0][..],
            &[0x80, 0, 1, 2, 3, 4, 0, 7, 0, 8, 9, 10, 11][..],
            &[0, 0, 0, 0, 0, 0][..],
        ] {
            for length in 0..accepted.len() {
                assert_eq!(
                    decode(&accepted[..length]),
                    Err(ProtocolError::new(ProtocolErrorKind::Truncated))
                );
            }
        }
    }
}
