# AgriSense — Universal Input Contract & OOD Prevention Plan

## Goal
Eliminate Out-Of-Distribution (OOD) model extrapolation failures and bridge real-world farmer input data (Soil Health Cards, Imperial units, P2O5 / K2O oxides, annual rainfall) with the ML model's internal training envelope (`kg/ha` elemental N/P/K, `°C`, `mm/month`).

---

## 1. Model Training Envelope vs Real-World Input Units

| Parameter | Model Min | Model Max | Model Base Unit | Common Lab / Farmer Unit | Conversion Rule |
|---|---|---|---|---|---|
| **Nitrogen (N)** | 0 | 140 | kg/ha (elemental N) | kg/acre, kg/ha | `kg/acre × 2.471 = kg/ha` |
| **Phosphorus (P)** | 5 | 145 | kg/ha (elemental P) | ppm, kg/ha as P₂O₅ | `P₂O₅ × 0.4364 = P`, `ppm × 2.24 = kg/ha` |
| **Potassium (K)** | 5 | 205 | kg/ha (elemental K) | ppm, kg/ha as K₂O | `K₂O × 0.8302 = K`, `ppm × 2.24 = kg/ha` |
| **Temperature** | 8.8 | 43.7 | °C | °F, °C | `(°F - 32) × 5/9 = °C` |
| **Humidity** | 14.3 | 100.0 | % | % | Direct |
| **Soil pH** | 3.5 | 9.9 | pH scale | pH scale | Direct |
| **Rainfall** | 20.2 | 298.6 | mm/month (crop cycle) | mm/annual, inches | `Annual / 12 = Monthly`, `inches × 25.4 = mm` |

---

## 2. Tasks

- [x] **Task 1 — Backend OOD Safeguards & Conversion Helpers (`app.py`)**
  - Implement conversion helpers for P₂O₅ → P, K₂O → K, ppm → kg/ha, °F → °C, and Annual → Monthly Rainfall.
  - Return HTTP 400 with field-level range error if inputs exceed model training envelope.

- [x] **Task 2 — Multilingual Labeling & Guidance (`translations.py`)**
  - Update N/P/K, Temperature, Humidity, and Rainfall labels across all 12 supported languages (`en`, `hi`, `te`, `ta`, `kn`, `mr`, `bn`, `gu`, `ml`, `pa`, `or`, `ur`) with clear unit annotations.

- [x] **Task 3 — Zero-Shift UI & Input Contract Hints (`templates/index.html`)**
  - Retain `position: absolute` for `.error-text` and `row-gap: 1.5rem` to guarantee zero UI shifting when error messages toggle.
  - Add helper text/tooltips for monthly vs annual rainfall and elemental vs oxide fertilizer forms.

- [x] **Task 4 — Automated & Manual Verification**
  - Verify prediction endpoint returns HTTP 200 for valid inputs (metric & converted units) and HTTP 400 for OOD inputs.
