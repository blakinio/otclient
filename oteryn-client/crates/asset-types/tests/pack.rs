use oteryn_asset_types::{
    AssetError, AssetId, AssetKind, AssetMetadata, AssetPack, AssetRecord, MAX_RECORDS,
    PACK_SCHEMA_VERSION,
};
use std::error::Error;
use std::io;

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
fn invalid_rgba8_payload_is_rejected() -> Result<(), Box<dyn Error>> {
    let metadata = AssetMetadata::new(
        AssetId::new(9)?,
        AssetKind::Rgba8 {
            width: 2,
            height: 2,
        },
        "rgba".to_owned(),
        "CC0-1.0".to_owned(),
        "original synthetic test fixture".to_owned(),
    )?;
    assert_eq!(
        AssetRecord::new(metadata, vec![0; 15]),
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
