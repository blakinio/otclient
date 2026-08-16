#!/usr/bin/env python3
"""Cancellation-safe Track A canonical bootstrap, rebind and Gate B."""
from __future__ import annotations
import argparse,fcntl,hashlib,importlib.util,json,os,signal,subprocess,sys,tempfile,time
from pathlib import Path
from typing import Any,Sequence

STATE=Path('/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime')
REG=STATE/'runtime-registration.json'
GUARD_PATH=Path(__file__).with_name('tibia-official-client-re-canonical-live-guard.py')
RID='track-a-canonical-live'; VER='15.32.df7b29'; SIZE=51965216
SHA='e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe'
STATES={'LOGIN','CHARACTER_SELECT','IN_GAME','DISCONNECTED','UNKNOWN'}
FIELDS={'schema_version','runtime_id','registration_generation','lease_generation','registered_at','boot_id_sha256','pid','process_start_ticks','client_version','client_size','client_sha256','display','window_identity','remote_view_endpoint','remote_view_mapping','state','source_task','source_run'}

class E(RuntimeError):
 def __init__(self,code:str,msg:str=''): super().__init__(msg or code); self.code=code

def _guard():
 s=importlib.util.spec_from_file_location('track_a_bootstrap_guard',GUARD_PATH)
 if not s or not s.loader: raise E('guard_unavailable')
 m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m); return m

def _sha(p:Path)->str:
 h=hashlib.sha256()
 with p.open('rb',buffering=0) as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()

def _boot()->str: return hashlib.sha256(Path('/proc/sys/kernel/random/boot_id').read_text().strip().encode()).hexdigest()
def _start(pid:int)->int:
 s=Path(f'/proc/{pid}/stat').read_text(); i=s.rfind(')'); f=s[i+2:].split()
 if i<0 or len(f)<20: raise E('proc_stat_invalid')
 return int(f[19])
def _exe(pid:int)->Path:
 try:return Path(os.readlink(f'/proc/{pid}/exe'))
 except OSError as x:raise E('client_exe_unreadable',str(x)) from x
def _ident(pid:int)->dict[str,Any]:
 p=_exe(pid); st=p.stat(); return {'boot_id_sha256':_boot(),'pid':pid,'process_start_ticks':_start(pid),'client_size':st.st_size,'client_sha256':_sha(p)}
def _exact(i:dict[str,Any])->None:
 if i['client_size']!=SIZE: raise E('client_size_mismatch')
 if i['client_sha256']!=SHA: raise E('client_sha256_mismatch')

def _candidates()->list[int]:
 out=[]
 for e in Path('/proc').iterdir():
  if not e.name.isdigit(): continue
  pid=int(e.name)
  try:p=_exe(pid); st=p.stat()
  except (OSError,E):continue
  plausible='CipSoft GmbH/Tibia/packages/Tibia' in str(p)
  if not plausible and st.st_size!=SIZE: continue
  try:s=_sha(p)
  except OSError:
   if plausible: out.append(pid)
   continue
  if plausible or (st.st_size==SIZE and s==SHA):out.append(pid)
 return sorted(set(out))

def _read()->dict[str,Any]|None:
 if not REG.exists():return None
 st=REG.lstat(); owner=not hasattr(os,'getuid') or st.st_uid==os.getuid()
 if not REG.is_file() or REG.is_symlink() or (st.st_mode&0o777)!=0o600 or not owner:raise E('registration_file_unsafe')
 try:d=json.loads(REG.read_text())
 except (OSError,json.JSONDecodeError) as x:raise E('registration_invalid_json',str(x)) from x
 if not isinstance(d,dict) or not FIELDS.issubset(d) or d.get('schema_version')!=1 or d.get('runtime_id')!=RID:raise E('registration_schema_invalid')
 if (d.get('client_version'),d.get('client_size'),d.get('client_sha256'))!=(VER,SIZE,SHA):raise E('registration_client_fence_invalid')
 if d.get('state') not in STATES or d.get('remote_view_mapping') not in {'PROVEN','UNKNOWN'}:raise E('registration_state_invalid')
 if not isinstance(d.get('registration_generation'),int) or d['registration_generation']<1:raise E('registration_generation_invalid')
 if not isinstance(d.get('lease_generation'),int) or d['lease_generation']<1:raise E('registration_lease_generation_invalid')
 return d

def _stage(d:dict[str,Any])->Path:
 STATE.mkdir(parents=True,exist_ok=True,mode=0o700); fd,n=tempfile.mkstemp(prefix='.runtime-registration.',dir=STATE); p=Path(n)
 try:
  os.fchmod(fd,0o600)
  with os.fdopen(fd,'wb') as f:f.write((json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode());f.flush();os.fsync(f.fileno())
  return p
 except BaseException:
  try:os.close(fd)
  except OSError:pass
  p.unlink(missing_ok=True);raise

def _commit(p:Path)->None:
 os.replace(p,REG); fd=os.open(STATE,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
def _write(d:dict[str,Any])->None:
 p=_stage(d)
 try:_commit(p)
 finally:p.unlink(missing_ok=True)
def _remove(expected:dict[str,Any])->None:
 if _read()!=expected:raise E('registration_cleanup_mismatch')
 REG.unlink(); fd=os.open(STATE,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
 if REG.exists():raise E('registration_cleanup_failed')

def _manifest(p:Path)->dict[str,Any]:
 try:d=json.loads(p.read_text())
 except (OSError,json.JSONDecodeError) as x:raise E('probe_manifest_invalid',str(x)) from x
 need={'pid','display','window_identity','remote_view_endpoint','remote_view_mapping','state'}
 if not isinstance(d,dict) or not need.issubset(d):raise E('probe_manifest_missing_fields')
 if not isinstance(d['pid'],int) or d['pid']<2:raise E('probe_pid_invalid')
 if not isinstance(d['display'],str) or not d['display'].startswith(':'):raise E('probe_display_invalid')
 if not isinstance(d['window_identity'],str) or not d['window_identity']:raise E('probe_window_invalid')
 if d['remote_view_mapping'] not in {'PROVEN','UNKNOWN'} or d['state'] not in STATES:raise E('probe_state_invalid')
 return d

def _match(m:dict[str,Any],r:dict[str,Any])->None:
 for k in ('pid','display','window_identity','remote_view_endpoint','remote_view_mapping','state'):
  if m.get(k)!=r.get(k):raise E(f'probe_registration_{k}_mismatch')
 i=_ident(int(r['pid']));_exact(i)
 for k in ('boot_id_sha256','pid','process_start_ticks'):
  if i[k]!=r.get(k):raise E(f'registered_identity_{k}_mismatch')

def _env()->dict[str,str]:
 e=dict(os.environ)
 for k in list(e):
  u=k.upper()
  if 'CAPABILITY' in u or 'LEASE_TOKEN' in u or u.startswith('TIBIA_TEST_') or k=='TRACK_A_CANONICAL_WORKER_CONTRACT_TEST':e.pop(k,None)
 return e

def _worker(w:Path,op:str,arg:str)->None:
 r=subprocess.run([str(w),op,arg],env=_env(),close_fds=True,check=False)
 if r.returncode:raise E(f'{op}_worker_failed')
def _probe(w:Path,p:Path)->dict[str,Any]:
 p.unlink(missing_ok=True);_worker(w,'probe',str(p));return _manifest(p)
def _kill(pgid:int)->None:
 try:os.killpg(pgid,signal.SIGTERM)
 except ProcessLookupError:return
 end=time.monotonic()+4
 while time.monotonic()<end:
  try:os.killpg(pgid,0)
  except ProcessLookupError:return
  try:
   while os.waitpid(-1,os.WNOHANG)[0]>0:pass
  except ChildProcessError:pass
  time.sleep(.1)
 try:os.killpg(pgid,signal.SIGKILL)
 except ProcessLookupError:pass

def _lease(manager:Any,lease:Any,ident:Any,token:Path,gen:int|None=None)->int:
 t=lease._read_private_token(token);s=manager._load_state_unlocked();manager._require_current_unlocked(s,ident,t,lease._now_epoch(None))
 if s is None:raise E('lease_absent')
 g=int(s['generation'])
 if gen is not None and g!=gen:raise E('lease_generation_changed')
 return g
def _cancel(g:Any)->None:
 if g._supervisor_cancel_signal is not None:raise E('supervisor_cancelled')
def _runid()->str:return os.environ.get('GITHUB_RUN_ID') or 'manual-unknown'

def _probe_reg(a:argparse.Namespace,g:Any,lease:Any,manager:Any,ident:Any,gen:int,old:bool)->tuple[dict[str,Any],dict[str,Any]]:
 r=_read()
 if r is None:raise E('registration_absent')
 rg=int(r['lease_generation'])
 if old and rg>=gen:raise E('rebind_generation_not_older')
 if not old and rg!=gen:raise E('registration_generation_mismatch')
 p=STATE/'.gate-b-manifest.json'
 try:
  m=_probe(a.probe,p);_match(m,r)
  if _candidates()!=[int(r['pid'])]:raise E('registered_target_not_unique')
  _lease(manager,lease,ident,a.token_file,gen);_cancel(g);return r,m
 finally:p.unlink(missing_ok=True)

def _bootstrap(a:argparse.Namespace,g:Any,lease:Any,manager:Any,ident:Any,gen:int)->None:
 if _read() is not None:raise E('registration_already_present')
 if _candidates():raise E('official_client_candidate_present')
 man=STATE/'.bootstrap-manifest.json'; post=STATE/'.bootstrap-post-manifest.json'; stage=None; child=None; committed=None; ok=False
 try:
  STATE.mkdir(parents=True,exist_ok=True,mode=0o700);man.unlink(missing_ok=True);post.unlink(missing_ok=True)
  child=subprocess.Popen([str(a.worker),'bootstrap',str(man)],env=_env(),close_fds=True,start_new_session=True)
  if child.wait(timeout=a.worker_timeout):raise E('bootstrap_worker_failed')
  _cancel(g);m=_manifest(man)
  if m.get('process_group_id')!=child.pid:raise E('bootstrap_process_group_invalid')
  i=_ident(int(m['pid']));_exact(i)
  if _candidates()!=[int(m['pid'])]:raise E('bootstrap_target_not_unique')
  _lease(manager,lease,ident,a.token_file,gen)
  r={'schema_version':1,'runtime_id':RID,'registration_generation':1,'lease_generation':gen,'registered_at':int(time.time()),'boot_id_sha256':i['boot_id_sha256'],'pid':i['pid'],'process_start_ticks':i['process_start_ticks'],'client_version':VER,'client_size':SIZE,'client_sha256':SHA,'display':m['display'],'window_identity':m['window_identity'],'remote_view_endpoint':m['remote_view_endpoint'],'remote_view_mapping':m['remote_view_mapping'],'state':m['state'],'source_task':a.task_id,'source_run':_runid()}
  stage=_stage(r);p=_probe(a.worker,post);_match(p,r)
  if _candidates()!=[int(r['pid'])]:raise E('bootstrap_uniqueness_changed_before_commit')
  _lease(manager,lease,ident,a.token_file,gen);_cancel(g)
  try:_commit(stage)
  except BaseException:
   try:
    cur=_read(); committed=r if cur==r else None
    if cur is not None and cur!=r:raise E('registration_commit_conflict')
   finally:
    if not stage.exists():stage=None
   raise
  else:stage=None;committed=r
  if _read()!=r:raise E('registration_revalidation_failed')
  p=_probe(a.worker,post);_match(p,r)
  if _candidates()!=[int(r['pid'])]:raise E('bootstrap_uniqueness_changed_before_detach')
  _lease(manager,lease,ident,a.token_file,gen);_cancel(g);ok=True
 finally:
  man.unlink(missing_ok=True);post.unlink(missing_ok=True)
  if stage:stage.unlink(missing_ok=True)
  if not ok and child is not None:
   _kill(child.pid)
   try:_worker(a.worker,'rollback',str(child.pid))
   except BaseException as x:
    if committed:_remove(committed)
    raise E('bootstrap_rollback_failed',str(x))
  if not ok and committed:_remove(committed)

def _rebind(a:argparse.Namespace,g:Any,lease:Any,manager:Any,ident:Any,gen:int)->None:
 old,m=_probe_reg(a,g,lease,manager,ident,gen,True);new=dict(old);new.update(registration_generation=int(old['registration_generation'])+1,lease_generation=gen,source_task=a.task_id,source_run=_runid())
 for k in ('display','window_identity','remote_view_endpoint','remote_view_mapping','state'):new[k]=m[k]
 stage=_stage(new);committed=False
 try:
  _probe_reg(a,g,lease,manager,ident,gen,True);_lease(manager,lease,ident,a.token_file,gen);_cancel(g)
  committed=True
  _commit(stage)
  if _read()!=new:raise E('rebind_revalidation_failed')
  final,_=_probe_reg(a,g,lease,manager,ident,gen,False)
  if final!=new:raise E('rebind_final_registration_changed')
 except BaseException as x:
  if committed:
   try:_write(old)
   except BaseException as y:raise E('rebind_rollback_failed',str(y)) from x
   if _read()!=old:raise E('rebind_rollback_revalidation_failed') from x
  raise
 finally:
  if not committed:stage.unlink(missing_ok=True)

def _gateb(a:argparse.Namespace,g:Any,lease:Any,manager:Any,ident:Any,gen:int)->None:_probe_reg(a,g,lease,manager,ident,gen,False)

def _child(a:argparse.Namespace,g:Any,fd:int,mask:set[signal.Signals])->None:
 rc=2
 try:
  g._supervisor_cancel_signal=None;g._install_supervisor_signal_handlers(mask);g._become_child_subreaper();lease=g.lease;manager=lease.LeaseManager(STATE);ident=lease.LeaseIdentity(a.task_id,a.session_id);gen=_lease(manager,lease,ident,a.token_file);_cancel(g)
  {'bootstrap':_bootstrap,'rebind':_rebind,'gate-b':_gateb}[a.operation](a,g,lease,manager,ident,gen)
  print(f'TRACK_A_CANONICAL_{a.operation.upper().replace("-","_")}=PASS',flush=True);print(f'TRACK_A_CANONICAL_LEASE_GENERATION={gen}',flush=True);rc=0
 except (E,g.lease.LeaseError) as x:print(f'TRACK_A_CANONICAL_TRANSITION_ERROR={getattr(x,"code","lease_error")}',file=sys.stderr,flush=True)
 except subprocess.TimeoutExpired:print('TRACK_A_CANONICAL_TRANSITION_ERROR=worker_timeout',file=sys.stderr,flush=True)
 except BaseException:print('TRACK_A_CANONICAL_TRANSITION_ERROR=supervisor_failure',file=sys.stderr,flush=True)
 finally:
  try:os.close(fd)
  except OSError:pass
 os._exit(rc)

def _supervise(a:argparse.Namespace)->int:
 g=_guard();lease=g.lease;ident=lease.LeaseIdentity(lease._validate_identity(a.task_id,'task-id'),lease._validate_identity(a.session_id,'session-id'));manager=lease.LeaseManager(STATE);token=lease._read_private_token(a.token_file);manager._prepare();fd=os.open(manager.lock_path,os.O_RDWR);mask=None
 try:
  fcntl.flock(fd,fcntl.LOCK_EX);s=manager._load_state_unlocked();manager._require_current_unlocked(s,ident,token,lease._now_epoch(None));mask=signal.pthread_sigmask(signal.SIG_BLOCK,g.SUPERVISOR_CANCELLATION_SIGNALS);pid=os.fork()
  if pid==0:_child(a,g,fd,mask)
  pending=signal.sigpending()
  for sig in g.SUPERVISOR_CANCELLATION_SIGNALS:
   if sig in pending:
    try:os.kill(pid,sig)
    except ProcessLookupError:pass
    break
  signal.pthread_sigmask(signal.SIG_SETMASK,mask);mask=None;os.close(fd);fd=-1;_,st=os.waitpid(pid,0);return os.waitstatus_to_exitcode(st)
 finally:
  if mask is not None:
   try:signal.pthread_sigmask(signal.SIG_SETMASK,mask)
   except OSError:pass
  if fd>=0:
   try:os.close(fd)
   except OSError:pass

def parser()->argparse.ArgumentParser:
 p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='operation',required=True)
 for n in ('bootstrap','rebind','gate-b'):
  q=s.add_parser(n);q.add_argument('--task-id',required=True);q.add_argument('--session-id',required=True);q.add_argument('--token-file',required=True,type=Path)
  if n=='bootstrap':q.add_argument('--worker',required=True,type=Path);q.add_argument('--worker-timeout',type=int,default=180)
  else:q.add_argument('--probe',required=True,type=Path)
 return p

def main(v:Sequence[str]|None=None)->int:
 try:return _supervise(parser().parse_args(v))
 except Exception as x:print(f'TRACK_A_CANONICAL_TRANSITION_ERROR={getattr(x,"code","controller_failure")}',file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
