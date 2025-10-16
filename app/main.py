# -------------------------------------------------------
# app/main.py
# -------------------------------------------------------
# Author: projectfong
# Copyright (c) 2025 Fong
# All Rights Reserved
# -------------------------------------------------------
#!/usr/bin/env python3
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List
import hashlib
from .logger_config import audit_log, write_vector

app = FastAPI(title="cfo-ai-security-demo", version="1.0.0")

class IngestInput(BaseModel):
    message: str = Field(min_length=1)
    source: Optional[str] = "fwlogs"

def _mock_vessel_summary(text: str) -> str:
    h = hashlib.sha256(text.encode()).hexdigest()[:12]
    return f"[mock] summary:{h}"

def _mock_embed_vector(text: str) -> List[float]:
    h = hashlib.sha256(text.encode()).hexdigest()
    base = int(h[:8], 16)
    return [((base >> (i % 16)) & 0xFF) / 255.0 for i in range(16)]

@app.get("/healthz")
def healthz():
    eid = audit_log("demo-api","healthz",{"status":"ok"})
    return {"status":"ok","event_id":f"sha256:{eid}"}

@app.post("/mock/ingest")
def mock_ingest(inp: IngestInput):
    audit_log("fwlogs","mock_receive",{"len":len(inp.message),"source":inp.source})
    summary = _mock_vessel_summary(inp.message)
    audit_log("vessel","mock_summarize",{"summary_len":len(summary)})
    vec = _mock_embed_vector(summary)
    audit_log("embed","mock_embed",{"dims":len(vec)})
    eid = write_vector({
        "component":"orchestrator",
        "action":"mock_upsert",
        "source":inp.source,
        "summary":summary,
        "vector_mock":vec,
        "category":"network-activity"
    })
    return {"status":"ok","summary":summary,"vector_dims":len(vec),"category":"network-activity","event_id":f"sha256:{eid}"}
