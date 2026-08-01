from pathlib import Path


identity_path = Path("oteryn-client/crates/identity/src/lib.rs")
identity = identity_path.read_text(encoding="utf-8")
old_docs = """/// One accepted TCP callback request reduced to the security-relevant facts.
///
/// The request target contains OAuth code/state material and is retained by a
/// non-cloneable redacted owner that overwrites its project-owned bytes on drop.
"""
new_docs = """/// One accepted TCP callback request reduced to the security-relevant facts.
///
/// The request target contains OAuth code/state material and is retained by a
/// non-cloneable redacted owner that overwrites its project-owned bytes on drop.
/// External callers can construct an attempt and inspect only its non-secret peer;
/// they cannot mutate, take or replace the accepted target.
///
/// ```compile_fail
/// use oteryn_identity::CallbackAttempt;
/// use std::net::{IpAddr, Ipv4Addr};
///
/// fn main() -> Result<(), Box<dyn std::error::Error>> {
///     let mut attempt = CallbackAttempt::new(
///         IpAddr::V4(Ipv4Addr::LOCALHOST),
///         "/callback?code=secret&state=secret".to_owned(),
///     )?;
///     attempt.target.clear();
///     Ok(())
/// }
/// ```
"""
if identity.count(old_docs) != 1:
    raise SystemExit("identity callback documentation anchor mismatch")
identity = identity.replace(old_docs, new_docs, 1)
old_field = """    /// Exact HTTP request target including query. The enclosing non-cloneable
    /// attempt overwrites this project-owned allocation on terminal drop.
    pub target: String,
"""
new_field = """    /// Exact HTTP request target including query. The enclosing non-cloneable
    /// attempt overwrites this project-owned allocation on terminal drop.
    target: String,
"""
if identity.count(old_field) != 1:
    raise SystemExit("identity callback target field anchor mismatch")
identity = identity.replace(old_field, new_field, 1)
identity_path.write_text(identity, encoding="utf-8")

game_path = Path("oteryn-client/crates/game-session/src/lib.rs")
game = game_path.read_text(encoding="utf-8")
old_owner = """struct SecretBytes(Box<[u8]>);

impl SecretBytes {
    fn new(secret: Vec<u8>) -> Result<Self, CredentialValidationError> {
        if secret.is_empty() {
            return Err(CredentialValidationError::Empty);
        }
        if secret.len() > MAX_GAME_ENTRY_CREDENTIAL_BYTES {
            return Err(CredentialValidationError::TooLarge);
        }
        Ok(Self(secret.into_boxed_slice()))
    }

    fn as_slice(&self) -> &[u8] {
        &self.0
    }

    fn clear(&mut self) {
        self.0.fill(0);
    }
}
"""
new_owner = """struct SecretBytes(Vec<u8>);

impl SecretBytes {
    fn new(mut secret: Vec<u8>) -> Result<Self, CredentialValidationError> {
        Self::validate_for_ownership(&mut secret)?;
        Ok(Self(secret))
    }

    fn validate_for_ownership(secret: &mut [u8]) -> Result<(), CredentialValidationError> {
        if secret.is_empty() {
            return Err(CredentialValidationError::Empty);
        }
        if secret.len() > MAX_GAME_ENTRY_CREDENTIAL_BYTES {
            secret.fill(0);
            return Err(CredentialValidationError::TooLarge);
        }
        Ok(())
    }

    fn as_slice(&self) -> &[u8] {
        &self.0
    }

    fn clear(&mut self) {
        self.0.fill(0);
    }
}
"""
if game.count(old_owner) != 1:
    raise SystemExit("game secret owner anchor mismatch")
game = game.replace(old_owner, new_owner, 1)
old_test = """    #[test]
    fn secret_storage_overwrite_is_explicit() -> Result<(), CredentialValidationError> {
        let mut secret = SecretBytes::new(b"erase-me".to_vec())?;
        secret.clear();
        assert!(secret.as_slice().iter().all(|byte| *byte == 0));
        Ok(())
    }
"""
new_test = """    #[test]
    fn secret_storage_overwrite_is_explicit() -> Result<(), CredentialValidationError> {
        let mut secret = SecretBytes::new(b"erase-me".to_vec())?;
        secret.clear();
        assert!(secret.as_slice().iter().all(|byte| *byte == 0));
        Ok(())
    }

    #[test]
    fn oversized_secret_input_is_cleared_before_rejection() {
        let mut secret = vec![0xa5; MAX_GAME_ENTRY_CREDENTIAL_BYTES + 1];
        assert_eq!(
            SecretBytes::validate_for_ownership(&mut secret),
            Err(CredentialValidationError::TooLarge)
        );
        assert!(secret.iter().all(|byte| *byte == 0));
    }
"""
if game.count(old_test) != 1:
    raise SystemExit("game cleanup test anchor mismatch")
game = game.replace(old_test, new_test, 1)
game_path.write_text(game, encoding="utf-8")
