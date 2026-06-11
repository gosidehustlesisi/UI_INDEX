# UI_INDEX — Political Corruption Forensics

## Project Purpose

This is an **investigative data forensics project** examining political corruption patterns in the tri-state area (MD, VA, DC) through the lens of unemployment insurance policy accountability.

**The core investigative hypothesis:** The "stagnant safety net" for unemployment benefits is not an accident of fiscal constraint — it is a **deliberate policy choice** funded by political actors who benefit from a broken system. This project traces the money to prove it.

---

## Data Architecture

### Dual-Track Analysis (Intentional by Design)

We maintain **two parallel datasets** to detect corruption patterns that single-cycle analysis would miss:

| Track | File | Purpose | Data Source |
|-------|------|---------|-------------|
| **Official View** | `fec_funding_profiles.json` | Cycle-filtered (2024), sanitized, public-facing | `fec_integration_v251d.py` |
| **Investigative View** | `fec_funding_profiles_raw.json` | Multi-cycle, unfiltered, anomaly-detection | `fec_integration_raw_investigative.py` |
| **Delta Analysis** | `corruption_delta_analysis.json` | Cross-cycle discrepancy flags | `delta_analyzer.py` |

### The Delta IS the Signal

The gap between the cycle-filtered view and the multi-cycle raw view is **not a data quality issue** — it is the **primary investigative target**. When a candidate's multi-cycle total exceeds their current-cycle total by >100%, that indicates:

- Rolling committee structures that recycle funds indefinitely
- Self-funding loans carried across cycles to bypass disclosure
- Dark money routed through multi-cycle PACs and joint fundraising committees
- Committee reorganizations that obscure donor origins

---

## Key Investigative Findings

### Known Anomalies (Documented, Not Fixed)

| Anomaly | What the Official View Shows | What the Raw View Reveals | Interpretation |
|---------|------------------------------|---------------------------|----------------|
| Van Hollen total | $330,578 (2024 cycle) | $1,515,661 (all cycles) | **360% gap** — multi-cycle financial engineering or committee reorganization |
| JUSTICE 2022 | Not visible in 2024 cycle | $82K+ from prior cycle | Recycled campaign funds entering current cycle through amended filings |
| "Business" contributors | Categorized by name | Includes vendors (e.g., NEW BLUE INTERACTIVE, LLC) | Possible shell company payments laundered through contribution channels |

### Corruption Flags Generated

The `fec_integration_v251d.py` script now generates `corruption_flags` for each member:

- `multi_cycle_bleed` — Multi-cycle data appears in current-cycle query results (HIGH severity)
- `committee_transfer` — Leadership PACs, joint fundraising committees funneling money (MEDIUM severity)
- `excessive_self_funding` — Self-funding >50% of total (may indicate wealth concealment)
- `vendor_masquerading_as_donor` — Service providers tagged as business contributors (possible shell company)

---

## API Setup

### Required Environment Variables

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
# Edit .env with your real keys
```

| Variable | Source | Purpose |
|----------|--------|---------|
| `FEC_API_KEY` | https://api.open.fec.gov/developers/ | FEC campaign finance data |
| `CENSUS_API_KEY` | https://api.census.gov/data/key_signup.html | Median income by district |

Congress.gov uses `DEMO_KEY` (public, no signup required for basic use).

---

## Data Quality Philosophy

This project does **not** sanitize data to match official narratives. Instead:

1. **Preserve anomalies** — Flag discrepancies as investigative leads, not errors
2. **Dual-track validation** — Official view + raw view = corruption detection
3. **Never suppress the gap** — The gap between endpoints is the story
4. **Document uncertainty** — Every output carries `_metadata` with provenance, caveats, and reconciliation status

---

## File Structure

```
ui_index/
├── fec_integration_v251d.py          # Cycle-filtered official analysis
├── fec_integration_raw_investigative.py # Multi-cycle raw forensics
├── delta_analyzer.py                  # Cross-cycle corruption detection
├── generate_fec_charts.py             # Visualization (with cycle assertion)
├── political_layer_builder.py         # Congress.gov + Census enrichment
├── api_client.py                      # Self-healing API client with caching
├── data/political/
│   ├── fec_funding_profiles.json      # Official cycle-filtered profiles
│   ├── fec_funding_profiles_raw.json  # Multi-cycle raw profiles (investigative)
│   ├── corruption_delta_analysis.json # Delta flags and investigative priority
│   ├── members.json                   # Congress.gov member metadata
│   └── audit_log.json                 # All API calls, cached and live
├── figures/                           # Exported matplotlib charts
└── .env.example                       # API key template
```

---

## Investigative Methodology

### Phase 1: Data Collection (Dual Track)

```bash
# Official view (cycle-filtered, validated)
python fec_integration_v251d.py

# Investigative view (multi-cycle, anomaly-preserving)
python fec_integration_raw_investigative.py

# Delta analysis (corruption detection)
python delta_analyzer.py
```

### Phase 2: Visualization

```bash
# Charts with cycle assertion (fails if data is stale)
python generate_fec_charts.py
```

### Phase 3: Political Layer Enrichment

```bash
# Congress.gov + Census median income overlay
python political_layer_builder.py
```

---

## License

MIT — This is investigative journalism infrastructure. Use it to expose corruption.

## Author

Sierra Napier, MPA  
Project: **The Stagnant Safety Net: A Tri-State Forensic Audit**
