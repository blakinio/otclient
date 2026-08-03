use oteryn_foundation::SessionGeneration;
use oteryn_game_domain::{Direction, DomainError, GameCommand, GameCommandEnvelope};
use std::fmt::{Display, Formatter};

/// Canary Current opcode for a clean gameplay-session logout request.
pub const OPCODE_LOGOUT: u8 = 0x14;
/// Canary Current opcode for one northward movement step.
pub const OPCODE_STEP_NORTH: u8 = 0x65;
/// Canary Current opcode for one eastward movement step.
pub const OPCODE_STEP_EAST: u8 = 0x66;
/// Canary Current opcode for one southward movement step.
pub const OPCODE_STEP_SOUTH: u8 = 0x67;
/// Canary Current opcode for one westward movement step.
pub const OPCODE_STEP_WEST: u8 = 0x68;
/// Canary Current opcode for stopping the active movement sequence.
pub const OPCODE_STOP_MOVEMENT: u8 = 0x69;
/// Canary Current opcode for one north-east movement step.
pub const OPCODE_STEP_NORTH_EAST: u8 = 0x6A;
/// Canary Current opcode for one south-east movement step.
pub const OPCODE_STEP_SOUTH_EAST: u8 = 0x6B;
/// Canary Current opcode for one south-west movement step.
pub const OPCODE_STEP_SOUTH_WEST: u8 = 0x6C;
/// Canary Current opcode for one north-west movement step.
pub const OPCODE_STEP_NORTH_WEST: u8 = 0x6D;

/// One bounded source-evidenced Canary Current client command.
///
/// The current M2 subset contains only single-byte commands whose producer
/// dispatch has no payload. A caller must not transmit these bytes until a
/// separately proven real-admission lifecycle authorizes the connection.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct EncodedCanaryCommand {
    bytes: [u8; 1],
}

impl EncodedCanaryCommand {
    const fn new(opcode: u8) -> Self {
        Self { bytes: [opcode] }
    }

    /// Return the encoded command opcode.
    #[must_use]
    pub const fn opcode(self) -> u8 {
        self.bytes[0]
    }

    /// Borrow the exact encoded bytes.
    #[must_use]
    pub const fn as_bytes(&self) -> &[u8] {
        &self.bytes
    }
}

/// Stable failure returned by the bounded Current development encoder.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CanaryCommandError {
    /// The semantic envelope is stale or otherwise violates the domain contract.
    Domain(DomainError),
    /// The merged semantic command has no exactly evidenced M2 encoding yet.
    UnsupportedCommand(GameCommand),
}

impl Display for CanaryCommandError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Domain(error) => write!(formatter, "invalid gameplay command envelope: {error}"),
            Self::UnsupportedCommand(_) => {
                formatter.write_str("gameplay command has no supported Canary Current encoding")
            }
        }
    }
}

impl std::error::Error for CanaryCommandError {}

impl From<DomainError> for CanaryCommandError {
    fn from(error: DomainError) -> Self {
        Self::Domain(error)
    }
}

/// Encode the exactly evidenced single-byte M2 command subset.
///
/// Supported commands are one semantic step in any of the eight directions,
/// movement stop and clean logout. Other merged semantic commands fail
/// explicitly instead of guessing a wire layout.
///
/// # Errors
///
/// Returns [`CanaryCommandError::Domain`] when the envelope is stale or invalid,
/// and [`CanaryCommandError::UnsupportedCommand`] when its wire layout has not
/// been accepted from exact source/fixture evidence.
pub fn encode_current_development_command(
    envelope: GameCommandEnvelope,
    current: SessionGeneration,
) -> Result<EncodedCanaryCommand, CanaryCommandError> {
    envelope.ensure_current(current)?;
    let opcode = match envelope.command() {
        GameCommand::Step { direction } => direction_opcode(direction),
        GameCommand::StopMovement => OPCODE_STOP_MOVEMENT,
        GameCommand::Logout => OPCODE_LOGOUT,
        unsupported => return Err(CanaryCommandError::UnsupportedCommand(unsupported)),
    };
    Ok(EncodedCanaryCommand::new(opcode))
}

const fn direction_opcode(direction: Direction) -> u8 {
    match direction {
        Direction::North => OPCODE_STEP_NORTH,
        Direction::NorthEast => OPCODE_STEP_NORTH_EAST,
        Direction::East => OPCODE_STEP_EAST,
        Direction::SouthEast => OPCODE_STEP_SOUTH_EAST,
        Direction::South => OPCODE_STEP_SOUTH,
        Direction::SouthWest => OPCODE_STEP_SOUTH_WEST,
        Direction::West => OPCODE_STEP_WEST,
        Direction::NorthWest => OPCODE_STEP_NORTH_WEST,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use oteryn_game_domain::{GameCommandEnvelope, SessionToken};
    use std::error::Error;

    fn envelope(
        generation: u64,
        command: GameCommand,
    ) -> Result<GameCommandEnvelope, Box<dyn Error>> {
        Ok(GameCommandEnvelope::v1(
            SessionToken::new(SessionGeneration::try_new(generation)?),
            command,
        )?)
    }

    #[test]
    fn all_eight_step_directions_match_source_dispatch() -> Result<(), Box<dyn Error>> {
        for (direction, opcode) in [
            (Direction::North, OPCODE_STEP_NORTH),
            (Direction::NorthEast, OPCODE_STEP_NORTH_EAST),
            (Direction::East, OPCODE_STEP_EAST),
            (Direction::SouthEast, OPCODE_STEP_SOUTH_EAST),
            (Direction::South, OPCODE_STEP_SOUTH),
            (Direction::SouthWest, OPCODE_STEP_SOUTH_WEST),
            (Direction::West, OPCODE_STEP_WEST),
            (Direction::NorthWest, OPCODE_STEP_NORTH_WEST),
        ] {
            let encoded = encode_current_development_command(
                envelope(7, GameCommand::Step { direction })?,
                SessionGeneration::try_new(7)?,
            )?;
            assert_eq!(encoded.opcode(), opcode);
            assert_eq!(encoded.as_bytes(), &[opcode]);
        }
        Ok(())
    }

    #[test]
    fn stop_and_logout_are_single_byte_commands() -> Result<(), Box<dyn Error>> {
        for (command, opcode) in [
            (GameCommand::StopMovement, OPCODE_STOP_MOVEMENT),
            (GameCommand::Logout, OPCODE_LOGOUT),
        ] {
            assert_eq!(
                encode_current_development_command(
                    envelope(8, command)?,
                    SessionGeneration::try_new(8)?,
                )?
                .as_bytes(),
                &[opcode]
            );
        }
        Ok(())
    }

    #[test]
    fn unsupported_semantic_command_fails_explicitly() -> Result<(), Box<dyn Error>> {
        let command = GameCommand::ClearAttackTarget;
        assert_eq!(
            encode_current_development_command(
                envelope(9, command)?,
                SessionGeneration::try_new(9)?,
            ),
            Err(CanaryCommandError::UnsupportedCommand(command))
        );
        Ok(())
    }

    #[test]
    fn stale_session_fails_before_encoding() -> Result<(), Box<dyn Error>> {
        assert!(matches!(
            encode_current_development_command(
                envelope(10, GameCommand::Logout)?,
                SessionGeneration::try_new(11)?,
            ),
            Err(CanaryCommandError::Domain(_))
        ));
        Ok(())
    }

    #[test]
    fn generated_index_contains_exact_command_dispatch_entries() {
        const CURRENT_INDEX: &str =
            include_str!("../../../tools/canary-protocol-index/generated/current-index.json");
        for (opcode, method) in [
            (OPCODE_LOGOUT, "inline:logout"),
            (OPCODE_STEP_NORTH, "inline:playerMove"),
            (OPCODE_STEP_EAST, "inline:playerMove"),
            (OPCODE_STEP_SOUTH, "inline:playerMove"),
            (OPCODE_STEP_WEST, "inline:playerMove"),
            (OPCODE_STOP_MOVEMENT, "inline:playerStopAutoWalk"),
            (OPCODE_STEP_NORTH_EAST, "inline:playerMove"),
            (OPCODE_STEP_SOUTH_EAST, "inline:playerMove"),
            (OPCODE_STEP_SOUTH_WEST, "inline:playerMove"),
            (OPCODE_STEP_NORTH_WEST, "inline:playerMove"),
        ] {
            let opcode_fragment = format!("\"opcode\": {opcode}");
            let method_fragment = format!("\"method\": \"{method}\"");
            let entry = CURRENT_INDEX
                .split(&opcode_fragment)
                .nth(1)
                .and_then(|suffix| suffix.split("    },").next())
                .unwrap_or("");
            assert!(entry.contains(&method_fragment), "missing {opcode:#04X} {method}");
            assert!(entry.contains("\"direction\": \"client-to-server\""));
            assert!(entry.contains("\"dispatch_phase\": \"gameplay-session\""));
        }
    }
}
