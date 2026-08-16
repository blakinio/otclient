#!/usr/bin/env python3
from __future__ import annotations
import argparse,importlib.util,json,os,stat,sys,tempfile,unittest
from pathlib import Path
from unittest import mock
SCRIPT=Path(__file__).with_name('tibia-official-client-re-canonical-live-transition.py')
WORKER=Path(__file__).with_name('tibia-official-client-re-canonical-live-session.sh')
def load():
 s=importlib.util.spec_from_file_location('transition_tested',SCRIPT);assert s and s.loader;m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m);return m
class Manager:
 generation=1
 def __init__(self,_):pass
 def _load_state_unlocked(self):return {'generation':self.generation}
 def _require_current_unlocked(self,s,i,t,n):
  if s['generation']!=self.generation or t!='token':raise RuntimeError('not current')
class Lease:
 LeaseManager=Manager
 @staticmethod
 def LeaseIdentity(t,s):return(t,s)
 @staticmethod
 def _read_private_token(_):return'token'
 @staticmethod
 def _now_epoch(_=None):return 100
class Guard: _supervisor_cancel_signal=None
class Popen:
 def __init__(self,command,**kwargs):self.pid=777;self.command=command;self.kwargs=kwargs
 def wait(self,timeout=None):return 0
class Tests(unittest.TestCase):
 def setUp(self):
  self.m=load();self.t=tempfile.TemporaryDirectory();r=Path(self.t.name);self.m.STATE=r;self.m.REG=r/'runtime-registration.json';self.a=argparse.Namespace(task_id='OTC-TEST',session_id='s',token_file=r/'tok',worker=WORKER,probe=WORKER,worker_timeout=2);self.i={'boot_id_sha256':'b'*64,'pid':4242,'process_start_ticks':123,'client_size':self.m.SIZE,'client_sha256':self.m.SHA};self.man={'pid':4242,'process_group_id':777,'display':':104','window_identity':'x11-window:9','remote_view_endpoint':'127.0.0.1:6091','remote_view_mapping':'PROVEN','state':'UNKNOWN'};self.g=Guard()
 def tearDown(self):self.t.cleanup()
 def reg(self,lg=1,rg=1):return {'schema_version':1,'runtime_id':self.m.RID,'registration_generation':rg,'lease_generation':lg,'registered_at':1,'boot_id_sha256':self.i['boot_id_sha256'],'pid':4242,'process_start_ticks':self.i['process_start_ticks'],'client_version':self.m.VER,'client_size':self.m.SIZE,'client_sha256':self.m.SHA,'display':self.man['display'],'window_identity':self.man['window_identity'],'remote_view_endpoint':self.man['remote_view_endpoint'],'remote_view_mapping':self.man['remote_view_mapping'],'state':self.man['state'],'source_task':'old','source_run':'old'}
 def write(self,d):self.m.STATE.mkdir(parents=True,exist_ok=True);self.m.REG.write_text(json.dumps(d));self.m.REG.chmod(0o600)
 def common(self):return mock.patch.object(self.m,'_ident',return_value=dict(self.i)),mock.patch.object(self.m,'_exact',return_value=None),mock.patch.object(self.m,'_lease',return_value=1)
 def test_bootstrap_stages_then_commits_and_uses_exact_worker_argv(self):
  seq=iter(([],[4242],[4242],[4242]));p1,p2,p3=self.common();calls=[]
  def fake_probe(w,p):calls.append(('probe',[str(w),'probe',str(p)]));return dict(self.man)
  with p1,p2,p3,mock.patch.object(self.m,'_candidates',side_effect=lambda:next(seq)),mock.patch.object(self.m.subprocess,'Popen',side_effect=lambda c,**k:(calls.append(('bootstrap',c)) or Popen(c,**k))),mock.patch.object(self.m,'_manifest',return_value=dict(self.man)),mock.patch.object(self.m,'_probe',side_effect=fake_probe):self.m._bootstrap(self.a,self.g,Lease,Manager(self.m.STATE),('t','s'),1)
  d=self.m._read();self.assertEqual(d['lease_generation'],1);self.assertEqual(stat.S_IMODE(self.m.REG.stat().st_mode),0o600);self.assertEqual(calls[0][1],[str(WORKER),'bootstrap',str(self.m.STATE/'.bootstrap-manifest.json')]);self.assertEqual(sum(x[0]=='probe' for x in calls),2)
 def test_bootstrap_failure_kills_group_rolls_worker_and_removes_registration(self):
  seq=iter(([],[4242]));p1,p2,p3=self.common();k=[];r=[]
  with p1,p2,p3,mock.patch.object(self.m,'_candidates',side_effect=lambda:next(seq)),mock.patch.object(self.m.subprocess,'Popen',Popen),mock.patch.object(self.m,'_manifest',return_value=dict(self.man)),mock.patch.object(self.m,'_probe',side_effect=self.m.E('post_probe_failed')),mock.patch.object(self.m,'_kill',side_effect=lambda x:k.append(x)),mock.patch.object(self.m,'_worker',side_effect=lambda w,o,a:r.append((o,a))):
   with self.assertRaises(self.m.E):self.m._bootstrap(self.a,self.g,Lease,Manager(self.m.STATE),('t','s'),1)
  self.assertEqual(k,[777]);self.assertEqual(r,[('rollback','777')]);self.assertFalse(self.m.REG.exists())
 def test_rebind_postwrite_probe_failure_restores_exact_previous(self):
  old=self.reg(lg=1,rg=4);self.write(old);Manager.generation=2;calls=0
  def pr(*args,**kw):
   nonlocal calls;calls+=1
   if calls==1:return old,dict(self.man)
   if calls==2:return old,dict(self.man)
   raise self.m.E('forced_final_probe_failure')
  try:
   with mock.patch.object(self.m,'_probe_reg',side_effect=pr),mock.patch.object(self.m,'_lease',return_value=2):
    with self.assertRaisesRegex(self.m.E,'forced_final_probe_failure'):self.m._rebind(self.a,self.g,Lease,Manager(self.m.STATE),('t','s'),2)
   self.assertEqual(self.m._read(),old)
  finally:Manager.generation=1
 def test_sanitized_environment_removes_credentials_capabilities_and_test_switch(self):
  with mock.patch.dict(os.environ,{'TIBIA_TEST_EMAIL':'mail','TIBIA_TEST_PASSWORD':'pw','TRACK_A_CANONICAL_LEASE_TOKEN':'x','SOME_CAPABILITY':'y','TRACK_A_CANONICAL_WORKER_CONTRACT_TEST':'1','SAFE':'ok'},clear=True):e=self.m._env()
  self.assertEqual(e,{'SAFE':'ok'})
 def test_real_worker_parser_accepts_transition_shape_and_rejects_extra_arg(self):
  out=Path(self.t.name)/'m.json';env=dict(os.environ,TRACK_A_CANONICAL_WORKER_CONTRACT_TEST='1')
  ok=self.m.subprocess.run([str(WORKER),'probe',str(out)],env=env,check=False);self.assertEqual(ok.returncode,0);self.assertTrue(out.exists())
  bad=self.m.subprocess.run([str(WORKER),'probe',str(out),'extra'],env=env,check=False);self.assertNotEqual(bad.returncode,0)
 def test_worker_has_no_login_or_historical_shared_wireproxy_dependency(self):
  s=WORKER.read_text();self.assertNotIn('login_e2e',s);self.assertNotIn('$BASE/runtime/wireproxy.pid',s);self.assertIn('OTCLIENT_TIBIA_RE_ROLE=wireproxy',s);self.assertIn('WGCF_VER=2.2.32',s);self.assertIn('WP_VER=1.1.3',s)
 def test_transition_reuses_cancellation_safe_supervisor_primitives(self):
  s=SCRIPT.read_text();self.assertIn('_install_supervisor_signal_handlers',s);self.assertIn('_become_child_subreaper',s);self.assertIn('signal.pthread_sigmask',s);self.assertIn('fcntl.flock',s)
if __name__=='__main__':unittest.main()
