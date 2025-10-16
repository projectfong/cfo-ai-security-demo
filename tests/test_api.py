# -------------------------------------------------------
# tests/test_api.py
# -------------------------------------------------------
# Author: projectfong
# Copyright (c) 2025 Fong
# All Rights Reserved
# -------------------------------------------------------
from fastapi.testclient import TestClient
from app.main import app
c = TestClient(app)
def test_healthz():
    r=c.get("/healthz"); assert r.status_code==200; assert r.json().get("status")=="ok"
def test_mock_ingest():
    r=c.post("/mock/ingest",json={"message":"Example 443 inbound","source":"fwlogs"})
    assert r.status_code==200; j=r.json(); assert j.get("status")=="ok"; assert j.get("vector_dims")==16
