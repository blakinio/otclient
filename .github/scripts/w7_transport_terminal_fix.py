from pathlib import Path

path = Path("oteryn-client/crates/transport/src/lib.rs")
text = path.read_text(encoding="utf-8")

old = """    fn apply_terminal_result(
        &mut self,
        result: Result<(), TransportError>,
    ) -> Result<(), TransportError> {
        if let Err(error) = result {
            if error.kind() == TransportErrorKind::ConnectionLost {
                self.close();
            }
            return Err(error);
        }
        Ok(())
    }
"""
new = """    fn apply_terminal_result(
        &mut self,
        result: Result<(), TransportError>,
    ) -> Result<(), TransportError> {
        if let Err(error) = result {
            // Any error after frame I/O begins can leave the byte stream at an
            // unknown frame boundary. Close terminally rather than permitting
            // a caller to reuse a potentially desynchronized connection.
            self.close();
            return Err(error);
        }
        Ok(())
    }
"""
if text.count(old) != 1:
    raise SystemExit("expected one apply_terminal_result implementation")
text = text.replace(old, new, 1)

old = """        assert_eq!(
            connected.read_exact_bounded(1, &connected_source.token()),
            Err(TransportError::new(TransportErrorKind::Cancelled))
        );
        Ok(())
"""
new = """        assert_eq!(
            connected.read_exact_bounded(1, &connected_source.token()),
            Err(TransportError::new(TransportErrorKind::Cancelled))
        );
        assert_eq!(connected.state(), ConnectionState::Closed);
        Ok(())
"""
if text.count(old) != 1:
    raise SystemExit("expected one connected cancellation assertion")
text = text.replace(old, new, 1)

old = """        assert_eq!(
            timed.read_exact_bounded(1, &source.token()),
            Err(TransportError::new(TransportErrorKind::Timeout))
        );
        drop(server);
"""
new = """        assert_eq!(
            timed.read_exact_bounded(1, &source.token()),
            Err(TransportError::new(TransportErrorKind::Timeout))
        );
        assert_eq!(timed.state(), ConnectionState::Closed);
        drop(server);
"""
if text.count(old) != 1:
    raise SystemExit("expected one timeout assertion")
text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
