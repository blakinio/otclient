from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from tools.tibia_re_control_center.control_api import ControlApiServer
from tools.tibia_re_control_center.control_cli import ControlApiClient


def find_browser() -> str:
    candidates = [
        shutil.which("google-chrome"), shutil.which("google-chrome-stable"),
        shutil.which("chromium"), shutil.which("chromium-browser"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    raise RuntimeError("real Chromium/Chrome browser binary was not found")


def cli(root: Path, *args: str) -> dict:
    command = [sys.executable, "-m", "tools.tibia_re_control_center.control_cli", "--data-dir", str(root), *args]
    completed = subprocess.run(command, check=False, capture_output=True, text=True, timeout=20)
    if completed.returncode != 0:
        raise RuntimeError("CLI command failed without exposing its captured output")
    return json.loads(completed.stdout.strip())


_CDP_PROBE = r'''
const port=process.argv[2], expectedEpoch=process.argv[3], clickExperiment=process.argv[4]==='1';
const sleep=(ms)=>new Promise(resolve=>setTimeout(resolve,ms));
const targets=await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
const target=targets.find(item=>item.type==='page');
if(!target) throw new Error('no browser page target');
const ws=new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject});
let nextId=1; const pending=new Map();
ws.onmessage=(event)=>{const message=JSON.parse(event.data);if(message.id&&pending.has(message.id)){const {resolve,reject}=pending.get(message.id);pending.delete(message.id);message.error?reject(new Error(message.error.message)):resolve(message.result)}};
function send(method,params={}){const id=nextId++;return new Promise((resolve,reject)=>{pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))})}
async function value(expression){const result=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});return result.result.value}
await send('Runtime.enable');
let epoch='';
for(let i=0;i<60;i++){epoch=await value("document.getElementById('backendEpoch')?.textContent||''");if(epoch.includes(expectedEpoch))break;await sleep(100)}
if(!epoch.includes(expectedEpoch)) throw new Error('browser did not render live backend epoch');
const statusText=await value("document.getElementById('statusJson')?.textContent||''");
const status=JSON.parse(statusText);
if(status.official_client_access!=='NONE') throw new Error('browser truthfulness boundary mismatch');
if(clickExperiment){
  await value("document.getElementById('runExperiment').click(); true");
  let resultText='';
  for(let i=0;i<100;i++){resultText=await value("document.getElementById('lastResult')?.textContent||''");if(resultText.includes('resource_id'))break;await sleep(100)}
  const result=JSON.parse(resultText);
  if(result.status!=='PASS'||result.adapter_kind!=='FAKE_TEST'||result.official_client_access!=='NONE') throw new Error('browser experiment did not complete through fake Package B path');
}
await send('Browser.close');
console.log('BROWSER_OK');
'''


def browser_probe(browser: str, root: Path, origin: str, backend_epoch: str, *, click_experiment: bool) -> None:
    profile = root / f"browser-profile-{backend_epoch}-{time.time_ns()}"
    profile.mkdir(parents=True, exist_ok=True)
    process = subprocess.Popen([
        browser, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
        "--disable-background-networking", "--disable-component-update", "--remote-debugging-port=0",
        "--remote-debugging-address=127.0.0.1", "--remote-allow-origins=*", f"--user-data-dir={profile}", origin + "/",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    active = profile / "DevToolsActivePort"
    deadline = time.monotonic() + 12
    while time.monotonic() < deadline and not active.exists():
        time.sleep(0.1)
    if not active.exists():
        process.terminate()
        raise RuntimeError("headless browser DevTools endpoint did not start")
    port = active.read_text(encoding="utf-8").splitlines()[0].strip()
    script = root / "browser-probe.mjs"
    script.write_text(_CDP_PROBE, encoding="utf-8")
    completed = subprocess.run(["node", str(script), port, backend_epoch, "1" if click_experiment else "0"], check=False, capture_output=True, text=True, timeout=25)
    if completed.returncode != 0 or "BROWSER_OK" not in completed.stdout:
        try:
            process.terminate()
        except OSError:
            pass
        raise RuntimeError("real browser CDP probe failed")
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.terminate()
        process.wait(timeout=5)
    time.sleep(0.5)


def main() -> int:
    browser = find_browser()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temporary:
        root = Path(temporary)
        first = ControlApiServer(root).start()
        try:
            status = cli(root, "status")
            if status["official_client_access"] != "NONE":
                raise RuntimeError("official-client boundary contradiction")
            browser_probe(browser, root, first.origin, first.domain.backend_epoch, click_experiment=True)
            if len(first.domain.adapter.physical_effects) != 1:
                raise RuntimeError("browser did not execute exactly one fake external effect")
            browser_probe(browser, root, first.origin, first.domain.backend_epoch, click_experiment=False)
            if len(first.domain.adapter.physical_effects) != 1:
                raise RuntimeError("browser reload/new-tab style read duplicated active work")
            scenario = ControlApiClient(root).get("/v1/scenarios")["items"][0]["scenario"]
            scenario_path = root / "scenario.json"
            scenario_path.write_text(json.dumps(scenario), encoding="utf-8")
            created = cli(root, "experiment", "--request-id", "e2e-package-b-cli-exp", "--scenario", str(scenario_path))
            replay = cli(root, "experiment", "--request-id", "e2e-package-b-cli-exp", "--scenario", str(scenario_path))
            if created != replay or len(first.domain.adapter.physical_effects) != 2:
                raise RuntimeError("CLI idempotency path duplicated or lost the fake external effect")
            stop = cli(root, "stop-all", "--request-id", "e2e-package-b-stop")
            reset = cli(root, "reset-stop", "--request-id", "e2e-package-b-reset")
            if not stop["stop_latched"] or reset["stop_latched"]:
                raise RuntimeError("STOP/reset E2E transition failed")
            resource_id = created["resource_id"]
        finally:
            if not first.close():
                raise RuntimeError("first backend did not complete graceful shutdown")
        second = ControlApiServer(root).start()
        try:
            replay_after_restart = cli(root, "experiment", "--request-id", "e2e-package-b-cli-exp", "--scenario", str(scenario_path))
            if replay_after_restart["resource_id"] != resource_id or second.domain.adapter.physical_effects:
                raise RuntimeError("restart replay did not preserve exactly-once logical resource semantics")
            browser_probe(browser, root, second.origin, second.domain.backend_epoch, click_experiment=False)
        finally:
            if not second.close():
                raise RuntimeError("second backend did not complete graceful shutdown")
    print("PACKAGE_B_BACKEND=PASS")
    print("PACKAGE_B_CLI=PASS")
    print("PACKAGE_B_BROWSER=PASS")
    print("PACKAGE_B_IDEMPOTENCY_RESTART=PASS")
    print("OFFICIAL_CLIENT_ACCESS=NONE")
    print("PACKAGE_B_E2E=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())