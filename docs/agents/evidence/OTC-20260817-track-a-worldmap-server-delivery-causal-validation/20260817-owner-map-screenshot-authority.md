# Owner authority — post-IN_GAME map screenshot

Task: `OTC-20260817-track-a-worldmap-server-delivery-causal-validation`
PR: `#475`
Date: `2026-08-17`

The repository owner explicitly requested in the current conversation:

```text
dokoncz zadanie i potwierdz wejscia do swiata gry na mape sascreenem
```

This is treated as a narrowly scoped authority change for visual evidence only.

Authorized:

- one screenshot derived from the exact task-owned manifest X11 client window;
- capture only after independent structural world-entry proof (`FullMap` plus map-description strips) has already passed;
- map-view/cropped PNG only;
- transient source XWD is permitted solely to derive the PNG and must be deleted before cleanup;
- the screenshot may be persisted on the task branch as evidence so the owner can inspect it.

Still forbidden:

- screenshots of the login form, credentials, 2FA/device confirmation, character-selection/account screens, or any pre-IN_GAME state;
- OCR;
- credential/token/cookie/session capture;
- alternate/root X11 capture;
- changing the manifest-owned XID, VNC mapping, geometry, reparenting or recreating the window for screenshot purposes;
- raw executable upload.

The visual screenshot is corroborating evidence. Structural world-entry proof remains authoritative; a screenshot alone cannot produce `IN_GAME=PASS`.
