use oteryn_asset_types::{
    AssetError, AssetId, AssetKind, AssetMetadata, AssetPack, AssetRecord, MAX_ASSET_BYTES,
    MAX_LOGICAL_NAME_BYTES, MAX_RECORDS, PACK_SCHEMA_VERSION,
};
use std::error::Error;
use std::io;

const HEADER_BYTES: usize = 8 + 2 + 4;
const FIRST_KIND_OFFSET: usize = HEADER_BYTES + 4;

fn record(id: u32, kind: AssetKind, payload: &[u8]) -> Result<AssetRecord, AssetError> {
    AssetRecord::new(
        AssetMetadata::new(
            AssetId::new(id)?,
            kind,
            format!("asset-{id}"),
            "CC0-1.0".to_owned(),
            "original synthetic test fixture".to_owned(),
        )?,
        payload.to_vec(),
    )
}

#[test]
fn identifiers_and_metadata_are_bounded() -> Result<(), Box<dyn Error>> {
    assert_eq!(AssetId::new(0), Err(AssetError::InvalidId));
    let id = AssetId::new(1)?;

    assert_eq!(
        AssetMetadata::new(
            id,
            AssetKind::Blob,
            String::new(),
            "CC0-1.0".to_owned(),
            "original".to_owned(),
        ),
        Err(AssetError::EmptyText)
    );
    assert_eq!(
        AssetMetadata::new(
            id,
            AssetKind::Blob,
            "x".repeat(MAX_LOGICAL_NAME_BYTES + 1),
            "CC0-1.0".to_owned(),
            "original".to_owned(),
        ),
        Err(AssetError::TextTooLong)
    );
    assert_eq!(
        AssetMetadata::new(
            id,
            AssetKind::Blob,
            "line\nbreak".to_owned(),
            "CC0-1.0".to_owned(),
            "original".to_owned(),
        ),
        Err(AssetError::ControlCharacter)
    );
    Ok(())
}

#[test]
fn sha256_matches_known_vector() -> Result<(), Box<dyn Error>> {
    let record = record(1, AssetKind::Blob, b"abc")?;
    let expected = [
        0xba, 0x78, 0x16, 0xbf, 0x8f, 0x01, 0xcf, 0xea, 0x41, 0x41, 0x40, 0xde, 0x5d, 0xae, 0x22,
        0x23, 0xb0, 0x03, 0x61, 0xa3, 0x96, 0x17, 0x7a, 0x9c, 0xb4, 0x10, 0xff, 0x61, 0xf2, 0x00,
        0x15, 0xad,
    ];
    assert_eq!(*record.digest(), expected);
    Ok(())
}

#[test]
fn output_is_canonical_and_manifest_order_independent() -> Result<(), Box<dyn Error>> {
    let first = record(1, AssetKind::Blob, b"first")?;
    let second = record(
        2,
        AssetKind::Rgba8 {
            width: 2,
            height: 2,
        },
        b"RGBA0123456789AB",
    )?;
    let ascending = AssetPack::new(vec![first.clone(), second.clone()])?.encode()?;
    let shuffled = AssetPack::new(vec![second, first])?.encode()?;
    assert_eq!(ascending, shuffled);
    Ok(())
}

#[test]
fn encoded_pack_round_trips_exactly() -> Result<(), Box<dyn Error>> {
    let pack = AssetPack::new(vec![
        record(1, AssetKind::Blob, b"synthetic blob")?,
        record(
            2,
            AssetKind::Rgba8 {
                width: 2,
                height: 2,
            },
            b"RGBA0123456789AB",
        )?,
    ])?;
    let encoded = pack.encode()?;
    let decoded = AssetPack::decode(&encoded)?;
    assert_eq!(decoded, pack);
    assert_eq!(decoded.encode()?, encoded);
    Ok(())
}

#[test]
fn duplicate_ids_are_rejected() -> Result<(), Box<dyn Error>> {
    let first = record(7, AssetKind::Blob, b"first")?;
    let second = record(7, AssetKind::Blob, b"second")?;
    assert_eq!(
        AssetPack::new(vec![first, second]),
        Err(AssetError::DuplicateId)
    );
    Ok(())
}

#[test]
fn invalid_rgba8_shape_is_rejected() -> Result<(), Box<dyn Error>> {
    let zero_dimension = AssetMetadata::new(
        AssetId::new(8)?,
        AssetKind::Rgba8 {
            width: 0,
            height: 2,
        },
        "rgba-zero".to_owned(),
        "CC0-1.0".to_owned(),
        "original synthetic test fixture".to_owned(),
    )?;
    assert_eq!(
        AssetRecord::new(zero_dimension, Vec::new()),
        Err(AssetError::InvalidDimensions)
    );

    let wrong_length = AssetMetadata::new(
        AssetId::new(9)?,
        AssetKind::Rgba8 {
            width: 2,
            height: 2,
        },
        "rgba-length".to_owned(),
        "CC0-1.0".to_owned(),
        "original synthetic test fixture".to_owned(),
    )?;
    assert_eq!(
        AssetRecord::new(wrong_length, vec![0; 15]),
        Err(AssetError::PayloadLengthMismatch)
    );
    Ok(())
}

#[test]
fn malformed_and_trailing_input_is_rejected() -> Result<(), Box<dyn Error>> {
    let encoded = AssetPack::new(vec![record(1, AssetKind::Blob, b"abc")?])?.encode()?;
    assert_eq!(
        AssetPack::decode(&encoded[..encoded.len() - 1]),
        Err(AssetError::MalformedPack)
    );

    let mut trailing = encoded;
    trailing.push(0);
    assert_eq!(AssetPack::decode(&trailing), Err(AssetError::TrailingBytes));
    Ok(())
}

#[test]
fn unsupported_version_and_unknown_kind_are_rejected() -> Result<(), Box<dyn Error>> {
    let encoded = AssetPack::new(vec![record(1, AssetKind::Blob, b"abc")?])?.encode()?;

    let mut unsupported = encoded.clone();
    unsupported[8..10].copy_from_slice(&(PACK_SCHEMA_VERSION + 1).to_le_bytes());
    assert_eq!(
        AssetPack::decode(&unsupported),
        Err(AssetError::UnsupportedVersion)
    );

    let mut unknown = encoded;
    unknown[FIRST_KIND_OFFSET] = u8::MAX;
    assert_eq!(AssetPack::decode(&unknown), Err(AssetError::UnknownKind));
    Ok(())
}

#[test]
fn non_canonical_record_order_is_rejected() -> Result<(), Box<dyn Error>> {
    let first = AssetPack::new(vec![record(1, AssetKind::Blob, b"first")?])?.encode()?;
    let second = AssetPack::new(vec![record(2, AssetKind::Blob, b"second")?])?.encode()?;

    let mut reversed = first[..HEADER_BYTES].to_vec();
    reversed[10..14].copy_from_slice(&2_u32.to_le_bytes());
    reversed.extend_from_slice(&second[HEADER_BYTES..]);
    reversed.extend_from_slice(&first[HEADER_BYTES..]);
    assert_eq!(
        AssetPack::decode(&reversed),
        Err(AssetError::NonCanonicalOrder)
    );
    Ok(())
}

#[test]
fn digest_mismatch_is_rejected() -> Result<(), Box<dyn Error>> {
    let mut encoded = AssetPack::new(vec![record(1, AssetKind::Blob, b"abc")?])?.encode()?;
    let Some(final_byte) = encoded.last_mut() else {
        return Err(io::Error::other("encoded test pack must contain a payload").into());
    };
    *final_byte ^= 0xff;
    assert_eq!(AssetPack::decode(&encoded), Err(AssetError::DigestMismatch));
    Ok(())
}

#[test]
fn oversized_record_count_is_rejected_before_allocation() {
    let mut encoded = Vec::new();
    encoded.extend_from_slice(b"OTASSET1");
    encoded.extend_from_slice(&PACK_SCHEMA_VERSION.to_le_bytes());
    let count = u32::try_from(MAX_RECORDS + 1).unwrap_or(u32::MAX);
    encoded.extend_from_slice(&count.to_le_bytes());
    assert_eq!(AssetPack::decode(&encoded), Err(AssetError::TooManyRecords));
}

#[test]
fn oversized_payload_length_is_rejected_before_payload_read() -> Result<(), Box<dyn Error>> {
    let mut encoded = AssetPack::new(vec![record(1, AssetKind::Blob, &[])])?.encode()?;
    let oversized = u32::try_from(MAX_ASSET_BYTES + 1)?;
    let payload_length_offset = encoded
        .len()
        .checked_sub(4)
        .ok_or_else(|| io::Error::other("encoded test pack must contain a payload length"))?;
    encoded[payload_length_offset..].copy_from_slice(&oversized.to_le_bytes());
    assert_eq!(AssetPack::decode(&encoded), Err(AssetError::PayloadTooLarge));
    Ok(())
}
