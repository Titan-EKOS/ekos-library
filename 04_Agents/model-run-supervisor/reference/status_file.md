# Status file (D08)

One file per job the user can open at any time: `20_Working\runs\run_status.md` plus `run_status.json`.
Written by `scripts/run_checks.py status run_register.csv --out-md run_status.md --out-json run_status.json`
after every poll. The supervisor updates `progress_hr`, `eta` and `last_check` in the register first.

Rules
- Status comes only from closed files and verified processes (name + command line + creation time).
- Queued is never reported as done. "complete-unchecked" is not "accepted".
- Chat status must match this file word for word on counts.
- Notify only on: run finished and accepted/rejected, failure, decision needed. No routine heartbeat messages.
- Heartbeat (15-30 min) refreshes the file only; skip when a healthy run is active and nothing changed; pause after
  delivery or a user freeze.

Register columns used by the status writer
job_id, engine, folder_or_plan, status, progress_hr, end_hr, eta, last_check, note

Status values
queued / preflight-fail / running / stalled / failed / complete-unchecked / accepted / rejected

Progress sources
- FLO-2D: simulated hour from SUMMARY.OUT / TIME.OUT (closed reads only).
- HEC-RAS: stdout progress line of the compute process; never open the live pNN.tmp.hdf.
- HEC-HMS: compute log.
