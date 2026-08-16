# Track A dedicated runner support-layout inventory — 2026-08-16

## Scope

Read-only physical infrastructure observation on `synology-otclient-01`. The job inspected only fixed support-tool paths and dpkg metadata. It did not inspect `/proc`, official-client files/processes, canonical registration/lease/session state, X11/VNC runtime state, game/network/login state or credentials.

## Exact execution

- workflow run: `31953830754`
- job: `95181286228`
- runner: `synology-otclient-01`
- selector: `[otclient, synology]`
- result: `SUCCESS`
- runtime access: `read_only`
- mutation authorized: `false`

## Proven current runner layout

### Historical home-work toolroot

`/home/runner/_work/_otclient_tibia_re_state/toolroot` is **ABSENT**.

### Persistent `/work` toolroot

`/work/_otclient_tibia_re_state/toolroot` exists and is a real directory. Under this root:

- `usr/bin/Xvfb`: exists, executable, contained below the root;
- `usr/bin/xdotool`: exists, executable, contained below the root;
- `usr/share/X11/xkb`: exists and is contained below the root;
- `usr/lib/x86_64-linux-gnu/libproxychains.so.4`: exists and is contained below the root;
- `lib/x86_64-linux-gnu/libproxychains.so.4`: resolves to the same contained library;
- `usr/bin/x11vnc`: **ABSENT**.

Therefore this root fails the trusted worker's all-components-in-one-root completeness gate **only because `x11vnc` is absent** among the observed required components.

### System paths/packages

Current container filesystem/package facts:

- `/usr/bin/x11vnc`: regular file, real path `/usr/bin/x11vnc`;
- package `x11vnc`: `install ok installed 0.9.16-10`;
- `/usr/bin/Xvfb`: absent; package `xvfb`: `NOT_INSTALLED`;
- `/usr/bin/xdotool`: absent; package `xdotool`: `NOT_INSTALLED`;
- `/usr/share/X11/xkb`: absent;
- system `libproxychains.so.4` paths inspected: absent; package `proxychains4`: `NOT_INSTALLED`.

## Root-cause classification

`PROVEN_SPLIT_SUPPORT_LAYOUT`

The current physical runner deliberately/effectively has the X11 support set split across two fixed trust domains:

```text
/work/_otclient_tibia_re_state/toolroot
  -> Xvfb
  -> xdotool
  -> XKB data
  -> libproxychains.so.4

/usr/bin/x11vnc
  -> x11vnc 0.9.16-10 (system package)
```

The trusted worker introduced by PR #379 correctly fails closed because it requires all support components below one root. The failure in RUNTIME #381 (`toolroot_unavailable`) is therefore explained without another bootstrap attempt.

## Static design correlation

PR #280's proposed dedicated-runner Dockerfile is not current deployment authority, but it independently shows an intended image design that installs `xvfb`, `xdotool` and `proxychains4` as system packages while omitting `x11vnc`. The live runner instead shows the inverse split for those particular system paths: `x11vnc` system-installed while the other support components live in `/work/.../toolroot`. This reinforces that the runtime worker must bind explicitly to the **observed fixed split layout** or the runner image must be redeployed to a unified layout; it must not reintroduce ambient `PATH` discovery.

## Safe next discriminator

A hosted-only worker repair may accept exactly:

1. the proven contained `/work/_otclient_tibia_re_state/toolroot` for Xvfb, xdotool, XKB and libproxychains; plus
2. the fixed literal `/usr/bin/x11vnc` system executable, validated as a regular non-symlink root-owned non-group/world-writable file and owned by the installed `x11vnc` Debian package.

No generic system-tool fallback, arbitrary environment override or additional support root is justified by this evidence.
