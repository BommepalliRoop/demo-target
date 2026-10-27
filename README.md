# demo-target

Deliberately old client app used by the PatchPilot demo. It is a small Flask service plus a tiny Node report helper.
Do not use it in production. Secrets, hostnames and payloads are fake.

## Layout

| Path | Purpose |
|---|---|
| `demo_app/` | Flask app: `/health`, `/greet/<name>`, `/import` (YAML, uses `yaml.load`), `/sync` (background `requests.get`) |
| `tests/test_app.py` | pytest suite; passes on the pinned old versions |
| `requirements.txt` | Exact pins (no ranges) |
| `requirements-dev.txt` | Adds pytest |
| `tools/report.js` | lodash `_.template` report helper |
| `tools/report.test.js` | `node --test` suite |

## Run tests

Python 3.11 is required. Use Python 3.11 or the old urllib3 pin breaks on newer Python (see Known issues).

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
pytest -q
```

Node tool:

```bash
npm install --ignore-scripts
npm test
```

## Expected PatchPilot outcome

Counts are alias-deduplicated advisories from OSV.dev (checked Oct 27, 2026).

| Ecosystem | Package | Pinned | Alerts | Reachable |
|---|---|---|---|---|
| PyPI | Flask | 1.1.2 | 2 | No (framework only) |
| PyPI | Werkzeug | 1.0.1 | 10 | No (framework only) |
| PyPI | Jinja2 | 2.11.2 | 5 | No (framework only) |
| PyPI | PyYAML | 5.3.1 | 1 | **Yes**: `yaml.load` in `POST /import` (P1) |
| PyPI | requests | 2.25.1 | 4 | **Yes**: `requests.get` in background job (P3/P4) |
| PyPI | urllib3 | 1.26.4 | 11 | No (requests only) |
| PyPI | MarkupSafe, itsdangerous, click | 1.1.1, 1.1.0, 7.1.2 | 0 | No |
| npm | lodash | 4.17.15 | 6 | Yes, generic analysis (`_.template` in `tools/report.js`) |

Total: **39 alerts** (33 PyPI, 6 npm). Expected result: 2 packages with reachable findings, 2 PRs.
One test (`test_parse_import_payload_without_loader_breaks_after_pyyaml_6`) breaks after the PyYAML 6 upgrade, so the AI patch has work to do.

## Known issues

- On Python 3.12+ `requests` 2.25.1 with the vendored urllib3 1.26.4 fails to import (`No module named 'urllib3.packages.six.moves'`). Use Python 3.11.
