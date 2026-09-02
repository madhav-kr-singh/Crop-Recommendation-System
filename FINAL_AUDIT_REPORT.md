# AGRISENSE — FINAL CROP RECOMMENDATION SYSTEM AUDIT REPORT

**Audit Date:** 2026-09-03  
**System Name:** AgriSense  
**Repository:** `crop-recommendation-system ui updated`  
**Dataset:** Atharva Ingle Crop Recommendation Dataset (`Crop_recommendation.csv`)  
**Scope:** Dataset · Model (`model.pkl`) · Scaler (`minmaxscaler.pkl`) · Notebook · `app.py` · `translations.py` · `templates/index.html`  
**Methodology:** Ponytail (minimum, verified, no invented values) + Multi-Agent Brainstorming (5-role structured review)

---

## EXECUTIVE SUMMARY

| # | Finding | Severity |
|---|---|---|
| 1 | N/P/K have **no physical unit defined** anywhere in dataset, notebook, backend, or UI | Critical |
| 2 | **No upper-bound validation** — inputs like N=5000, pH=99, Humidity=500% pass silently | Critical |
| 3 | OOD inputs cause **silent, confident wrong predictions** (Random Forest saturation) | Critical |
| 4 | Rainfall timeframe (monthly vs annual) is **undefined** | High |
| 5 | `standscaler.pkl` exists in repo but is **never used** — dead artifact | Low |
| 6 | Model accuracy (99.32%) and pipeline consistency are **correct and intact** | PASS |

**Production Readiness: NOT READY. Model is excellent; input contract is broken.**

---

## 1. MODEL INPUT VERIFICATION

| # | Feature | Dataset Col | Type | app.py Parsing | Model Index | Used? |
|---|---|---|---|---|---|---|
| 1 | Nitrogen | N | int64 | int(request.form["Nitrogen"]) line 46 | 0 | YES |
| 2 | Phosphorus | P | int64 | int(request.form["Phosphorus"]) line 47 | 1 | YES |
| 3 | Potassium | K | int64 | int(request.form["Potassium"]) line 48 | 2 | YES |
| 4 | Temperature | temperature | float64 | float(request.form["Temperature"]) line 49 | 3 | YES |
| 5 | Humidity | humidity | float64 | float(request.form["Humidity"]) line 50 | 4 | YES |
| 6 | pH | ph | float64 | float(request.form["Ph"]) line 51 | 5 | YES |
| 7 | Rainfall | rainfall | float64 | float(request.form["Rainfall"]) line 52 | 6 | YES |

**Verdict: TRUE.** All 7 features in exact order [N, P, K, temperature, humidity, ph, rainfall].

---

## 2. TRAINING DATASET AUDIT (Crop_recommendation.csv)

- Rows: 2,200 | Columns: 8 | Classes: 22 (100 samples each — perfectly balanced)
- Missing values: 0 | Duplicates: 0 | Invalid values: 0
- Crops (22): apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean, muskmelon, orange, papaya, pigeonpeas, pomegranate, rice, watermelon

### Empirical Feature Ranges (Computed Directly from File)

| Feature | Min | Max | Mean | Std Dev | Kaggle-Defined Unit |
|---|---:|---:|---:|---:|---|
| N | 0.00 | 140.00 | 50.55 | 36.92 | None — nutrient ratio |
| P | 5.00 | 145.00 | 53.36 | 32.99 | None — nutrient ratio |
| K | 5.00 | 205.00 | 48.15 | 50.65 | None — nutrient ratio |
| Temperature | 8.83 | 43.68 | 25.62 | 5.06 | deg C (implied) |
| Humidity | 14.26 | 99.98 | 71.48 | 22.26 | % (implied) |
| pH | 3.50 | 9.94 | 6.47 | 0.77 | Standard pH scale |
| Rainfall | 20.21 | 298.56 | 103.46 | 54.96 | mm monthly/cycle (implied) |

NOTE: Kaggle officially describes N/P/K as "nutrient-content ratios" with no declared physical unit. kg/ha is an interpretation/convention, not a specification.

---

## 3. MODEL & SCALER AUDIT

### model.pkl — RandomForestClassifier

| Parameter | Value |
|---|---|
| n_estimators | 100 |
| criterion | gini |
| max_depth | None (full depth) |
| min_samples_split | 2 |
| min_samples_leaf | 1 |
| max_features | sqrt |
| random_state | 42 |
| bootstrap | True |

Train/Test Split: 80/20 (random_state=42) -> 1,760 train / 440 test rows

| Metric | Value |
|---|---|
| Test Accuracy | 99.32% (437/440 correct) |
| Precision (Macro / Weighted) | 99.26% / 99.37% |
| Recall (Macro / Weighted) | 99.33% / 99.32% |
| F1-Score (Macro / Weighted) | 99.26% / 99.32% |
| 5-Fold CV Mean | 99.45% [99.77, 99.32, 99.77, 99.55, 98.86] |

### minmaxscaler.pkl — MinMaxScaler (Fitted on X_train)

| Feature | data_min_ | data_max_ | scale_ | min_ |
|---|---:|---:|---:|---:|
| N | 0.00000000 | 140.00000000 | 0.00714286 | 0.00000000 |
| P | 5.00000000 | 145.00000000 | 0.00714286 | -0.03571429 |
| K | 5.00000000 | 205.00000000 | 0.00500000 | -0.02500000 |
| temperature | 8.82567475 | 43.67549305 | 0.02869455 | -0.25324880 |
| humidity | 14.27327988 | 99.98187601 | 0.01166744 | -0.16653265 |
| ph | 3.50475231 | 9.93509073 | 0.15551281 | -0.54503388 |
| rainfall | 20.36001144 | 298.56011750 | 0.00359453 | -0.07318477 |

NOTE: MinMaxScaler is mathematically redundant for Random Forest but MUST remain in place since model was trained on scaled inputs.
DEAD ARTIFACT: standscaler.pkl is never loaded or referenced. Safe to delete.

---

## 4. N/P/K UNIT AMBIGUITY — FULL TRACE

| Component | File | Unit Status |
|---|---|---|
| Dataset header | Crop_recommendation.csv | N, P, K — NO UNIT |
| Training notebook | Crop recommendation system.ipynb | No unit declared |
| Backend | app.py:46-48 | Blind int cast, no unit |
| Frontend labels | translations.py:10-15 | "Nitrogen", "Phosphorus", "Potassium" — no unit |
| Frontend placeholders | templates/index.html:553-568 | "Enter Nitrogen" — no unit |

STATUS: UNIT NOT DEFINED ANYWHERE IN PROJECT.

AgriSense documented convention (chosen): kg/ha (elemental N, P, K).
This does NOT require retraining.

---

## 5. REAL-WORLD INPUT vs MODEL CONVENTION

### Model Training Envelope

| Parameter | Model Min | Model Max | Convention |
|---|---:|---:|---|
| Nitrogen (N) | 0 | 140 | kg/ha (elemental N) |
| Phosphorus (P) | 5 | 145 | kg/ha (elemental P) |
| Potassium (K) | 5 | 205 | kg/ha (elemental K) |
| Temperature | 8.83 | 43.68 | deg C |
| Humidity | 14.26 | 99.98 | % RH |
| pH | 3.50 | 9.94 | pH scale |
| Rainfall | 20.21 | 298.56 | mm (monthly/cycle) |

### Farmer Soil Report Conversions

| Parameter | Common Lab Form | Common Unit | Conversion to Model Convention |
|---|---|---|---|
| Nitrogen | Available N (KMnO4) | kg/ha or kg/acre | If kg/acre -> x2.471 |
| Phosphorus | Available P (Olsen/Bray) | ppm or kg/ha as P2O5 | P2O5 x 0.4364 = elemental P. ppm x 2.24 = kg/ha |
| Potassium | Available K (NH4OAc) | ppm or kg/ha as K2O | K2O x 0.8302 = elemental K. ppm x 2.24 = kg/ha |
| Temperature | Weather station | deg C or deg F | F to C: (F - 32) x 5/9 |
| Humidity | Hygrometer / RH | % | Direct |
| pH | 1:2.5 soil-water | dimensionless | Direct |
| Rainfall | Rain gauge | mm | MUST be monthly/cycle — NOT annual |

### Real-World Risk Table (Indian Soil Health Cards)

| Parameter | Typical SHC Range | Risk if Entered Directly |
|---|---|---|
| N | 150-450 kg/ha | 1-3x over model max (140) -> OOD saturation |
| P | 5-120 kg/ha | Within range if elemental P |
| K | 50-600 kg/ha | 0.25-3x model max (205) -> OOD at high end |
| Rainfall (annual) | 800-2000 mm | 3-7x model max (298) -> severe OOD |

---

## 6. OUT-OF-DISTRIBUTION (OOD) PROBLEM

### Trace: Farmer Enters N = 600

1. Frontend: min="0" check passes. Submitted without warning.
2. Backend: n = int(600) — accepted.
3. Scaler: scaled_N = (600 - 0) / 140 = 4.2857 (normal range [0.0, 1.0])
4. Model: RF splits are xi <= theta. Since 4.2857 > theta_max -> traverses outermost right path -> arbitrary leaf.
5. Output: 100% confident prediction (e.g. "coffee") with zero warning.

### Trace: Farmer Enters Annual Rainfall = 1200 mm

1. Scaler: scaled_rainfall = (1200 - 20.36) / 278.20 = 4.24 (3x out-of-range)
2. Model: Same leaf saturation -> wrong confident prediction.

### Risk Summary

| Risk | Impact |
|---|---|
| Silent extrapolation failure | Farmer acts on wrong recommendation |
| No OOD warning or confidence flag | No recourse |
| Trees cannot model gradients beyond training box | Any extreme input = nearest arbitrary leaf |

---

## 7. CURRENT UI INPUT AUDIT

| Field | HTML min | HTML max | Unit in Label | Unit in Placeholder |
|---|---|---|---|---|
| Nitrogen | 0 | NONE | NONE | NONE |
| Phosphorus | 0 | NONE | NONE | NONE |
| Potassium | 0 | NONE | NONE | NONE |
| Temperature | 0 | NONE | YES (deg C) | YES (deg C) |
| Humidity | 0 | NONE | YES (%) | YES (%) |
| pH | 0 | NONE | — | YES ("pH Value") |
| Rainfall | 0 | NONE | YES (mm) | YES (mm) |

No upper bounds anywhere. N/P/K have zero unit information.

---

## 8. VERIFICATION STATEMENT AUDIT

| # | Statement | Verdict | Issue | Fix |
|---|---|---|---|---|
| 1 | Model uses N, P, K, temp, humidity, pH, rainfall | TRUE | — | None |
| 2 | N/P/K from soil testing | TRUE (concept) | Unit/form not defined | Add kg/ha labels |
| 3 | pH from soil testing | TRUE | — | None |
| 4 | Temperature from weather data | TRUE | Avg season vs daily unclear | Clarify in placeholder |
| 5 | Humidity from weather data | TRUE | — | None |
| 6 | Rainfall from weather data | TRUE | Monthly vs annual undefined | Add mm/month to label |
| 7 | UI accepts correct units | FALSE | N/P/K no units; rainfall timeframe missing | Update labels + placeholders |
| 8 | UI has proper validation | FALSE | No upper bounds; pH=99, Humidity=500% accepted | Add max + server-side bounds |
| 9 | Model handles real-world OOD safely | FALSE | RF saturates silently at leaf thresholds | Validate before inference |
| 10 | System ready for general farmer usage | FALSE | Unit ambiguity + no OOD guard + no confidence score | Full validation + unit docs |

---

## 9. MULTI-AGENT BRAINSTORMING — STRUCTURED REVIEW

### Agent 1 — Primary Designer (Lead Auditor)

Design Proposal — 5-stage input pipeline:

  Soil Report Input
  -> Unit/Form Identifier (UI labels + tooltips)
  -> Agronomic Converter (P2O5->P, K2O->K, ppm->kg/ha, kg/acre->kg/ha)
  -> Range Validator (hard bounds against scaler data_min_/data_max_)
  -> MinMaxScaler
  -> Random Forest -> Recommendation

Decision Log Entry 1: Keep existing model + scaler. Only fix input contract.

---

### Agent 2 — Skeptic / Challenger

Objection 1: "Why not retrain on Indian SHC data?"
Resolution: Requires multi-regional, multi-season agro-climatic dataset across all 22 crops.
99.32% accuracy is sufficient if input contract is enforced. Retrain only if unit-converter layer fails.

Objection 2: "kg/ha convention is arbitrary — what if a lab reports mg/kg?"
Resolution: AgriSense documents kg/ha as declared convention. Converter provided for other units.
This is a documentation + UX problem, not a model problem.

Objection 3: "Rainfall timeframe still ambiguous."
Resolution: Placeholder must explicitly say "mm/month (growing season average)".
Annual rainfall / 12 is incorrect — monsoon distribution matters.

---

### Agent 3 — Constraint Guardian

Enforcement 1: Any scaled_feature outside [0.0, 1.0] is a hard constraint violation.
Must trigger user-visible error BEFORE model.predict() is called.

Enforcement 2: Server-side validation is non-negotiable.
Frontend JS can be bypassed (curl, Postman, form tampering). app.py must independently validate.

Enforcement 3: standscaler.pkl is dead code.
Must be documented as unused or deleted. Dead artifacts create maintenance confusion.

---

### Agent 4 — User Advocate

Flag 1: Farmers cannot know N/P/K is in kg/ha. The label MUST say it.
Flag 2: Farmers don't understand "cycle rainfall." Placeholder must say "monthly average rainfall during growing season."
Flag 3: Farmers should not manually convert P2O5 to P. Simple tooltip/toggle needed.
Flag 4: Error messages must state valid ranges, not just "invalid input."

---

### Agent 5 — Integrator / Arbiter

Accepted objections (all agents):
- Add explicit kg/ha to N/P/K labels and placeholders
- Add mm/month clarification to rainfall
- Add server-side VALIDATION_BOUNDS in app.py
- Add frontend max attributes to HTML inputs
- Remove or document standscaler.pkl
- Provide conversion tooltips for P2O5, K2O, ppm inputs

Rejected: Retraining. Current model is accurate. Input contract fix is sufficient.

FINAL DISPOSITION: APPROVED FOR IMPLEMENTATION
Proceed with input contract + validation layer only. Model and scaler remain unchanged.

---

## 10. CONCRETE ACTION PLAN (IMPLEMENTATION ROADMAP)

### A. Frontend Labels & Placeholders (translations.py + templates/index.html)

| Parameter | Current Label | Recommended Label | Recommended Placeholder |
|---|---|---|---|
| Nitrogen | Nitrogen | Nitrogen (N) [kg/ha] | e.g. 50  (0-140 kg/ha) |
| Phosphorus | Phosphorus | Phosphorus (P) [kg/ha] | e.g. 50  (5-145 kg/ha) |
| Potassium | Potassium | Potassium (K) [kg/ha] | e.g. 50  (5-205 kg/ha) |
| Temperature | Temperature | Temperature (deg C) | e.g. 25.5  (9-44 deg C) |
| Humidity | Humidity | Relative Humidity (%) | e.g. 70  (15-100 %) |
| pH | pH Level | Soil pH | e.g. 6.5  (3.5-9.5) |
| Rainfall | Rainfall | Monthly Rainfall (mm) | e.g. 100  (20-300 mm/month) |

---

### B. Backend Validation Layer (app.py)

```python
# ponytail: strict validation bounds matching model training distribution
VALIDATION_BOUNDS = {
    "Nitrogen":    {"min": 0,    "max": 140,  "unit": "kg/ha"},
    "Phosphorus":  {"min": 5,    "max": 145,  "unit": "kg/ha"},
    "Potassium":   {"min": 5,    "max": 205,  "unit": "kg/ha"},
    "Temperature": {"min": 8.0,  "max": 45.0, "unit": "deg C"},
    "Humidity":    {"min": 14.0, "max": 100.0,"unit": "%"},
    "Ph":          {"min": 3.5,  "max": 10.0, "unit": "pH"},
    "Rainfall":    {"min": 20.0, "max": 300.0,"unit": "mm/month"},
}

def validate_inputs(data):
    # ponytail: returns dict of field -> error message, empty dict = valid
    errors = {}
    for field, b in VALIDATION_BOUNDS.items():
        val = data.get(field)
        if val is None or not (b["min"] <= val <= b["max"]):
            errors[field] = f"{field} must be between {b['min']} and {b['max']} {b['unit']}"
    return errors
```

---

### C. HTML Input Bounds (templates/index.html)

Add max attributes matching model envelope:

  Nitrogen:    min="0"   max="140"  step="1"
  Phosphorus:  min="5"   max="145"  step="1"
  Potassium:   min="5"   max="205"  step="1"
  Temperature: min="8"   max="44"   step="0.01"
  Humidity:    min="14"  max="100"  step="0.01"
  pH:          min="3.5" max="10"   step="0.01"
  Rainfall:    min="20"  max="300"  step="0.01"

---

### D. Recommended UI Validation Ranges (Soft vs Hard)

| Field | Hard Min | Model Max (Soft) | Hard Max |
|---|---:|---:|---:|
| Nitrogen (kg/ha) | 0 | 140 | 200 |
| Phosphorus (kg/ha) | 0 | 145 | 250 |
| Potassium (kg/ha) | 0 | 205 | 350 |
| Temperature (deg C) | 0 | 44 | 55 |
| Humidity (%) | 5 | 100 | 100 |
| Soil pH | 3.0 | 10 | 10.5 |
| Rainfall (mm/month) | 0 | 300 | 500 |

---

### E. Soil Health Card Conversion Formulas

| From | To | Formula |
|---|---|---|
| P2O5 (kg/ha) | Elemental P (kg/ha) | P = P2O5 x 0.4364 |
| K2O (kg/ha) | Elemental K (kg/ha) | K = K2O x 0.8302 |
| ppm (mg/kg) | kg/ha | kg/ha = ppm x 2.24 (15cm furrow, rho=1.33 g/cm3) |
| kg/acre | kg/ha | kg/ha = kg/acre x 2.471 |
| deg F | deg C | C = (F - 32) x 5/9 |
| Annual rainfall | Monthly avg | Divide by growing months (NOT simple /12) |

---

### F. Model Retraining Verdict

| Question | Answer |
|---|---|
| Retrain the model? | NO |
| Retrain the scaler? | NO |
| Why? | 99.32% accuracy, 99.45% 5-fold CV — model correct within envelope |
| What to fix? | Input contract, validation layer, UI labels |
| When to retrain? | Only if adding direct SHC raw-unit support requiring new input scale |

---

## 11. DECISION LOG

| # | Decision | Alternatives Considered | Objection | Resolution |
|---|---|---|---|---|
| 1 | Keep existing RF model unchanged | Retrain on Indian SHC data | No multi-regional dataset available | Rejected retraining |
| 2 | Use kg/ha as documented N/P/K convention | ppm, mg/kg, no unit declared | Ambiguous for farmers | Document + enforce in UI and backend |
| 3 | Add server-side validation before inference | OOD-clip instead of reject | Clip silently hides data quality issues | Reject out-of-range with clear error |
| 4 | Remove/document standscaler.pkl | Keep as-is | Dead artifact causes maintenance confusion | Document or delete |
| 5 | Rainfall = monthly/cycle average | Annual / seasonal total | Dataset max 298mm inconsistent with Indian annual (800-2000mm) | Confirm monthly; state in placeholder |

---

Report version: FINAL
All ranges sourced from direct inspection of Crop_recommendation.csv and minmaxscaler.pkl.
No values invented.
