# -------------------------------------------------------
# app/logger_config.py
# -------------------------------------------------------
# Author: projectfong
# Copyright (c) 2025 Fong
# All Rights Reserved
# -------------------------------------------------------
#!/usr/bin/env python3
import os, json, hashlib
from datetime import datetime, timezone
EVIDENCE_ROOT = os.environ.get("EVIDENCE_ROOT","./evidence")
def _utc(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def _dir(kind):
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    p = os.path.join(EVIDENCE_ROOT, kind, day); os.makedirs(p, exist_ok=True); return p
def _h(d): return hashlib.sha256(json.dumps(d, sort_keys=True, separators=(',',':')).encode()).hexdigest()
def audit_log(component, action, payload):
    rec = {"ts":_utc(),"component":component,"action":action,"payload":payload}; eid=_h(rec); rec["event_id"]=eid
    with open(os.path.join(_dir("logs"),"api.log"),"a",encoding="utf-8") as f: f.write(json.dumps(rec, sort_keys=True)+"\n")
    print(f"{rec['ts']} component={component} action={action} event_id=sha256:{eid}")
    return eid
def write_vector(entry):
    rec = {"ts":_utc(), **entry}; eid=_h(rec); rec["event_id"]=eid
    with open(os.path.join(_dir("vectors"),"vector_log.jsonl"),"a",encoding="utf-8") as f: f.write(json.dumps(rec, sort_keys=True)+"\n")
    return eid
