# OTC2 Tokio transport evidence

## Scope

This evidence compares the retained blocking transport baseline with the new bounded Tokio transport on the same deterministic Windows loopback workload. It measures application queue, scheduler and process CPU behavior only. It does not measure or claim lower physical, Internet, Gateway or game-server round-trip time.

## Reproduction

- Source SHA: `d9e536d75b3ed4aeb78e301549651d91f6868881`
- GitHub Actions run: `30929681775`
- Job: `windows-cpu-evidence`
- Runner: Windows, X64
- Rust: `rustc 1.94.0 (4a4ef493e 2026-03-02)`
- Cargo: `cargo 1.94.0 (85eff7c80 2026-01-15)`
- Tokio: exact `1.51.4`
- Frame size: 64 bytes
- Sequential latency samples per path: 200
- Pipelined burst per path: 1000 frames
- Raw output: `OTC2_TOKIO_TRANSPORT_EVIDENCE_RAW.txt`

The same job passed canonical formatting, strict transport Clippy with all targets and `blocking-baseline`, and the complete focused transport test suite before recording the measurements. Each release-mode path ran in its own process; `TotalProcessorTime` is the process user-plus-kernel CPU time reported by Windows for that path.

## Results

| Measure | Blocking baseline | Tokio transport | Interpretation |
|---|---:|---:|---|
| Loopback queue latency p50 | 40 µs | 42 µs | Exact result for this single hosted-runner sample |
| Loopback queue latency p95 | 74 µs | 70 µs | Exact result for this single hosted-runner sample |
| Loopback queue latency p99 | 91 µs | 99 µs | Exact result for this single hosted-runner sample |
| Pipelined burst throughput | 23003.74 frames/s | 87961.58 frames/s | Tokio 3.82× the blocking sequential baseline in this bounded workload |
| Process CPU time | 62.500 ms | 46.875 ms | Tokio/blocking CPU ratio 0.75× for separate complete harness processes |
| Joined shutdown | 52 µs | 121 µs | Tokio includes supervisor and child-task joining |
| Queue high-water | not applicable | 968 frames | Observed across burst and slow-consumer cases |
| Queue-full rejections | not applicable | 0 | No silent loss; overflow remains typed and counted |
| Slow-consumer cancellation | not applicable | 15788 µs | Cancellation remained bounded while the inbound queue was saturated |

## Allocation and backpressure proxy

Stable allocator-internal telemetry is not available from the shared hosted runner without adding platform-specific unsafe instrumentation. The reproducible allocation/backpressure proxy is therefore the configured finite capacities, validated frame-size-before-allocation rule, observed queue high-water mark and explicit queue-full counter:

- every directional queue has a configured finite capacity;
- inbound allocation occurs only after validating the complete frame length;
- burst and slow-consumer high-water are recorded without unbounded growth;
- saturation retains bounded cancellation and joined shutdown;
- queue overflow is a typed error and metric, never silent loss.

## Conclusion

The evidence supports the implementation objective: Tokio enables bounded full-duplex pipelining, typed backpressure and deterministic cancellation/shutdown without changing the physical network. These figures are evidence for this exact CI host, workload and commit only, not a production latency or CPU forecast.
