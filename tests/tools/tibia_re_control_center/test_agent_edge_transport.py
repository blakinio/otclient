from __future__ import annotations

import unittest

from tools.tibia_re_control_center.agent_edge_transport import (
    EdgeFrameKind,
    EdgeTransportSigner,
    EdgeTransportVerifier,
)

EDGE_KEY = b"e" * 32
MOLEHILL_KEY = b"m" * 32


class AgentEdgeTransportTests(unittest.TestCase):
    def test_authenticated_observation_round_trip_is_authority_neutral(self):
        signer = EdgeTransportSigner(
            local_peer_id="synology-edge",
            local_auth_key=EDGE_KEY,
        )
        verifier = EdgeTransportVerifier(
            expected_peer_id="synology-edge",
            expected_peer_auth_key=EDGE_KEY,
        )

        packet = signer.seal(
            kind=EdgeFrameKind.OBSERVATION,
            connection_id="connection-1",
            sequence=1,
            sent_epoch_ms=1_000_000,
            payload={"runtime_signal": "LOGIN_SCREEN", "artifact_refs": []},
        )
        verified = verifier.verify(packet, now_epoch_ms=1_000_100)

        self.assertTrue(verified.peer_authenticated)
        self.assertEqual("LOGIN_SCREEN", verified.payload["runtime_signal"])
        self.assertFalse(verified.mutation_authorized)
        self.assertEqual(0, verified.physical_action_budget)
        self.assertFalse(verified.evidence_fresh)
        self.assertFalse(verified.action_resume_allowed)


    def test_duplicate_json_keys_are_rejected_before_authentication(self):
        verifier = EdgeTransportVerifier(
            expected_peer_id="synology-edge",
            expected_peer_auth_key=EDGE_KEY,
        )
        packet = (
            b'{"schema":"otclient.local-agent.edge-transport.v1",'
            b'"schema":"otclient.local-agent.edge-transport.v1"}'
        )
        with self.assertRaisesRegex(Exception, "duplicate|valid UTF-8 JSON"):
            verifier.verify(packet, now_epoch_ms=1_000_000)


    def test_content_addressed_artifact_detects_tampering(self):
        from tools.tibia_re_control_center.agent_edge_transport import (
            describe_artifact,
            verify_artifact_bytes,
        )

        payload = b"secret-safe-frame-bytes"
        descriptor = describe_artifact(payload, media_type="image/png")
        self.assertEqual(len(payload), descriptor.size_bytes)
        self.assertTrue(descriptor.ref.startswith("sha256:"))
        self.assertEqual(payload, verify_artifact_bytes(descriptor, payload))

        with self.assertRaisesRegex(Exception, "integrity|size|hash"):
            verify_artifact_bytes(descriptor, payload + b"tampered")


    def test_reconnect_requires_explicit_new_connection_binding_and_no_resume(self):
        signer = EdgeTransportSigner(local_peer_id="synology-edge", local_auth_key=EDGE_KEY)
        verifier = EdgeTransportVerifier(
            expected_peer_id="synology-edge",
            expected_peer_auth_key=EDGE_KEY,
            expected_connection_id="connection-1",
        )
        first = signer.seal(
            kind=EdgeFrameKind.HEARTBEAT,
            connection_id="connection-1",
            sequence=1,
            sent_epoch_ms=1_000_000,
            payload={"edge_state": "ONLINE"},
        )
        self.assertEqual(1, verifier.verify(first, now_epoch_ms=1_000_001).sequence)

        verifier.bind_connection("connection-2")
        second = signer.seal(
            kind=EdgeFrameKind.HEARTBEAT,
            connection_id="connection-2",
            sequence=1,
            sent_epoch_ms=1_000_002,
            payload={"edge_state": "ONLINE"},
        )
        verified = verifier.verify(second, now_epoch_ms=1_000_003)
        self.assertFalse(verified.evidence_fresh)
        self.assertFalse(verified.action_resume_allowed)

        old_connection = signer.seal(
            kind=EdgeFrameKind.HEARTBEAT,
            connection_id="connection-1",
            sequence=2,
            sent_epoch_ms=1_000_004,
            payload={"edge_state": "ONLINE"},
        )
        with self.assertRaisesRegex(Exception, "connection"):
            verifier.verify(old_connection, now_epoch_ms=1_000_005)


    def test_metadata_frames_are_bounded_on_send_and_receive(self):
        signer = EdgeTransportSigner(local_peer_id="synology-edge", local_auth_key=EDGE_KEY)
        verifier = EdgeTransportVerifier(
            expected_peer_id="synology-edge",
            expected_peer_auth_key=EDGE_KEY,
        )
        with self.assertRaisesRegex(Exception, "size|large|bound"):
            signer.seal(
                kind=EdgeFrameKind.OBSERVATION,
                connection_id="connection-large",
                sequence=1,
                sent_epoch_ms=1_000_000,
                payload={"blob": "x" * 300_000},
            )
        with self.assertRaisesRegex(Exception, "size|large|bound"):
            verifier.verify(b"{" + b" " * 300_000 + b"}", now_epoch_ms=1_000_000)


    def test_generic_shell_gui_and_secret_getter_payloads_are_absent(self):
        signer = EdgeTransportSigner(local_peer_id="synology-edge", local_auth_key=EDGE_KEY)
        forbidden_payloads = (
            {"command": "whoami"},
            {"nested": {"click": [10, 20]}},
            {"get_secret": "login"},
        )
        for payload in forbidden_payloads:
            with self.subTest(payload=payload), self.assertRaisesRegex(Exception, "control|forbidden|authority"):
                signer.seal(
                    kind=EdgeFrameKind.OBSERVATION,
                    connection_id="connection-safe",
                    sequence=1,
                    sent_epoch_ms=1_000_000,
                    payload=payload,
                )


    def test_outbound_client_requires_mutual_authentication_before_sending_observations(self):
        import socket
        import struct
        import threading

        from tools.tibia_re_control_center.agent_edge_transport import (
            EdgeOutboundClient,
        )

        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        host, port = listener.getsockname()
        received = []
        failures = []

        def recv_packet(conn):
            header = conn.recv(4)
            if len(header) != 4:
                raise RuntimeError("short header")
            length = struct.unpack("!I", header)[0]
            data = b""
            while len(data) < length:
                chunk = conn.recv(length - len(data))
                if not chunk:
                    raise RuntimeError("short frame")
                data += chunk
            return data

        def send_packet(conn, packet):
            conn.sendall(struct.pack("!I", len(packet)) + packet)

        def server_worker():
            try:
                conn, _ = listener.accept()
                with conn:
                    hello_packet = recv_packet(conn)
                    verifier = EdgeTransportVerifier(
                        expected_peer_id="synology-edge",
                        expected_peer_auth_key=EDGE_KEY,
                    )
                    hello = verifier.verify(hello_packet, now_epoch_ms=1_000_001)
                    self.assertEqual(EdgeFrameKind.HELLO, hello.kind)
                    self.assertEqual("OUTBOUND_ONLY", hello.payload["transport_mode"])
                    signer = EdgeTransportSigner(
                        local_peer_id="molehill-control",
                        local_auth_key=MOLEHILL_KEY,
                    )
                    ack = signer.seal(
                        kind=EdgeFrameKind.HELLO_ACK,
                        connection_id=hello.connection_id,
                        sequence=1,
                        sent_epoch_ms=1_000_002,
                        payload={
                            "acknowledged_peer_id": "synology-edge",
                            "transport_mode": "OUTBOUND_ONLY",
                        },
                    )
                    send_packet(conn, ack)
                    observation = verifier.verify(recv_packet(conn), now_epoch_ms=1_000_004)
                    received.append(observation)
            except Exception as exc:  # noqa: BLE001 - test thread forwards failures
                failures.append(exc)
            finally:
                listener.close()

        thread = threading.Thread(target=server_worker)
        thread.start()
        client = EdgeOutboundClient(
            local_peer_id="synology-edge",
            local_auth_key=EDGE_KEY,
            expected_remote_peer_id="molehill-control",
            expected_remote_auth_key=MOLEHILL_KEY,
        )
        channel = client.connect(host, port, now_epoch_ms=1_000_000)
        try:
            self.assertTrue(channel.peer_authenticated)
            self.assertFalse(channel.mutation_authorized)
            self.assertFalse(channel.action_resume_allowed)
            channel.send(
                EdgeFrameKind.OBSERVATION,
                {"runtime_signal": "LOGIN_SCREEN", "artifact_refs": []},
                sent_epoch_ms=1_000_003,
            )
        finally:
            channel.close()
        thread.join(timeout=3)
        self.assertFalse(thread.is_alive())
        if failures:
            raise failures[0]
        self.assertEqual(1, len(received))
        self.assertEqual(EdgeFrameKind.OBSERVATION, received[0].kind)
        self.assertFalse(received[0].evidence_fresh)


    def test_artifact_descriptor_metadata_is_versioned_and_self_consistent(self):
        from tools.tibia_re_control_center.agent_edge_transport import (
            EdgeArtifactDescriptor,
            describe_artifact,
        )

        descriptor = describe_artifact(b"frame", media_type="image/png")
        mapping = descriptor.as_mapping()
        self.assertEqual("otclient.local-agent.artifact-ref.v1", mapping["schema"])
        self.assertEqual(descriptor, EdgeArtifactDescriptor.from_mapping(mapping))

        forged = dict(mapping)
        forged["ref"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(Exception, "descriptor|hash|ref"):
            EdgeArtifactDescriptor.from_mapping(forged)


    def test_wrong_peer_and_wrong_key_fail_closed(self):
        from tools.tibia_re_control_center.model import ValidationError

        packet = EdgeTransportSigner(
            local_peer_id="synology-edge", local_auth_key=EDGE_KEY
        ).seal(
            kind=EdgeFrameKind.HEARTBEAT,
            connection_id="connection-auth",
            sequence=1,
            sent_epoch_ms=1_000_000,
            payload={"edge_state": "ONLINE"},
        )
        with self.assertRaises(ValidationError) as wrong_peer:
            EdgeTransportVerifier(
                expected_peer_id="different-edge",
                expected_peer_auth_key=EDGE_KEY,
            ).verify(packet, now_epoch_ms=1_000_001)
        self.assertEqual("EDGE_PEER_REJECTED", wrong_peer.exception.code)

        with self.assertRaises(ValidationError) as wrong_key:
            EdgeTransportVerifier(
                expected_peer_id="synology-edge",
                expected_peer_auth_key=b"x" * 32,
            ).verify(packet, now_epoch_ms=1_000_001)
        self.assertEqual("EDGE_AUTHENTICATION_FAILED", wrong_key.exception.code)

    def test_replay_stale_and_future_frames_do_not_advance_replay_state(self):
        from tools.tibia_re_control_center.model import ValidationError

        signer = EdgeTransportSigner(local_peer_id="synology-edge", local_auth_key=EDGE_KEY)
        verifier = EdgeTransportVerifier(
            expected_peer_id="synology-edge",
            expected_peer_auth_key=EDGE_KEY,
            expected_connection_id="connection-replay",
            max_age_ms=100,
            max_future_skew_ms=10,
        )
        first = signer.seal(
            kind=EdgeFrameKind.HEARTBEAT,
            connection_id="connection-replay",
            sequence=1,
            sent_epoch_ms=1_000,
            payload={"edge_state": "ONLINE"},
        )
        verifier.verify(first, now_epoch_ms=1_001)
        with self.assertRaises(ValidationError) as replay:
            verifier.verify(first, now_epoch_ms=1_002)
        self.assertEqual("EDGE_REPLAY_REJECTED", replay.exception.code)
        self.assertEqual(1, verifier.last_accepted_sequence)

        stale = signer.seal(
            kind=EdgeFrameKind.HEARTBEAT,
            connection_id="connection-replay",
            sequence=2,
            sent_epoch_ms=800,
            payload={"edge_state": "ONLINE"},
        )
        with self.assertRaises(ValidationError) as stale_error:
            verifier.verify(stale, now_epoch_ms=1_003)
        self.assertEqual("EDGE_STALE_REJECTED", stale_error.exception.code)
        self.assertEqual(1, verifier.last_accepted_sequence)

        future = signer.seal(
            kind=EdgeFrameKind.HEARTBEAT,
            connection_id="connection-replay",
            sequence=2,
            sent_epoch_ms=2_000,
            payload={"edge_state": "ONLINE"},
        )
        with self.assertRaises(ValidationError) as future_error:
            verifier.verify(future, now_epoch_ms=1_004)
        self.assertEqual("EDGE_STALE_REJECTED", future_error.exception.code)
        self.assertEqual(1, verifier.last_accepted_sequence)

    def test_authenticated_peer_cannot_expand_authority_or_protocol_version(self):
        import hashlib
        import hmac
        import json

        from tools.tibia_re_control_center.canonical import jcs_dumps
        from tools.tibia_re_control_center.model import ValidationError

        packet = EdgeTransportSigner(
            local_peer_id="synology-edge", local_auth_key=EDGE_KEY
        ).seal(
            kind=EdgeFrameKind.OBSERVATION,
            connection_id="connection-authority",
            sequence=1,
            sent_epoch_ms=1_000_000,
            payload={"runtime_signal": "LOGIN_SCREEN"},
        )
        decoded = json.loads(packet.decode("utf-8"))
        decoded["mutation_authorized"] = True
        unsigned = dict(decoded)
        unsigned.pop("auth_tag")
        decoded["auth_tag"] = hmac.new(
            EDGE_KEY, jcs_dumps(unsigned).encode("utf-8"), hashlib.sha256
        ).hexdigest()
        forged = jcs_dumps(decoded).encode("utf-8")
        with self.assertRaises(ValidationError) as authority:
            EdgeTransportVerifier(
                expected_peer_id="synology-edge",
                expected_peer_auth_key=EDGE_KEY,
            ).verify(forged, now_epoch_ms=1_000_001)
        self.assertEqual("EDGE_AUTHORITY_EXPANSION_REJECTED", authority.exception.code)

        decoded["mutation_authorized"] = False
        decoded["protocol_major"] = 999
        unsigned = dict(decoded)
        unsigned.pop("auth_tag")
        decoded["auth_tag"] = hmac.new(
            EDGE_KEY, jcs_dumps(unsigned).encode("utf-8"), hashlib.sha256
        ).hexdigest()
        wrong_version = jcs_dumps(decoded).encode("utf-8")
        with self.assertRaises(ValidationError) as version:
            EdgeTransportVerifier(
                expected_peer_id="synology-edge",
                expected_peer_auth_key=EDGE_KEY,
            ).verify(wrong_version, now_epoch_ms=1_000_001)
        self.assertEqual("EDGE_VERSION_REJECTED", version.exception.code)


    def test_same_connection_cannot_reset_replay_window(self):
        from tools.tibia_re_control_center.model import ValidationError

        signer = EdgeTransportSigner(local_peer_id="synology-edge", local_auth_key=EDGE_KEY)
        verifier = EdgeTransportVerifier(
            expected_peer_id="synology-edge",
            expected_peer_auth_key=EDGE_KEY,
            expected_connection_id="connection-fixed",
        )
        packet = signer.seal(
            kind=EdgeFrameKind.HEARTBEAT,
            connection_id="connection-fixed",
            sequence=1,
            sent_epoch_ms=1_000,
            payload={"edge_state": "ONLINE"},
        )
        verifier.verify(packet, now_epoch_ms=1_001)
        with self.assertRaises(ValidationError) as rebound:
            verifier.bind_connection("connection-fixed")
        self.assertEqual("EDGE_CONNECTION_REUSE_REJECTED", rebound.exception.code)
        self.assertEqual(1, verifier.last_accepted_sequence)
        with self.assertRaises(ValidationError) as replay:
            verifier.verify(packet, now_epoch_ms=1_002)
        self.assertEqual("EDGE_REPLAY_REJECTED", replay.exception.code)


    def test_send_failure_latches_channel_closed_and_never_retries_same_stream(self):
        from tools.tibia_re_control_center.agent_edge_transport import (
            EdgeOutboundChannel,
        )
        from tools.tibia_re_control_center.model import ValidationError

        class BrokenSocket:
            def __init__(self):
                self.send_calls = 0
                self.closed = False

            def sendall(self, _data):
                self.send_calls += 1
                raise OSError("synthetic send failure")

            def shutdown(self, _how):
                return None

            def close(self):
                self.closed = True

        connection = BrokenSocket()
        channel = EdgeOutboundChannel(
            connection=connection,
            signer=EdgeTransportSigner(local_peer_id="synology-edge", local_auth_key=EDGE_KEY),
            connection_id="connection-failed",
        )
        with self.assertRaises(ValidationError) as first:
            channel.send(
                EdgeFrameKind.HEARTBEAT,
                {"edge_state": "ONLINE"},
                sent_epoch_ms=1_000,
            )
        self.assertEqual("EDGE_SEND_FAILED", first.exception.code)
        with self.assertRaises(ValidationError) as second:
            channel.send(
                EdgeFrameKind.HEARTBEAT,
                {"edge_state": "ONLINE"},
                sent_epoch_ms=1_001,
            )
        self.assertEqual("EDGE_CONNECTION_CLOSED", second.exception.code)
        self.assertEqual(1, connection.send_calls)
        self.assertTrue(connection.closed)


    def test_concurrent_outbound_sends_receive_unique_monotonic_sequences(self):
        import threading
        import time

        from tools.tibia_re_control_center.agent_edge_transport import (
            EdgeOutboundChannel,
        )

        class SlowSocket:
            def __init__(self):
                self.first_entered = threading.Event()
                self.release = threading.Event()
                self.calls = 0
                self.guard = threading.Lock()

            def sendall(self, _data):
                with self.guard:
                    self.calls += 1
                    if self.calls == 1:
                        self.first_entered.set()
                self.release.wait(timeout=2)

            def shutdown(self, _how):
                return None

            def close(self):
                return None

        connection = SlowSocket()
        channel = EdgeOutboundChannel(
            connection=connection,
            signer=EdgeTransportSigner(local_peer_id="synology-edge", local_auth_key=EDGE_KEY),
            connection_id="connection-concurrent",
        )
        sequences = []

        def worker(index):
            sequences.append(channel.send(
                EdgeFrameKind.HEARTBEAT,
                {"edge_state": "ONLINE", "index": index},
                sent_epoch_ms=1_000 + index,
            ))

        first = threading.Thread(target=worker, args=(1,))
        second = threading.Thread(target=worker, args=(2,))
        first.start()
        self.assertTrue(connection.first_entered.wait(timeout=1))
        second.start()
        time.sleep(0.05)
        connection.release.set()
        first.join(timeout=2)
        second.join(timeout=2)
        self.assertFalse(first.is_alive())
        self.assertFalse(second.is_alive())
        self.assertEqual([2, 3], sorted(sequences))


    def test_mutual_authentication_requires_distinct_directional_pairing_keys(self):
        from tools.tibia_re_control_center.agent_edge_transport import (
            EdgeOutboundClient,
        )
        from tools.tibia_re_control_center.model import ValidationError

        with self.assertRaises(ValidationError) as raised:
            EdgeOutboundClient(
                local_peer_id="synology-edge",
                local_auth_key=EDGE_KEY,
                expected_remote_peer_id="molehill-control",
                expected_remote_auth_key=EDGE_KEY,
            )
        self.assertEqual("EDGE_PAIRING_KEY_REUSE_REJECTED", raised.exception.code)


    def test_artifact_bytes_are_transferred_separately_after_signed_descriptor(self):
        import socket
        import struct
        import threading

        from tools.tibia_re_control_center.agent_edge_transport import (
            EdgeArtifactDescriptor,
            EdgeOutboundClient,
            verify_artifact_bytes,
        )

        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        host, port = listener.getsockname()
        received = []
        failures = []

        def recv_packet(conn):
            header = conn.recv(4)
            if len(header) != 4:
                raise RuntimeError("short header")
            length = struct.unpack("!I", header)[0]
            data = b""
            while len(data) < length:
                chunk = conn.recv(length - len(data))
                if not chunk:
                    raise RuntimeError("short frame")
                data += chunk
            return data

        def send_packet(conn, packet):
            conn.sendall(struct.pack("!I", len(packet)) + packet)

        def server_worker():
            try:
                conn, _ = listener.accept()
                with conn:
                    verifier = EdgeTransportVerifier(
                        expected_peer_id="synology-edge",
                        expected_peer_auth_key=EDGE_KEY,
                    )
                    hello = verifier.verify(recv_packet(conn), now_epoch_ms=2_000_001)
                    ack = EdgeTransportSigner(
                        local_peer_id="molehill-control",
                        local_auth_key=MOLEHILL_KEY,
                    ).seal(
                        kind=EdgeFrameKind.HELLO_ACK,
                        connection_id=hello.connection_id,
                        sequence=1,
                        sent_epoch_ms=2_000_002,
                        payload={
                            "acknowledged_peer_id": "synology-edge",
                            "transport_mode": "OUTBOUND_ONLY",
                        },
                    )
                    send_packet(conn, ack)
                    metadata = verifier.verify(recv_packet(conn), now_epoch_ms=2_000_004)
                    self.assertEqual(EdgeFrameKind.ARTIFACT, metadata.kind)
                    self.assertEqual({"artifact"}, set(metadata.payload))
                    descriptor = EdgeArtifactDescriptor.from_mapping(metadata.payload["artifact"])
                    received.append(verify_artifact_bytes(descriptor, recv_packet(conn)))
            except Exception as exc:  # noqa: BLE001 - test thread forwards failures
                failures.append(exc)
            finally:
                listener.close()

        thread = threading.Thread(target=server_worker)
        thread.start()
        client = EdgeOutboundClient(
            local_peer_id="synology-edge",
            local_auth_key=EDGE_KEY,
            expected_remote_peer_id="molehill-control",
            expected_remote_auth_key=MOLEHILL_KEY,
        )
        channel = client.connect(host, port, now_epoch_ms=2_000_000)
        try:
            sequence, descriptor = channel.send_artifact(
                b"secret-safe-frame-bytes",
                media_type="image/png",
                sent_epoch_ms=2_000_003,
            )
            self.assertEqual(2, sequence)
            self.assertTrue(descriptor.ref.startswith("sha256:"))
        finally:
            channel.close()
        thread.join(timeout=3)
        self.assertFalse(thread.is_alive())
        if failures:
            raise failures[0]
        self.assertEqual([b"secret-safe-frame-bytes"], received)


    def test_artifact_descriptor_refuses_declared_size_above_transport_bound(self):
        from tools.tibia_re_control_center.agent_edge_transport import (
            MAX_ARTIFACT_BYTES,
            EdgeArtifactDescriptor,
        )
        from tools.tibia_re_control_center.model import ValidationError

        digest = "a" * 64
        mapping = {
            "schema": "otclient.local-agent.artifact-ref.v1",
            "ref": f"sha256:{digest}",
            "sha256": digest,
            "size_bytes": MAX_ARTIFACT_BYTES + 1,
            "media_type": "image/png",
        }
        with self.assertRaises(ValidationError) as raised:
            EdgeArtifactDescriptor.from_mapping(mapping)
        self.assertEqual("EDGE_ARTIFACT_TOO_LARGE", raised.exception.code)


    def test_receiver_reads_only_exact_descriptor_sized_artifact_frame(self):
        import struct

        from tools.tibia_re_control_center.agent_edge_transport import (
            describe_artifact,
            receive_artifact_bytes,
        )
        from tools.tibia_re_control_center.model import ValidationError

        class BufferSocket:
            def __init__(self, data):
                self.data = data

            def recv(self, size):
                chunk, self.data = self.data[:size], self.data[size:]
                return chunk

        payload = b"frame-bytes"
        descriptor = describe_artifact(payload, media_type="image/png")
        connection = BufferSocket(struct.pack("!I", len(payload)) + payload)
        self.assertEqual(payload, receive_artifact_bytes(connection, descriptor))

        wrong_length = BufferSocket(struct.pack("!I", len(payload) + 1) + payload + b"x")
        with self.assertRaises(ValidationError) as raised:
            receive_artifact_bytes(wrong_length, descriptor)
        self.assertEqual("EDGE_ARTIFACT_LENGTH_MISMATCH", raised.exception.code)


    def test_generic_metadata_send_cannot_bypass_separate_artifact_path(self):
        from tools.tibia_re_control_center.agent_edge_transport import (
            EdgeOutboundChannel,
        )
        from tools.tibia_re_control_center.model import ValidationError

        class SinkSocket:
            def __init__(self):
                self.calls = 0

            def sendall(self, _data):
                self.calls += 1

            def shutdown(self, _how):
                return None

            def close(self):
                return None

        connection = SinkSocket()
        channel = EdgeOutboundChannel(
            connection=connection,
            signer=EdgeTransportSigner(local_peer_id="synology-edge", local_auth_key=EDGE_KEY),
            connection_id="connection-artifact-bypass",
        )
        with self.assertRaises(ValidationError) as raised:
            channel.send(
                EdgeFrameKind.ARTIFACT,
                {"artifact": {"ref": "not-admitted"}},
                sent_epoch_ms=1_000,
            )
        self.assertEqual("EDGE_DIRECTION_REJECTED", raised.exception.code)
        self.assertEqual(0, connection.calls)


    def test_artifact_media_type_is_plain_bounded_metadata_not_secret_carrier(self):
        from tools.tibia_re_control_center.agent_edge_transport import describe_artifact
        from tools.tibia_re_control_center.model import ValidationError

        for media_type in ("image/png; password=hunter2", "image/png\nX-Control: value", "not-a-media-type"):
            with self.subTest(media_type=media_type), self.assertRaises(ValidationError):
                describe_artifact(b"frame", media_type=media_type)


    def test_endpoint_resolution_rejects_public_network_destinations(self):
        from tools.tibia_re_control_center.agent_edge_transport import (
            resolve_edge_endpoint,
        )
        from tools.tibia_re_control_center.model import ValidationError

        with self.assertRaises(ValidationError) as raised:
            resolve_edge_endpoint("8.8.8.8", 443)
        self.assertEqual("EDGE_ENDPOINT_PUBLIC_REJECTED", raised.exception.code)
        self.assertEqual("127.0.0.1", resolve_edge_endpoint("127.0.0.1", 12345))


    def test_signer_deep_snapshots_payload_before_privacy_admission(self):
        import json

        import tools.tibia_re_control_center.agent_edge_transport as transport_module

        payload = {"nested": {"state": "LOGIN_SCREEN"}}
        original_guard = transport_module.ensure_no_secret_material

        def guard_then_mutate(value, *, key_path):
            original_guard(value, key_path=key_path)
            payload["nested"]["token"] = "secret-after-scan"

        transport_module.ensure_no_secret_material = guard_then_mutate
        try:
            packet = EdgeTransportSigner(
                local_peer_id="synology-edge", local_auth_key=EDGE_KEY
            ).seal(
                kind=EdgeFrameKind.OBSERVATION,
                connection_id="connection-snapshot",
                sequence=1,
                sent_epoch_ms=1_000,
                payload=payload,
            )
        finally:
            transport_module.ensure_no_secret_material = original_guard

        decoded = json.loads(packet.decode("utf-8"))
        self.assertEqual({"state": "LOGIN_SCREEN"}, decoded["payload"]["nested"])
        self.assertIn("token", payload["nested"])



    def test_endpoint_rejects_reserved_nonlocal_ranges(self):
        from tools.tibia_re_control_center.agent_edge_transport import (
            resolve_edge_endpoint,
        )
        from tools.tibia_re_control_center.model import ValidationError

        for address in ("192.0.2.1", "198.51.100.1", "203.0.113.1"):
            with self.subTest(address=address):
                with self.assertRaises(ValidationError) as raised:
                    resolve_edge_endpoint(address, 12345)
                self.assertEqual("EDGE_ENDPOINT_PUBLIC_REJECTED", raised.exception.code)

    def test_control_surface_key_normalization_blocks_separator_variants(self):
        from tools.tibia_re_control_center.model import ValidationError

        signer = EdgeTransportSigner(local_peer_id="synology-edge", local_auth_key=EDGE_KEY)
        for key in ("get secret", "get.secret", "shell command", "gui/control"):
            with self.subTest(key=key):
                with self.assertRaises(ValidationError) as raised:
                    signer.seal(
                        kind=EdgeFrameKind.OBSERVATION,
                        connection_id="connection-normalized-control",
                        sequence=1,
                        sent_epoch_ms=1_000,
                        payload={key: "value"},
                    )
                self.assertEqual("EDGE_CONTROL_SURFACE_REJECTED", raised.exception.code)


    def test_payload_structure_is_bounded_and_json_only(self):
        from tools.tibia_re_control_center.model import ValidationError

        signer = EdgeTransportSigner(local_peer_id="synology-edge", local_auth_key=EDGE_KEY)
        nested = {"value": "ok"}
        for _ in range(20):
            nested = {"nested": nested}
        cases = (
            (nested, "EDGE_PAYLOAD_TOO_DEEP"),
            ({"value": object()}, "EDGE_PAYLOAD_INVALID"),
            ({"items": list(range(4097))}, "EDGE_PAYLOAD_TOO_LARGE"),
        )
        for payload, code in cases:
            with self.subTest(code=code):
                with self.assertRaises(ValidationError) as raised:
                    signer.seal(kind=EdgeFrameKind.OBSERVATION, connection_id="bounded-payload", sequence=1, sent_epoch_ms=1_000, payload=payload)
                self.assertEqual(code, raised.exception.code)

    def test_boolean_protocol_and_budget_fields_are_rejected_even_when_signed(self):
        import hashlib
        import hmac
        import json

        from tools.tibia_re_control_center.canonical import jcs_dumps
        from tools.tibia_re_control_center.model import ValidationError

        packet = EdgeTransportSigner(local_peer_id="synology-edge", local_auth_key=EDGE_KEY).seal(kind=EdgeFrameKind.HEARTBEAT, connection_id="strict-types", sequence=1, sent_epoch_ms=1_000, payload={"edge_state": "ONLINE"})
        for field, value in (("protocol_major", True), ("physical_action_budget", False)):
            decoded = json.loads(packet.decode("utf-8"))
            decoded[field] = value
            unsigned = dict(decoded)
            unsigned.pop("auth_tag")
            decoded["auth_tag"] = hmac.new(EDGE_KEY, jcs_dumps(unsigned).encode("utf-8"), hashlib.sha256).hexdigest()
            with self.subTest(field=field), self.assertRaises(ValidationError):
                EdgeTransportVerifier(expected_peer_id="synology-edge", expected_peer_auth_key=EDGE_KEY).verify(jcs_dumps(decoded).encode("utf-8"), now_epoch_ms=1_001)

    def test_timeout_must_be_finite(self):
        from tools.tibia_re_control_center.agent_edge_transport import (
            EdgeOutboundClient,
        )
        from tools.tibia_re_control_center.model import ValidationError

        with self.assertRaises(ValidationError) as raised:
            EdgeOutboundClient(local_peer_id="synology-edge", local_auth_key=EDGE_KEY, expected_remote_peer_id="molehill-control", expected_remote_auth_key=MOLEHILL_KEY, timeout_seconds=float("nan"))
        self.assertEqual("EDGE_TIMEOUT_INVALID", raised.exception.code)

    def test_authenticated_receiver_reapplies_payload_structure_bounds(self):
        import hashlib
        import hmac

        from tools.tibia_re_control_center.canonical import jcs_dumps
        from tools.tibia_re_control_center.model import ValidationError

        payload = {"value": "ok"}
        for _ in range(20):
            payload = {"nested": payload}
        unsigned = {
            "schema": "otclient.local-agent.edge-transport.v1",
            "protocol_major": 1,
            "sender_peer_id": "synology-edge",
            "connection_id": "receiver-bounds",
            "sequence": 1,
            "sent_epoch_ms": 1_000,
            "kind": "OBSERVATION",
            "authority_scope": "PEER_IDENTITY_ONLY",
            "mutation_authorized": False,
            "physical_action_budget": 0,
            "evidence_fresh": False,
            "action_resume_allowed": False,
            "payload": payload,
        }
        unsigned["auth_tag"] = hmac.new(EDGE_KEY, jcs_dumps(unsigned).encode("utf-8"), hashlib.sha256).hexdigest()
        with self.assertRaises(ValidationError) as raised:
            EdgeTransportVerifier(expected_peer_id="synology-edge", expected_peer_auth_key=EDGE_KEY).verify(jcs_dumps(unsigned).encode("utf-8"), now_epoch_ms=1_001)
        self.assertEqual("EDGE_PAYLOAD_TOO_DEEP", raised.exception.code)

    def test_receiver_converts_json_recursion_failure_to_validation_error(self):
        from tools.tibia_re_control_center.model import ValidationError

        packet = (b'{"x":' * 2000) + b'0' + (b'}' * 2000)
        with self.assertRaises(ValidationError) as raised:
            EdgeTransportVerifier(expected_peer_id="synology-edge", expected_peer_auth_key=EDGE_KEY).verify(packet, now_epoch_ms=1_000)
        self.assertEqual("EDGE_FRAME_INVALID", raised.exception.code)

if __name__ == "__main__":
    unittest.main()
