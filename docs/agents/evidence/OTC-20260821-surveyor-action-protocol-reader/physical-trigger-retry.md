# One-shot physical acceptance retry trigger

Task: `OTC-20260821-surveyor-action-protocol-reader`

Trusted base for this retry is current `main` containing final RW-bound repair merge `a28550bf5ad0880d947aa2ebc2de13f438cef6bd`.

This marker is non-executable and exists only to generate a fresh same-repository `pull_request` synchronize event for the trusted-main read-only physical acceptance workflow. It is not intended for merge.
