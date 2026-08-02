#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("generate.py")
SPEC = importlib.util.spec_from_file_location("canary_protocol_index_generate", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load generator module")
generator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generator)


class GeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self._write_required_sources()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, relative: Path, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")

    def _write_required_sources(self) -> None:
        self.write(
            generator.CORE_HPP,
            'inline constexpr auto SERVER_RELEASE_VERSION = "3.6.1";\n'
            'inline constexpr uint16_t CLIENT_VERSION = 1525;\n',
        )
        self.write(
            generator.PROFILE_HPP,
            """
            enum class ProtocolProfileId : uint8_t {
                Current,
                Tibia1100,
            };
            enum class ProtocolFeature : uint64_t {
                None = 0,
                CurrentPayload = 1ULL << 0,
                MarketPackets = 1ULL << 1,
            };
            """,
        )
        self.write(
            generator.PROFILE_CPP,
            """
            constexpr ProtocolProfile currentProfile {
                .id = ProtocolProfileId::Current,
                .features = protocolFeatureMask(ProtocolFeature::CurrentPayload)
                    | protocolFeatureMask(ProtocolFeature::MarketPackets),
            };
            """,
        )
        self.write(
            generator.PORT_UTILS_HPP,
            "constexpr auto currentPort = ProtocolProfileId::Current;\n",
        )
        self.write(
            generator.SESSION_HINT_HPP,
            "struct ProtocolSessionHintStore {};\n",
        )
        self.write(
            generator.PROTOCOL_GAME_HPP,
            """
            class ProtocolGame {
                void parseAutoWalk(NetworkMessage &msg);
                void parseSay(NetworkMessage &msg);
                void parseDeclaredOnly(NetworkMessage &msg);
                void sendMapDescription();
                void sendMarketEnter();
                void sendDeclaredOnly();
            };
            """,
        )
        self.write(
            generator.PROTOCOL_GAME_CPP,
            """
            void ProtocolGame::parsePacketFromDispatcher(NetworkMessage &msg, uint8_t recvbyte) {
                switch (recvbyte) {
                    case 0x64:
                        parseAutoWalk(msg);
                        break;
                    case 0x96:
                        if (protocolProfile->hasFeature(ProtocolFeature::CurrentPayload)) {
                            parseSay(msg);
                        }
                        break;
                    case 0xF0:
                        g_game().playerMove(playerId, Direction::NORTH);
                        break;
                    case 0xF1:
                        break;
                }
            }

            void ProtocolGame::sendMapDescription() {
                NetworkMessage msg;
                msg.addByte(0x64);
                msg.addByte(7);
            }

            void ProtocolGame::sendMarketEnter() {
                NetworkMessage msg;
                if (protocolProfile->hasFeature(ProtocolFeature::MarketPackets)) {
                    msg.addByte(0xF6);
                }
            }

            void ProtocolGame::sendDeclaredOnly() {
                sendMapDescription();
            }
            """,
        )

    def test_build_model_extracts_literal_and_unresolved_evidence(self) -> None:
        model = generator.build_model(self.root, "abc123")
        self.assertEqual(model.server_release, "3.6.1")
        self.assertEqual(model.client_version, 1525)
        self.assertEqual(model.enabled_features, ("CurrentPayload", "MarketPackets"))

        inbound = [entry for entry in model.entries if entry.direction == "client-to-server"]
        outbound = [entry for entry in model.entries if entry.direction == "server-to-client"]
        self.assertEqual([entry.opcode for entry in inbound], [0x64, 0x96, 0xF0, 0xF1])
        self.assertEqual(inbound[0].method, "parseAutoWalk")
        self.assertEqual(inbound[0].family, "movement")
        self.assertEqual(inbound[1].profile_gates, ("CurrentPayload",))
        self.assertEqual(inbound[2].extraction, "inline-dispatch")
        self.assertEqual(inbound[3].extraction, "unresolved")

        by_method = {entry.method: entry for entry in outbound}
        self.assertEqual(by_method["sendMapDescription"].opcode, 0x64)
        self.assertEqual(by_method["sendMarketEnter"].opcode, 0xF6)
        self.assertEqual(by_method["sendMarketEnter"].profile_gates, ("MarketPackets",))
        self.assertIsNone(by_method["sendDeclaredOnly"].opcode)
        self.assertIn("parseDeclaredOnly", model.unresolved_declarations)

    def test_outputs_are_byte_identical_and_machine_readable(self) -> None:
        model = generator.build_model(self.root, "abc123")
        first = self.root / "first"
        second = self.root / "second"
        generator.write_outputs(
            model,
            first / "protocol.md",
            first / "fixtures.md",
            first / "index.json",
        )
        generator.write_outputs(
            model,
            second / "protocol.md",
            second / "fixtures.md",
            second / "index.json",
        )
        for name in ("protocol.md", "fixtures.md", "index.json"):
            self.assertEqual((first / name).read_bytes(), (second / name).read_bytes())
        payload = json.loads((first / "index.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["schema"], "oteryn-canary-source-index-v1")
        self.assertEqual(payload["producer"]["revision"], "abc123")
        self.assertNotIn("playerMove(playerId", (first / "protocol.md").read_text(encoding="utf-8"))

    def test_missing_source_and_missing_dispatch_fail_closed(self) -> None:
        (self.root / generator.SESSION_HINT_HPP).unlink()
        with self.assertRaises(generator.GenerationError):
            generator.build_model(self.root, "abc123")

        self.write(generator.SESSION_HINT_HPP, "struct ProtocolSessionHintStore {};\n")
        self.write(generator.PROTOCOL_GAME_CPP, "void unrelated() {}\n")
        with self.assertRaises(generator.GenerationError):
            generator.build_model(self.root, "abc123")


if __name__ == "__main__":
    unittest.main()
