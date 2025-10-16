# cfo-ai-security-demo

Author: projectfong  
Copyright (c) 2025 Fong  
All Rights Reserved

---

## Summary

`cfo-ai-security-demo` is a **public-safe, runnable demonstration** built on the **AI orchestration framework `cfo-aistack`**.
The system connects to a firewall API, retrieves log entries, and performs **echo-based mock calls** to two core `cfo-aistack` services:
**`cfo-vessel`** (summarization engine) and **`cfo-embed`** (1024-dimensional embedding engine).
Each stage produces deterministic, reproducible JSON evidence representing what the full production system would generate during real summarization and embedding operations.
The demo runs fully offline, writing all output as structured evidence for audit and validation.
It aligns with established cybersecurity frameworks and best practices (e.g., NIST SP 800-171 concepts), emphasizing **secure-by-design** architecture, reproducibility, and traceable audit generation.

---

## Purpose

* Demonstrate how `cfo-ai-security` integrates with `cfo-aistack` using only `cfo-vessel` and `cfo-embed`.
* Provide a safe, offline mock implementation of the summarization and embedding stages in the AI Security Stack.
* Capture timestamped, hash-verified JSON evidence showing deterministic orchestration and event logging.
* Showcase secure handling and organization of firewall log data using auditable, offline methods.
* For research and demonstration only; not production software. License: All Rights Reserved.

---

## Core Components

| Component                   | Description                                                                                                    | Notes                                            |
| --------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **cfo-ai-security-fwlogs**  | Connects to a firewall API, retrieves log data, and passes entries into the `cfo-aistack` integration workflow | Deterministic, offline-only                      |
| **cfo-ai-security**         | Main orchestrator that calls `cfo-vessel` (summary) and `cfo-embed` (embedding) through mock echo routines     | Writes all results as structured evidence        |
| **cfo-vessel (mock)**       | Simulated summarization engine from `cfo-aistack`; returns structured plain-text summaries                     | Echo-only; fully offline                         |
| **cfo-embed (mock)**        | Simulated embedding engine that returns deterministic 1024-D vector arrays                                     | Echo-only; fully offline                         |
| **Evidence Logger**         | Records each mock API interaction, summary, and embedding to JSONL files                                       | `./evidence/logs/YYYY-MM-DD/api.log`             |
| **Vector Evidence Store**   | Stores mock vector records generated from `cfo-embed`                                                          | `./evidence/vectors/YYYY-MM-DD/vector_log.jsonl` |
| **CLI Tool**                | Triggers mock ingestion, health checks, and evidence validation                                                | Offline execution                                |
| **cfo-aistack (framework)** | Provides interface layer for connecting `cfo-ai-security` to `cfo-vessel` and `cfo-embed`                      | Only these two components used in demo           |

---

## Memory Structure

`cfo-ai-security-demo` references the **tiered memory model** implemented in the full `cfo-ai-security` system.
In the production environment, this model uses **Qdrant** as the vector database to organize categorized embeddings and summarized records across distinct memory tiers.
Each tier represents a specific stage of event lifecycle and trust level, allowing separation between transient alerts, pattern recognition, immutable baselines, and long-term retention.

This **demo does not implement** the full tiered memory engine.
Instead, it **simulates the conceptual flow** of data through these tiers by writing **mock JSON evidence files** to represent how logs and embeddings would be processed in the complete system.

| Tier      | Purpose                           | Description                                                                       | Demo Implementation                                    |
| --------- | --------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------ |
| **AISTM** | Short-Term Volatile Alerts        | Holds transient security events and short-lived detections (fast TTL).            | Simulated via JSON evidence records only.              |
| **AIMTM** | Mid-Term Pattern Candidates       | Retains events showing repetitive or evolving behavior for pattern evaluation.    | Not implemented; represented conceptually.             |
| **AIPM**  | Confirmed Pattern Memory          | Stores validated or recurring patterns indicating known behaviors or anomalies.   | Not implemented; referenced for context.               |
| **AIBM**  | Immutable Baseline Memory         | Contains stable baseline data such as firewall configurations and trusted states. | Not implemented; shown for architectural completeness. |
| **AILTM** | Trusted Long-Term Memory          | Retains confirmed events and summaries for extended recall and validation.        | Not implemented; concept only.                         |
| **AIAM**  | Archive Memory                    | Compresses older evidence entries for long-term offline storage.                  | Not implemented; concept only.                         |
| **AIIM**  | Immutable Rules and Ethics Memory | Holds fixed rule sets and system integrity constraints; monitored for drift.      | Not implemented; concept only.                         |
| **AILM**  | Log Memory                        | Represents raw log collections (e.g., firewall and infrastructure logs).          | Simulated via local JSON logs.                         |

All embeddings and summaries in the demo are **echo-based mock records** that conceptually correspond to these memory tiers.
No real Qdrant persistence, tier promotion, or background maintenance occurs — this is an **illustrative model only**.

---

## Background Jobs

The production `cfo-ai-security` system maintains tier health and consistency through scheduled background tasks.
These tasks are **not active in the demo**; their purpose is documented below for architectural context.
In this demonstration, they appear only as **descriptive placeholders** and **do not execute any automation**.

| Task                        | Interval | Description                                                    | Demo Implementation |
| --------------------------- | -------- | -------------------------------------------------------------- | ------------------- |
| **AIIM Monitor**            | 60s      | Detects immutable memory drift and logs compliance results.    | Not implemented.    |
| **OPNsense Config Watcher** | 60s      | Monitors firewall configuration changes and reloads baselines. | Not implemented.    |
| **Vector Cleanup**          | 60s      | Removes expired records from the AISTM tier.                   | Not implemented.    |
| **AIMTM Promotion**         | 300s     | Promotes recurring logs from AIMTM to AIPM.                    | Not implemented.    |
| **AILM Exporter**           | 300s     | Archives older log memory entries to disk.                     | Not implemented.    |
| **Tier Auditor**            | Weekly   | Scans for tier mismatches and corrective alignment.            | Not implemented.    |

These background job definitions are retained in documentation for structural visibility only and do not execute in the demo.

---

## Promotion Logic

In the production system, promotion logic is handled by background processes that evaluate frequency, trust level, and category metrics.
For the purposes of this **public-safe demonstration**, the following rules are shown for **context only**.
No actual promotion, baseline comparison, or anomaly evaluation occurs.

1. New logs start in **AISTM**.
2. If repeated more than five times → promoted to **AIMTM**.
3. Events matching known baselines or trusted tiers → promotion blocked.
4. Confirmed anomaly → promoted to **AIPM**.
5. Stable events older than 30 days → promoted to **AILTM**.

In this demo, each ingestion simply produces a mock summary and embedding record written to `./evidence/` for audit verification — no dynamic tier movement occurs.

---

## Databases and Storage

| Store                        | Purpose                                                       | Retention               |
| ---------------------------- | ------------------------------------------------------------- | ----------------------- |
| **Evidence Logs**            | Audit trail of ingestion, summarization, and embedding events | Local developer control |
| **Vector Evidence (JSON)**   | Stores mock vector data and metadata                          | Local developer control |
| **Hash Manifest (optional)** | Records hash integrity values for evidence verification       | Local developer control |

Validation Result:
Running the demo performs a full mock ingestion cycle — firewall → vessel → embed — and produces deterministic JSON evidence under `./evidence/`.
Each run generates reproducible SHA256 event IDs and timestamped entries suitable for audit review.

---

## Evidence Structure

```
evidence/
  logs/
    YYYY-MM-DD/
      api.log               # JSONL: ts, component, action, payload, event_id
  vectors/
    YYYY-MM-DD/
      vector_log.jsonl      # JSONL: mock embeddings and metadata
  hashes/
```

Each record includes the simulated flow:

```json
{
  "ts": "2025-10-15T21:42:08Z",
  "component": "fwlogs",
  "action": "mock_ingest",
  "summary": "[mock] Firewall connection accepted on port 443",
  "vector_mock": [0.001, 0.002, 0.003, "..."],
  "category": "network-activity",
  "event_id": "sha256:91a6f8...",
  "status": "recorded"
}
```

Validation Result:
Entries contain reproducible timestamps, summaries, and deterministic hash IDs; no external calls or real embeddings are performed.

---

## Installation with Logs

### Build

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### Create Container

```bash
docker compose up --build -d
```

### Verify

```bash
curl -s http://127.0.0.1:8080/healthz
pytest -q
```

Expected Results:

* HTTP 200 JSON: `{"status":"ok","event_id":"sha256:..."}`
* Evidence written under `./evidence/logs/<today>/api.log` and `./evidence/vectors/<today>/vector_log.jsonl`.
* Deterministic event IDs confirm reproducibility.

Validation Result:
Mock services respond deterministically, confirming offline operation and full evidence logging.

---

## CLI

```bash
python tools/cli.py health
python tools/cli.py mock-ingest
python tools/cli.py verify-evidence
```

| Command           | Description                                            |
| ----------------- | ------------------------------------------------------ |
| `health`          | Check API health and confirm mock mode status          |
| `mock-ingest`     | Run simulated firewall → vessel → embed pipeline       |
| `verify-evidence` | Validate JSON structure, timestamps, and SHA256 hashes |

Validation Result:
CLI confirms container health, executes mock ingestion, and prints reproducible event IDs.

### Logs

python tools/cli.py health
```
python ./tools/cli.py health
2025-10-16T08:04:50Z cli=start cmd=health
{
  "event_id": "sha256:239503798891f02e2011fbd8ee74d82db3835582e72124fa4b559ba5c53221c6",
  "status": "ok"
}
2025-10-16T08:04:50Z cli=done cmd=health
```

python tools/cli.py mock-ingest
```
python ./tools/cli.py mock-ingest --message "Test inbound connection on port 443" --source fwlogs
2025-10-16T08:05:05Z cli=start cmd=mock-ingest
{
  "category": "network-activity",
  "event_id": "sha256:f894b5fd6148f0fdbebdea0d55e95ef5961719587cede8c8868af3882fc3ddbc",
  "status": "ok",
  "summary": "[mock] summary:dd5ba488d98d",
  "vector_dims": 16
}
2025-10-16T08:05:05Z cli=done cmd=mock-ingest
```
python tools/cli.py verify-evidence
```
python ./tools/cli.py verify-evidence
2025-10-16T08:11:37Z cli=start cmd=verify-evidence

Verification Summary:
  Files checked : 3
  Verified       : 3
  Failed         : 0
  Result         : VERIFIED (All entries passed)
{
  "status": "done"
}
2025-10-16T08:11:37Z cli=done cmd=verify-evidence
```
---

## Security and Isolation Notes

* Containers run as **non-root users** with minimal privileges.
* No outbound network traffic; all mock calls handled locally.
* `.env` file optional and does not include secrets.
* Filesystem is read-only except for `./evidence`.
* Each operation generates timestamped, hash-verified evidence entries.
* Mock summarization and embedding ensure no sensitive data is processed or exposed.

---

## License

All Rights Reserved. Redistribution or commercial use is prohibited.
See `LICENSE.md` for full license terms.

---

## Revision Control

| Version   | Date       | Summary                                                                                                     | Author      |
| --------- | ---------- | ----------------------------------------------------------------------------------------------------------- | ----------- |
| **1.0.0** | 2025-10-15 | Public-safe runnable demo using `cfo-aistack` (`cfo-vessel` + `cfo-embed`) with deterministic mock evidence | projectfong |

