# Track A P2 intermediate vtable identity — coordinator promotion boundary

Source Draft PR: #305 (`research/OTC-20260815-track-a-p2-writer-vtable-group`)
Source exact final head: `9329e338235b7f9997d74d4db5313f329662378b`
Coordinator disposition: `ACCEPT_WITH_EDITS`
Final source task-specific run: `31884379539` / job `95011421555` — `SUCCESS`
Final source required PR CI: `31884381191` — `SUCCESS`
Exact client: official native Linux Tibia `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

## FACT promoted

`0x2f69e30` is a structurally valid normal Itanium-style address point with:

```text
offset-to-top = 0
typeinfo = 0x3080748
first targets = 0x7de7f0, 0x7dfd60
```

The reviewed setup evidence independently proves a separately allocated retained object receives vptr `0x2f69e30`.

Typeinfo `0x3080748` differs from canonical `TProtocolWriter` RTTI `0x3080728` and `TIODeviceWriter` RTTI `0x3080718`.

The accepted PR #301 relation therefore sharpens to:

```text
TProtocolClientMessageProcessor
 -> retained intermediate object
      vptr 0x2f69e30
      Itanium typeinfo 0x3080748
      semantic type name UNKNOWN
 -> retained shared TProtocolWriter
```

## DISPROVEN promoted

Table adjacency does not justify collapsing the `0x2f69e30` object into canonical `TProtocolWriter` as a simple secondary/base address point. Distinct typeinfo plus separate object allocation/provenance reject that interpretation.

## INFERENCE promoted with label

Functions `0x7de7f0` and `0x7dfd60` are teardown-like based on exact vptr-install/cleanup behavior. No semantic symbol name or writer-transform stage is assigned.

## UNKNOWN retained

- semantic type name for RTTI `0x3080748`;
- inheritance/base relation represented by RTTI `0x3080748`;
- first writer transformation/framing boundary;
- gameplay serialization/framing order;
- final binary QIODevice/socket egress;
- relationship of historical `0x3084c70 -> +0xd0 -> 0xb40630` family to the canonical writer branch.

Historical `0x3084c70` remains a separate lead; its reviewed artifact reports RTTI zero and no direct LEA provenance.

## Provenance boundary

`source-snapshot/` contains exact Git blobs from reviewed #305 final head: evidence report, machine result, reproducer and workflow. The workflow verifies the three historical reviewed artifact ZIP digests before parsing and fails closed on the exact client/source/table anchors.

This correction improves P2 type/provenance truth only. It does not prove any new transform order, final egress or P2 completion.
