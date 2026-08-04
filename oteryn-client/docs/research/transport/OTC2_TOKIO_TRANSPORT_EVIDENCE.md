# OTC2 Tokio transport evidence

## Scope

This evidence compares the retained blocking transport baseline with the new bounded Tokio transport on the same deterministic Windows loopback workload. It measures application queue and scheduler behavior only. It does not measure or claim lower physical, Internet, Gateway or game-server round-trip time.

## Reproduction

- Source SHA: `e4a3b1d8c3ec602a29770031b394e34b2668a5fa`
- GitHub Actions run: `30928282581`
- Job: `92056161573` (`windows-evidence`)
- Runner: Windows Server 2025, x64
- Rust: `rustc 1.94.0 (4a4ef493e 2026-03-02)`
- Tokio: exact `1.51.4`
- Command: `cargo run -p oteryn-transport --example transport_evidence --features blocking-baseline --release`
- Frame size: 64 bytes
- Sequential latency samples: 200
- Pipelined burst: 1,000 frames
- Raw output: `OTC2_TOKIO_TRANSPORT_EVIDENCE_RAW.txt`

The same job passed canonical formatting, strict transport Clippy with all targets and `blocking-baseline`, and the complete transport test suite before recording the measurements.

## Results

| Measure | Blocking baseline | Tokio transport | Interpretation |
|---|---:|---:|---|
| Loopback queue latency p50 | 43 µs | 43 µs | Equal median in this single run |
| Loopback queue latency p95 | 54 µs | 58 µs | Tokio +4 µs |
| Loopback queue latency p99 | 65 µs | 82 µs | Tokio +17 µs |
| Pipelined burst throughput | 22,907.88 frames/s | 103,215.15 frames/s | Tokio 4.51× the blocking sequential baseline in this bounded loopback workload |
| Joined shutdown | 58 µs | 130 µs | Both bounded; Tokio includes supervisor and child-task joining |
| Queue high-water | not applicable | 978 frames | Observed across the pipelined burst and slow-consumer case |
| Queue-full rejections | not applicable | 0 | No silent loss or overflow in this workload |
| Slow-consumer cancellation | not applicable | 16,259 µs | Cancellation remained bounded while the inbound queue was saturated |

## Resource proxy

The run did not collect stable process CPU or allocator telemetry from the shared hosted runner. Queue capacities, queue high-water marks, explicit queue-full counts and bounded frame allocation are used as the reproducible resource/backpressure proxy:

- every directional queue has a configured finite capacity;
- inbound allocation occurs only after validating the complete frame length;
- the 1,000-frame burst reached a high-water mark of 978 without queue overflow;
- the saturated slow-consumer path still observed cancellation and joined within 16.259 ms.

## Conclusion

The evidence supports the implementation objective: Tokio enables bounded full-duplex pipelining and deterministic cancellation/shutdown without changing the physical network. Median loopback latency was unchanged, tail latency was slightly higher, and pipelined throughput was materially higher in this synthetic workload. These numbers are evidence for this exact CI host and commit only, not a production latency forecast.
