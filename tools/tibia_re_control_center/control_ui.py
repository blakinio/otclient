from __future__ import annotations

import html
import json

TABS = (
    "Main", "Agent", "Runtime", "Movement", "Healing", "Spells", "Consumables",
    "Combat", "Targeting", "Inventory", "Containers", "Equipment", "Chat",
    "Conditions", "Scenarios", "Recorder", "Network", "Experiments", "Compare", "Logger",
)


_TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TIBIA RE Control Center — Package B</title>
<style nonce="__CSP_NONCE__">
:root{font-family:system-ui,sans-serif;color-scheme:dark;background:#111;color:#eee}
body{margin:0;display:grid;grid-template-rows:auto auto 1fr;min-height:100vh}
header{padding:12px 16px;background:#1b1b1b;display:flex;gap:12px;align-items:center;position:sticky;top:0}
header strong{flex:1}.danger{font-weight:800;border:2px solid currentColor;padding:9px 18px}.muted{opacity:.75}
nav{display:flex;gap:6px;overflow:auto;padding:8px;background:#171717}nav button{white-space:nowrap}
button,input,textarea{font:inherit;padding:7px 10px}textarea{min-width:280px;min-height:70px}main{padding:16px;max-width:1400px;width:100%;box-sizing:border-box;margin:auto}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:10px}.card{border:1px solid #444;padding:12px;border-radius:8px;background:#181818}
.card h3{margin-top:0}.state{font-family:ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#0d0d0d;padding:10px;border-radius:6px;max-height:420px;overflow:auto}
section[data-tab]{display:none}section[data-tab].active{display:block}.toolbar{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}.warn{border-left:4px solid currentColor;padding-left:10px}
</style>
</head>
<body>
<header><strong>TIBIA RE Control Center / E2E Lab — Package B</strong><span id="backendEpoch" class="muted">backend: UNKNOWN</span><button id="resetStop">RESET STOP</button><button id="stopAll" class="danger">STOP ALL</button></header>
<nav id="tabs">__TAB_BUTTONS__</nav>
<main>
<section data-tab="Main" class="active">
<p class="warn">Package B is FAKE_TEST-only. Official Tibia access: <strong>NONE</strong>. Official mutation authority: <strong>UNSUPPORTED</strong>.</p>
<div class="grid">
<div class="card"><h3>Runtime</h3><div id="runtime" class="state">UNKNOWN</div></div>
<div class="card"><h3>Authority</h3><div id="authority" class="state">UNKNOWN</div></div>
<div class="card"><h3>Capability</h3><div id="capability" class="state">UNKNOWN</div></div>
<div class="card"><h3>Evidence</h3><div id="evidence" class="state">NOT_PROVEN</div></div>
<div class="card"><h3>Freshness</h3><div id="freshness" class="state">UNKNOWN</div></div>
<div class="card"><h3>Session</h3><div id="session" class="state">UNKNOWN</div></div>
</div>
<div class="toolbar"><button id="refresh">Refresh read views</button><button id="runExperiment">Run fake one-step experiment</button></div>
<pre id="lastResult">No mutating request has been sent.</pre>
</section>
<section data-tab="Agent">
<h2>Local vision agent</h2>
<p class="warn">Secret-safe local views only. Runtime access is session-scoped and may be read-only when separately admitted. Mutation authority: <strong>NONE</strong>.</p>
<div class="toolbar"><input id="agentSessionId" placeholder="session id"><input id="agentRunId" placeholder="run id"><button id="loadAgent">Load safe agent views</button></div>
<div class="grid">
<div class="card"><h3>Session heartbeat</h3><div id="agentHeartbeat" class="state">UNKNOWN</div></div>
<div class="card"><h3>Task / run / main SHA</h3><div id="agentTaskRun" class="state">UNKNOWN</div></div>
<div class="card"><h3>Secret-safe capture</h3><div id="agentCapture" class="state">UNAVAILABLE</div></div>
<div class="card"><h3>Visual-only label / OCR</h3><div id="agentVisual" class="state">UNKNOWN</div></div>
<div class="card"><h3>Runtime evidence class</h3><div id="agentRuntimeEvidence" class="state">UNKNOWN</div></div>
<div class="card"><h3>Reconciliation state</h3><div id="agentReconciliation" class="state">UNKNOWN</div></div>
<div class="card"><h3>Action status / budget</h3><div id="agentActionBudget" class="state">UNKNOWN</div></div>
</div>
<h3>Owner controls</h3>
<div class="toolbar"><button id="agentPause">PAUSE</button><button id="agentStop" class="danger">STOP</button><button id="agentResume">RESUME</button><button id="agentScreenshot">SCREENSHOT</button></div>
<h3>Owner chat</h3>
<div class="toolbar"><textarea id="agentChatText" placeholder="owner message"></textarea><button id="agentChat">Send owner message</button></div>
<h3>Submit TaskEnvelope.v1</h3>
<div class="toolbar"><input id="agentTaskFile" type="file" accept="application/json"><button id="agentSubmitTask">Submit task file</button></div>
<h3>Provenance timeline</h3><pre id="agentTimeline">UNKNOWN</pre>
<h3>Agent result</h3><pre id="agentResult">UNKNOWN</pre>
</section>
<section data-tab="Runtime"><h2>Runtime / backend / control</h2><pre id="statusJson">UNKNOWN</pre></section>
<section data-tab="Scenarios"><h2>Scenarios</h2><button id="refreshScenarios">Refresh</button><pre id="scenariosJson">UNKNOWN</pre></section>
<section data-tab="Experiments"><h2>Experiments and runs</h2><button id="refreshRuns">Refresh runs</button><div class="toolbar"><input id="runId" placeholder="run id"><button id="inspectRun">Inspect run + artifacts</button></div><pre id="runsJson">UNKNOWN</pre><pre id="runJson">UNKNOWN</pre></section>
<section data-tab="Logger"><h2>Events / logger</h2><button id="refreshEvents">Refresh bounded polling</button><pre id="eventsJson">UNKNOWN</pre></section>
<section data-tab="Recorder"><h2>Recorder</h2><p>Package B view only. Runtime recorder integration: <strong>NOT_PROVEN</strong>.</p></section>
<section data-tab="Network"><h2>Network</h2><p>Official-client network evidence in Package B: <strong>UNSUPPORTED</strong>.</p></section>
<section data-tab="Compare"><h2>Compare</h2><p>Comparison UI integration in this package: <strong>UNSUPPORTED</strong>.</p></section>
__GENERIC_SECTIONS__
</main>
<script nonce="__CSP_NONCE__">
const CONTROL_NONCE=__CONTROL_NONCE_JSON__;
const json=(v)=>JSON.stringify(v,null,2);
const requestId=(prefix)=>`${prefix}-${crypto.randomUUID()}`;
async function api(path,{method='GET',body=null,requestIdValue=null}={}){
  const headers={'X-Tibia-RE-Control-Nonce':CONTROL_NONCE};
  if(body!==null){headers['Content-Type']='application/json'}
  if(requestIdValue){headers['X-Tibia-RE-Request-Id']=requestIdValue}
  const response=await fetch(path,{method,headers,body:body===null?null:JSON.stringify(body),credentials:'omit',cache:'no-store'});
  let payload;try{payload=await response.json()}catch{payload={code:'CONTROL_INVALID_RESPONSE',safe_message:'backend returned a non-JSON response'}}
  if(!response.ok){throw Object.assign(new Error(payload.safe_message||'request failed'),{payload,status:response.status})}
  return payload;
}
function showError(error){document.getElementById('lastResult').textContent=json(error.payload||{code:'CONTROL_UI_ERROR',safe_message:'request failed'});}
async function refresh(){
  try{
    const [status,caps]=await Promise.all([api('/v1/status'),api('/v1/capabilities')]);
    document.getElementById('backendEpoch').textContent=`backend: ${status.backend.epoch}`;
    for(const key of ['runtime','authority','capability','evidence','freshness','session'])document.getElementById(key).textContent=json(status[key]);
    document.getElementById('statusJson').textContent=json(status);
    document.getElementById('capability').textContent=json({summary:status.capability,items:caps.items});
  }catch(error){showError(error)}
}
async function scenarios(){try{const value=await api('/v1/scenarios');document.getElementById('scenariosJson').textContent=json(value);return value}catch(error){showError(error)}}
async function runs(){try{document.getElementById('runsJson').textContent=json(await api('/v1/runs?limit=100'))}catch(error){showError(error)}}
async function events(){try{document.getElementById('eventsJson').textContent=json(await api('/v1/events?limit=100'))}catch(error){showError(error)}}
function agentSessionId(){return document.getElementById('agentSessionId').value.trim()}
function agentRunId(){return document.getElementById('agentRunId').value.trim()}
function applyAgentSession(session){
  const dashboard=session.dashboard||{};
  const edge=session.edge||{availability:'DISCONNECTED',current:false,reason:'NO_EDGE_OBSERVATION',admission:{bound:false,current:false,reason:'RUNTIME_ADMISSION_REQUIRED'},capture:null,runtime:null};
  document.getElementById('agentHeartbeat').textContent=json({state:session.operational_state,heartbeat_epoch_ms:session.heartbeat_epoch_ms,edge:{availability:edge.availability,current:edge.current,reason:edge.reason,edge_instance_id:edge.edge_instance_id,admission:edge.admission||{bound:false,current:false,reason:'RUNTIME_ADMISSION_REQUIRED'}},pause_latched:session.pause_latched,stop_latched:session.stop_latched});
  document.getElementById('agentTaskRun').textContent=json({task_id:session.task_id,run_id:session.current_run_id,trusted_main_sha:session.trusted_main_sha,runtime_access:session.runtime_access,official_client_access:session.official_client_access});
  document.getElementById('agentCapture').textContent=json(edge.capture||dashboard.latest_secret_safe_capture||{status:'UNAVAILABLE',secret_safe:true,current:false});
  document.getElementById('agentVisual').textContent=json(dashboard.visual||{label:'UNKNOWN',ocr:[],visual_only:true,structural_authority:false});
  document.getElementById('agentRuntimeEvidence').textContent=json(edge.runtime||dashboard.runtime_evidence_class||'UNKNOWN');
  document.getElementById('agentReconciliation').textContent=json(dashboard.reconciliation_state||'UNKNOWN');
  document.getElementById('agentActionBudget').textContent=json({latest_action:dashboard.latest_action||null,physical_action_budget:session.physical_action_budget,physical_action_count:session.physical_action_count,remaining_physical_action_budget:session.remaining_physical_action_budget,mutation_authority:session.mutation_authority});
  document.getElementById('agentTimeline').textContent=json(dashboard.provenance_timeline||session.events||[]);
  if(session.current_run_id&&!agentRunId())document.getElementById('agentRunId').value=session.current_run_id;
}
async function loadAgent(){
  try{
    const sessionId=agentSessionId();
    const session=await api(`/v1/agent/session?session_id=${encodeURIComponent(sessionId)}`);
    applyAgentSession(session);
    const timeline=await api(`/v1/agent/events?session_id=${encodeURIComponent(sessionId)}&cursor=0&limit=100`);
    document.getElementById('agentTimeline').textContent=json(timeline.items);
    const runId=agentRunId();
    if(runId)document.getElementById('agentResult').textContent=json(await api(`/v1/agent/result?run_id=${encodeURIComponent(runId)}`));
  }catch(error){showError(error)}
}
async function agentControl(command){
  try{
    const value=await api('/v1/agent/control',{method:'POST',body:{session_id:agentSessionId(),command},requestIdValue:requestId(`ui-agent-${command.toLowerCase()}`)});
    applyAgentSession(value.session);document.getElementById('agentResult').textContent=json(value);
  }catch(error){showError(error)}
}
document.getElementById('tabs').addEventListener('click',(event)=>{if(event.target.tagName!=='BUTTON')return;const name=event.target.dataset.tab;document.querySelectorAll('section[data-tab]').forEach((section)=>section.classList.toggle('active',section.dataset.tab===name));});
document.getElementById('refresh').onclick=refresh;document.getElementById('refreshScenarios').onclick=scenarios;document.getElementById('refreshRuns').onclick=runs;document.getElementById('refreshEvents').onclick=events;
document.getElementById('stopAll').onclick=async()=>{try{document.getElementById('lastResult').textContent=json(await api('/v1/stop-all',{method:'POST',body:{},requestIdValue:requestId('ui-stop')}));await refresh()}catch(error){showError(error)}};
document.getElementById('resetStop').onclick=async()=>{try{document.getElementById('lastResult').textContent=json(await api('/v1/reset-stop',{method:'POST',body:{},requestIdValue:requestId('ui-reset')}));await refresh()}catch(error){showError(error)}};
document.getElementById('runExperiment').onclick=async()=>{try{const list=await scenarios();const scenario=list.items[0].scenario;const value=await api('/v1/experiments/one-step',{method:'POST',body:{scenario},requestIdValue:requestId('ui-exp')});document.getElementById('lastResult').textContent=json(value);await Promise.all([refresh(),runs(),events()])}catch(error){showError(error)}};
document.getElementById('inspectRun').onclick=async()=>{try{const id=document.getElementById('runId').value.trim();document.getElementById('runJson').textContent=json(await api(`/v1/runs/${encodeURIComponent(id)}`))}catch(error){showError(error)}};
document.getElementById('loadAgent').onclick=loadAgent;
document.getElementById('agentPause').onclick=()=>agentControl('PAUSE');document.getElementById('agentStop').onclick=()=>agentControl('STOP');document.getElementById('agentResume').onclick=()=>agentControl('RESUME');document.getElementById('agentScreenshot').onclick=()=>agentControl('SCREENSHOT');
document.getElementById('agentChat').onclick=async()=>{try{const text=document.getElementById('agentChatText').value;const value=await api('/v1/agent/chat',{method:'POST',body:{session_id:agentSessionId(),text},requestIdValue:requestId('ui-agent-chat')});document.getElementById('agentChatText').value='';applyAgentSession(value.session);document.getElementById('agentResult').textContent=json(value)}catch(error){showError(error)}};
document.getElementById('agentSubmitTask').onclick=async()=>{try{const file=document.getElementById('agentTaskFile').files[0];if(!file)throw new Error('task file required');const body=JSON.parse(await file.text());const value=await api('/v1/agent/tasks',{method:'POST',body,requestIdValue:requestId('ui-agent-task')});document.getElementById('agentSessionId').value=value.session.session_id;document.getElementById('agentRunId').value=value.session.current_run_id||'';applyAgentSession(value.session);document.getElementById('agentResult').textContent=json(value)}catch(error){showError(error)}};
window.addEventListener('load',()=>Promise.all([refresh(),scenarios(),runs(),events()]));
</script>
</body>
</html>'''


def render_control_ui(control_nonce: str, csp_nonce: str) -> str:
    buttons = "".join(f'<button data-tab="{html.escape(tab)}">{html.escape(tab)}</button>' for tab in TABS)
    custom = {"Main", "Agent", "Runtime", "Scenarios", "Experiments", "Logger", "Recorder", "Network", "Compare"}
    generic = "".join(
        f'<section data-tab="{html.escape(tab)}"><h2>{html.escape(tab)}</h2><p>Package B semantic view: <strong>UNSUPPORTED</strong> until an admitted provider supplies this domain.</p></section>'
        for tab in TABS if tab not in custom
    )
    return (
        _TEMPLATE.replace("__CSP_NONCE__", html.escape(csp_nonce, quote=True))
        .replace("__TAB_BUTTONS__", buttons)
        .replace("__GENERIC_SECTIONS__", generic)
        .replace("__CONTROL_NONCE_JSON__", json.dumps(control_nonce))
    )
