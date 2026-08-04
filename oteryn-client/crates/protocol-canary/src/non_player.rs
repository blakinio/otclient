use crate::CANARY_NETWORK_MESSAGE_MAX_BYTES;
use crate::inbound::{CanaryInboundBootstrapState, CanaryInboundError};
use crate::outfit::decode_current_non_otcr_outfit;
use crate::tile::OPCODE_ADD_TILE_THING;
use oteryn_foundation::SessionGeneration;
use oteryn_game_domain::{
    EntityHandle, EntityId, EntityKind, Floor, GameEvent, GameEventEnvelope, NameText, StackIndex,
    TilePosition,
};
use oteryn_protocol_core::{BoundedReader, ProtocolError, ProtocolErrorKind, TrailingDataPolicy};

const UNKNOWN_CREATURE_MARKER: u16 = 0x61;
const CREATURE_TYPE_MONSTER: u8 = 1;
const CREATURE_TYPE_NPC: u8 = 2;
const CREATURE_TYPE_PLAYER_SUMMON: u8 = 3;
const MAX_ENTITY_NAME_BYTES: usize = 64;
const MAX_CREATURE_ICONS: u8 = 3;
const MAX_TILE_STACK_INDEX: u8 = 9;
const MAP_MAX_LAYERS: u8 = 16;
const CREATURE_MARK_UNMARKED: u8 = 0xFF;
const CREATURE_INSPECTION_NONE: u8 = 0;

/// Decode one complete Current unknown monster, player-owned monster
/// summon or NPC appearance.
///
/// The accepted producer branch is exactly opcode `0x6A`, one canonical
/// position, a visible stack index, unknown-creature marker `0x61`, zero cache
/// eviction, one non-local entity id, a header type of monster (`1`) or NPC
/// (`2`), one non-empty domain-bounded name and the complete common payload. A
/// normal monster or NPC repeats its header type in the final type field. A
/// source-reachable monster with a player master keeps monster type in the
/// header, is rewritten to player-summon type (`3`) in the final field and
/// appends one nonzero master id.
///
/// The adapter never creates, mutates or infers the producer's known-creature
/// cache and does not expose the Canary-only master relationship. It emits only
/// protocol-neutral [`GameEvent::EntityAppeared`] state. Hidden health, direct
/// summon header types, nonzero eviction, extension payloads and every trailing
/// byte remain rejected.
///
/// # Errors
///
/// Rejects stale, pre-bootstrap or terminal state; local or zero identity;
/// invalid floor, stack, name, health, direction, outfit, icon, type, master,
/// mark, inspection or walkthrough fields; truncation, oversize and trailing
/// data.
pub fn decode_current_unknown_remote_non_player_appearance(
    input: &[u8],
    state: &CanaryInboundBootstrapState,
    current: SessionGeneration,
) -> Result<GameEventEnvelope, CanaryInboundError> {
    state.session().ensure_current(current)?;
    if !state.bootstrap_completed() || state.session_ended() {
        return Err(CanaryInboundError::InvalidOrder);
    }
    let local_player = state
        .local_player()
        .ok_or(CanaryInboundError::InvalidOrder)?;

    let mut reader = BoundedReader::new(input, CANARY_NETWORK_MESSAGE_MAX_BYTES)?;
    expect_u8(&mut reader, OPCODE_ADD_TILE_THING)?;
    let position = read_position(&mut reader)?;
    let stack = read_stack(&mut reader)?;

    if reader.read_u16_le()? != UNKNOWN_CREATURE_MARKER || reader.read_u32_le()? != 0 {
        return Err(unknown_value().into());
    }
    let entity_id = reader.read_u32_le()?;
    if entity_id == local_player.id().get() {
        return Err(unknown_value().into());
    }

    let header_type = reader.read_u8()?;
    let kind = entity_kind(header_type)?;
    let name = reader.read_u16_string(MAX_ENTITY_NAME_BYTES)?;
    if name.is_empty() {
        return Err(unknown_value().into());
    }

    parse_non_player_payload(&mut reader, header_type)?;
    reader.finish(TrailingDataPolicy::Reject)?;

    let entity = EntityHandle::new(state.session(), EntityId::try_new(entity_id)?);
    let envelope = GameEventEnvelope::v1(
        state.session(),
        GameEvent::EntityAppeared {
            entity,
            kind,
            name: Some(NameText::try_new(name)?),
            position,
            stack,
        },
    )?;
    envelope.ensure_current(current)?;
    Ok(envelope)
}

fn parse_non_player_payload(
    reader: &mut BoundedReader<'_>,
    header_type: u8,
) -> Result<(), CanaryInboundError> {
    if !(1..=100).contains(&reader.read_u8()?) || reader.read_u8()? > 7 {
        return Err(unknown_value().into());
    }
    decode_current_non_otcr_outfit(reader)?;

    let _light_level = reader.read_u8()?;
    let _light_color = reader.read_u8()?;
    let _step_speed = reader.read_u16_le()?;
    let icon_count = reader.read_u8()?;
    if icon_count > MAX_CREATURE_ICONS {
        return Err(unknown_value().into());
    }
    for _ in 0..icon_count {
        let _serialized_icon = reader.read_u8()?;
        let _icon_category = reader.read_u8()?;
        let _icon_count = reader.read_u16_le()?;
    }

    let _skull = reader.read_u8()?;
    let _party_shield = reader.read_u8()?;
    let _guild_emblem = reader.read_u8()?;
    parse_final_type(reader, header_type)?;
    let _speech_bubble = reader.read_u8()?;
    expect_u8(reader, CREATURE_MARK_UNMARKED)?;
    expect_u8(reader, CREATURE_INSPECTION_NONE)?;
    if !matches!(reader.read_u8()?, 0 | 1) {
        return Err(unknown_value().into());
    }
    Ok(())
}

fn parse_final_type(
    reader: &mut BoundedReader<'_>,
    header_type: u8,
) -> Result<(), CanaryInboundError> {
    let final_type = reader.read_u8()?;
    match (header_type, final_type) {
        (CREATURE_TYPE_MONSTER, CREATURE_TYPE_MONSTER) | (CREATURE_TYPE_NPC, CREATURE_TYPE_NPC) => {
            Ok(())
        }
        (CREATURE_TYPE_MONSTER, CREATURE_TYPE_PLAYER_SUMMON) => {
            if reader.read_u32_le()? == 0 {
                return Err(unknown_value().into());
            }
            Ok(())
        }
        _ => Err(unknown_value().into()),
    }
}

fn entity_kind(creature_type: u8) -> Result<EntityKind, CanaryInboundError> {
    match creature_type {
        CREATURE_TYPE_MONSTER => Ok(EntityKind::Creature),
        CREATURE_TYPE_NPC => Ok(EntityKind::NonPlayerCharacter),
        _ => Err(unknown_value().into()),
    }
}

fn read_position(reader: &mut BoundedReader<'_>) -> Result<TilePosition, CanaryInboundError> {
    let x = reader.read_u16_le()?;
    let y = reader.read_u16_le()?;
    let z = reader.read_u8()?;
    if z >= MAP_MAX_LAYERS {
        return Err(unknown_value().into());
    }
    Ok(TilePosition::new(x, y, Floor::new(z)))
}

fn read_stack(reader: &mut BoundedReader<'_>) -> Result<StackIndex, CanaryInboundError> {
    let stack = reader.read_u8()?;
    if stack > MAX_TILE_STACK_INDEX {
        return Err(unknown_value().into());
    }
    Ok(StackIndex::new(stack))
}

fn expect_u8(reader: &mut BoundedReader<'_>, expected: u8) -> Result<(), ProtocolError> {
    if reader.read_u8()? == expected {
        Ok(())
    } else {
        Err(unknown_value())
    }
}

const fn unknown_value() -> ProtocolError {
    ProtocolError::new(ProtocolErrorKind::UnknownValue)
}

#[cfg(test)]
mod tests;
