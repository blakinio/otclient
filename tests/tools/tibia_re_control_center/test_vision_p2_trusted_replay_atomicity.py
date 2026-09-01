import tempfile
import unittest
from unittest.mock import patch

import tools.tibia_re_control_center.vision_p2_trusted_composition as composition_module
from tools.tibia_re_control_center.agent_edge_transport import EdgeFrameKind, EdgeTransportSigner
from tools.tibia_re_control_center.control_domain import ControlDomainService
from tools.tibia_re_control_center.vision_p2_trusted_composition import VisionP2TrustedComposition


_EDGE_KEY = b"edge-auth-key-for-tests-32-bytes!!"


class TrustedReplayAtomicityTests(unittest.TestCase):
    def test_durable_verifier_loads_and_saves_inside_one_store_transaction(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            service = ControlDomainService(raw)
            runtime = VisionP2TrustedComposition().attach(service)
            try:
                verifier = runtime.durable_edge_verifier(
                    session_id="session-atomic",
                    run_id="run-atomic",
                    expected_peer_id="edge-peer",
                    expected_peer_auth_key=_EDGE_KEY,
                    expected_connection_id="connection-atomic",
                )
                signer = EdgeTransportSigner(
                    local_peer_id="edge-peer",
                    local_auth_key=_EDGE_KEY,
                    session_id="session-atomic",
                    run_id="run-atomic",
                )
                packet = signer.seal(
                    kind=EdgeFrameKind.HEARTBEAT,
                    connection_id="connection-atomic",
                    connection_generation="generation-atomic",
                    sequence=1,
                    sent_epoch_ms=1_000,
                    payload={"edge_state": "ONLINE"},
                )
                original_load = composition_module._load_replay_ledger
                original_save = composition_module._save_replay_ledger
                observed_depths: list[tuple[str, int]] = []

                def load_with_depth(service_arg, key):
                    observed_depths.append(("load", service_arg.store._transaction_depth))
                    return original_load(service_arg, key)

                def save_with_depth(service_arg, key, ledger):
                    observed_depths.append(("save", service_arg.store._transaction_depth))
                    return original_save(service_arg, key, ledger)

                with (
                    patch.object(composition_module, "_load_replay_ledger", side_effect=load_with_depth),
                    patch.object(composition_module, "_save_replay_ledger", side_effect=save_with_depth),
                ):
                    verifier.verify(packet, now_epoch_ms=1_000)

                self.assertEqual([("load", 1), ("save", 1)], observed_depths)
            finally:
                service.store.close()


if __name__ == "__main__":
    unittest.main()
