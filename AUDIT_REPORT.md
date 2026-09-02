# AGRISENSE CROP RECOMMENDATION SYSTEM — SYSTEM & AGRONOMIC AUDIT REPORT

**Audit Date:** 2026-09-03  
**System Name:** AgriSense (Crop Recommendation System)  
**Target Repository:** `c:\Users\ADMIN\Desktop\crop\crop-recommendation-system ui updated`  
**Dataset Reference:** Atharva Ingle Crop Recommendation Dataset (`Crop_recommendation.csv`)  
**Audit Scope:** Dataset, Model (`model.pkl`), Scaler (`minmaxscaler.pkl`), Training Notebook (`Crop recommendation system.ipynb`), Backend (`app.py`), Translations (`translations.py`), and Frontend (`templates/index.html`).

---

## EXECUTIVE SUMMARY & CRITICAL FINDINGS

1. **Dataset Origin & Unit Reality:**  
   The underlying dataset is Atharva Ingle's Crop Recommendation Dataset from Kaggle.
   - **Kaggle officially describes $N, P, K$ as *nutrient-content ratios*** and **does not declare any physical unit** ($kg/ha$, $ppm$, $mg/kg$, etc.) in the data specification.
   - While academic literature commonly references $kg/ha$ as a working assumption, **$kg/ha$ is an interpretation convention, not an official Kaggle specification**.
2. **Current Code Assumptions:**  
   The current codebase accepts raw integers for $N, P, K$ without any unit label in the UI, without unit conversions in the backend, and without range validation against the model's training envelope.
3. **The Interoperability Gap:**  
   Real-world farmers obtain soil health cards with varying units ($\text{kg/ha}$, $\text{ppm}$, $\text{kg/acre}$, $P_2O_5$, $K_2O$). Directly passing unstandardized laboratory numbers into `MinMaxScaler` produces distorted feature vectors and arbitrary model outputs.
4. **Architectural Solution:**  
   The production pipeline must follow a deterministic flow:  
   $$\text{Soil / Weather Report} \longrightarrow \text{Identify Unit \& Form} \longrightarrow \text{Standardize / Convert} \longrightarrow \text{Range Validate} \longrightarrow \text{MinMaxScaler} \longrightarrow \text{Random Forest} \longrightarrow \text{Recommendation}$$

---

## 1. PROJECT / MODEL INPUTS & TRACEABILITY

| # | Expected Feature | Dataset Column | Data Type | Backend Parsing (`app.py`) | Model Feature Index | Actually Used in Prediction? |
|---|---|---|---|---|---|---|
| 1 | Nitrogen | `N` | `int64` | `int(request.form["Nitrogen"])` (line 46) | 0 | **YES** |
| 2 | Phosphorus | `P` | `int64` | `int(request.form["Phosphorus"])` (line 47) | 1 | **YES** |
| 3 | Potassium | `K` | `int64` | `int(request.form["Potassium"])` (line 48) | 2 | **YES** |
| 4 | Temperature | `temperature` | `float64` | `float(request.form["Temperature"])` (line 49) | 3 | **YES** |
| 5 | Humidity | `humidity` | `float64` | `float(request.form["Humidity"])` (line 50) | 4 | **YES** |
| 6 | pH | `ph` | `float64` | `float(request.form["Ph"])` (line 51) | 5 | **YES** |
| 7 | Rainfall | `rainfall` | `float64` | `float(request.form["Rainfall"])` (line 52) | 6 | **YES** |

- **Feature Order:** Exact sequence `[N, P, K, temperature, humidity, ph, rainfall]` constructed in `app.py:54` matching `ms.feature_names_in_`.
- **Target Label:** `label` (22 string classes).
- **Confirmation:** **TRUE**. All 7 features are actively used in prediction in identical order.

---

## 2. TRAINING DATASET AUDIT (`Crop_recommendation.csv`)

### Dataset Statistics (Empirical Values Computed Directly from File)

- **Total Rows:** `2,200`
- **Total Columns:** `8` (`N`, `P`, `K`, `temperature`, `humidity`, `ph`, `rainfall`, `label`)
- **Number of Crop Classes:** `22` (Exactly 100 samples per class — perfectly balanced)
- **Crop / Class Names (22):**  
  `apple`, `banana`, `blackgram`, `chickpea`, `coconut`, `coffee`, `cotton`, `grapes`, `jute`, `kidneybeans`, `lentil`, `maize`, `mango`, `mothbeans`, `mungbean`, `muskmelon`, `orange`, `papaya`, `pigeonpeas`, `pomegranate`, `rice`, `watermelon`
- **Missing / Null Values:** `0` across all columns.
- **Duplicate Rows:** `0` duplicates.
- **Invalid / Non-Numeric Values:** `0`.

### Exact Dataset & Scaler Learned Ranges

| Parameter | Dataset Min | Dataset Max | Scaler `data_min_` | Scaler `data_max_` | Dataset Mean | Dataset Std Dev | Kaggle Defined Unit |
|---|---:|---:|---:|---:|---:|---:|---|
| **N** (Nitrogen) | **0.00** | **140.00** | `0.00000000` | `140.00000000` | 50.55 | 36.92 | *Ratio (No physical unit)* |
| **P** (Phosphorus) | **5.00** | **145.00** | `5.00000000` | `145.00000000` | 53.36 | 32.99 | *Ratio (No physical unit)* |
| **K** (Potassium) | **5.00** | **205.00** | `5.00000000` | `205.00000000` | 48.15 | 50.65 | *Ratio (No physical unit)* |
| **Temperature** | **8.83** | **43.68** | `8.82567475` | `43.67549305` | 25.62 | 5.06 | *°C (Implied by values)* |
| **Humidity** | **14.26** | **99.98** | `14.27327988` | `99.98187601` | 71.48 | 22.26 | *% (Relative Humidity)* |
| **pH** | **3.50** | **9.94** | `3.50475231` | `9.93509073` | 6.47 | 0.77 | *Standard pH scale* |
| **Rainfall** | **20.21** | **298.56** | `20.36001144` | `298.56011750` | 103.46 | 54.96 | *mm (Cycle / Monthly)* |

---

## 3. MODEL TRAINING & PREPROCESSING AUDIT

- **Notebook Used:** `Crop recommendation system.ipynb` (12 cells total).
- **ML Algorithm:** `RandomForestClassifier` from `sklearn.ensemble`.
- **Model Parameters (`model.pkl`):**
  - `n_estimators=100`, `criterion='gini'`, `max_depth=None`, `min_samples_split=2`, `min_samples_leaf=1`, `max_features='sqrt'`, `random_state=42`, `bootstrap=True`.
- **Train / Test Split:** `test_size=0.2` (1,760 train rows, 440 test rows), `random_state=42`.
- **Scaler Used:** `MinMaxScaler` fitted on `X_train` (`minmaxscaler.pkl`).
- **StandScaler Note:** `standscaler.pkl` exists in the repo root but is not loaded or referenced in `app.py`.
- **Model Evaluation Metrics:**
  - **Accuracy:** `99.32%` (437 / 440 correct predictions on test set)
  - **Precision (Macro / Weighted):** `99.26%` / `99.37%`
  - **Recall (Macro / Weighted):** `99.33%` / `99.32%`
  - **F1-Score (Macro / Weighted):** `99.26%` / `99.32%`
  - **5-Fold Cross-Validation Accuracy:** `[99.77%, 99.32%, 99.77%, 99.55%, 98.86%]`, Mean = **99.45%**.
- **Preprocessing in Inference (`app.py:55`):** Identical scaler (`ms.transform()`) is applied to inputs before passing to `model.predict()`.

---

## 4. CODEBASE INSPECTION: WHERE N, P, K ARE HANDLED

Below is the complete inventory of every location in the project where N, P, and K are handled:

| Component | File Path | Exact Lines | Code Snippet / Element | Current Handling & Assumption |
|---|---|---|---|---|
| **Frontend Form** | `templates/index.html` | 553–568 | `<input type="number" id="Nitrogen" name="Nitrogen" min="0" ...>` | Only checks `min="0"`. **No unit displayed in label or placeholder**. |
| **Frontend Validation** | `templates/index.html` | 664–670 | `if (['-', 'e', 'E', '+'].includes(e.key)) e.preventDefault();` | Blocks negative signs and letters. No upper bound check. |
| **English Translations** | `translations.py` | 10–15 | `"nitrogen": "Nitrogen"`, `"enter_nitrogen": "Enter Nitrogen"` | **No unit specified** for N, P, K. |
| **Multilingual Translations** | `translations.py` | 60–700 | 11 other Indian languages (`hi`, `te`, `ta`, etc.) | Literal crop/nutrient names without units. |
| **Backend Parsing** | `app.py` | 46–48 | `n = int(request.form["Nitrogen"])` ... | Blind integer casting. Assumes raw input directly matches training scale. |
| **Feature Array Assembly** | `app.py` | 54 | `features = np.array([[n, p, k, temp, humidity, ph, rainfall]])` | Assembles 7-element vector in training order. |
| **Scaler Transformation** | `app.py` | 55 | `features = ms.transform(features)` | Normalizes inputs: $(x - \min) / (\max - \min)$. Unbounded if input $> \max$. |
| **Model Inference** | `app.py` | 57 | `prediction = model.predict(features)` | Classifies scaled vector using Random Forest decision trees. |
| **Result Presentation** | `templates/index.html` | 608 | `<span class="result-card__crop">{{ t(result, lang) }}</span>` | Displays predicted crop name; input values/units are not echoed back. |

---

## 5. REAL-WORLD FARMER INPUT VS MODEL CONVENTION

### TABLE A — CURRENT MODEL DATA RANGE & CONVENTION

| Parameter | Dataset Min | Dataset Max | Model Input Convention | Source |
|---|---:|---:|---|---|
| **Nitrogen (N)** | `0.00` | `140.00` | **Ratio scale / Documented convention ($\text{kg/ha}$)** | `Crop_recommendation.csv` (Col 0) |
| **Phosphorus (P)** | `5.00` | `145.00` | **Ratio scale / Documented convention ($\text{kg/ha}$)** | `Crop_recommendation.csv` (Col 1) |
| **Potassium (K)** | `5.00` | `205.00` | **Ratio scale / Documented convention ($\text{kg/ha}$)** | `Crop_recommendation.csv` (Col 2) |
| **Temperature** | `8.83` | `43.68` | **°C** (Ambient growing condition) | `Crop_recommendation.csv` (Col 3) |
| **Humidity** | `14.26` | `99.98` | **%** (Relative humidity) | `Crop_recommendation.csv` (Col 4) |
| **pH** | `3.50` | `9.94` | **pH scale** ($0–14$) | `Crop_recommendation.csv` (Col 5) |
| **Rainfall** | `20.21` | `298.56` | **mm** (Cycle / monthly rainfall) | `Crop_recommendation.csv` (Col 6) |

---

### TABLE B — FARMER INPUT (REAL-WORLD SOIL REPORT VARIATIONS)

| Parameter | Laboratory Test Form / Unit | Typical Soil Report Unit | Agronomic Conversion to Model Convention |
|---|---|---|---|
| **Nitrogen (N)** | Available N ($\text{KMnO}_4$ method) | $\text{kg/ha}$ | If report is in $\text{kg/ha}$, direct mapping (if in range $0–140$). If $\text{kg/acre}$, $\text{kg/ha} = \text{kg/acre} \times 2.471$. |
| **Phosphorus (P)** | Available P (Olsen / Bray method) | $\text{ppm}$ or $\text{kg/ha as } P_2O_5$ | $\text{kg/ha } P_2O_5 \times 0.4364 = \text{Elemental } P\text{ (kg/ha)}$. $\text{ppm } P \times 2.24 = \text{kg/ha } P$. |
| **Potassium (K)** | Available K ($\text{NH}_4\text{OAc}$ method) | $\text{ppm}$ or $\text{kg/ha as } K_2O$ | $\text{kg/ha } K_2O \times 0.8302 = \text{Elemental } K\text{ (kg/ha)}$. $\text{ppm } K \times 2.24 = \text{kg/ha } K$. |
| **Temperature** | Local weather forecast / station | $^\circ\text{C}$ or $^\circ\text{F}$ | $^\circ\text{C} = (^\circ\text{F} - 32) \times 5/9$. |
| **Humidity** | Relative humidity ($RH$) | $\%$ | Direct percentage ($0–100\%$). |
| **pH** | $1:2.5$ soil-water suspension | Dimensionless | Standard scale ($0–14$). |
| **Rainfall** | Seasonal/annual meteorological gauge | $\text{mm}$ or $\text{inches}$ | $1\text{ inch} = 25.4\text{ mm}$. Must represent monthly/cycle precipitation, not annual total. |

---

## 6. OUT-OF-DISTRIBUTION (OOD) PROBLEM & EXTRAPOLATION RISK

### What Happens When a Farmer Enters $N = 600$ (Standard High-N Soil Test)?
1. **Frontend:** $600 \ge 0$, passes empty check, form submits.
2. **Backend:** `n = int(request.form["Nitrogen"])` -> `600`.
3. **Scaler:** $\text{scaled\_N} = (600 - 0) / 140 = 4.2857$ *(outside normal $[0, 1]$ training interval)*.
4. **Model:** Random Forest decision splits evaluate $x_i \le \theta$. Since $4.2857 > \theta_{\max}$, it traverses the outermost right path and lands in an arbitrary leaf.
5. **Output:** The application returns a **$100\%$ confident prediction** (e.g. "coffee" or "cotton") without any warning that the input was $4.3\times$ higher than the dataset maximum.

### Risk Summary:
- **Decision Tree Saturation:** Trees cannot extrapolate slopes; any extreme input acts like an edge value.
- **Crop Failure Liability:** Recommending a crop based on unstandardized or saturated values risks catastrophic crop loss for a farmer.

---

## 7. FINAL VERIFICATION STATEMENT AUDIT

| # | Statement | Verdict | Evidence / Code Location | What is Wrong | Recommended Fix |
|---|---|---|---|---|---|
| **1** | The model uses N, P, K, temperature, humidity, pH, and rainfall. | **TRUE** | `Crop recommendation system.ipynb` & `app.py:54` | Correctly configured. | None required. |
| **2** | N/P/K are obtained from soil testing. | **TRUE** | Agronomic domain standard | True in concept, but project fails to specify testing unit or form. | Add explicit unit labels ($\text{kg/ha}$ or $\text{ppm}$) and nutrient form ($P$ vs $P_2O_5$, $K$ vs $K_2O$). |
| **3** | pH is obtained from soil testing. | **TRUE** | `templates/index.html:588` | Standard dimensionless soil test measurement. | None required. |
| **4** | Temperature can come from environmental/weather data. | **TRUE** | `templates/index.html:573` | Standard ambient measurement. | Clarify average growing-season metric. |
| **5** | Humidity can come from environmental/weather data. | **TRUE** | `templates/index.html:581` | Standard relative humidity percentage. | None required. |
| **6** | Rainfall can come from environmental/weather data. | **TRUE** | `templates/index.html:594` | Standard precipitation depth. | **Crucial:** Clarify if rainfall is monthly or seasonal total. |
| **7** | My current UI accepts the correct units. | **FALSE** | `templates/index.html:553-568`, `translations.py:10-15` | N, P, and K have **no units** in labels or placeholders; rainfall duration is undefined. | Update labels/placeholders with explicit units (e.g., $N\text{ [kg/ha]}$, $\text{Rainfall [mm/month]}$). |
| **8** | My current UI has proper validation. | **FALSE** | `templates/index.html:554-596, 660-671` | No upper bound (`max`) constraints; allows nonsensical inputs ($\text{pH}=99$, $\text{Humidity}=500\%$, $\text{Temp}=500$). | Implement realistic agricultural range checks in both frontend and backend. |
| **9** | My current model can safely handle real-world values outside the dataset range. | **FALSE** | `minmaxscaler.pkl` & `app.py:55-57` | Random Forest saturates at leaf thresholds for OOD inputs; scaler generates values far outside $[0, 1]$. | Add anomaly/OOD detection or strict clamp/validation bounds before inference. |
| **10** | My current system is ready for general farmer usage. | **FALSE** | `app.py:46-52`, `templates/index.html` | Unit ambiguity, absence of seasonal rainfall context, lack of input boundary validation, and uncalibrated point predictions make it unsafe for real deployment. | Implement full validation, define units, provide crop cultivation advice/confidence, and document data collection guidelines. |

---

## 8. MULTI-AGENT BRAINSTORMING & ARCHITECTURAL REVIEW

### Agent 1 — Primary Designer (Lead Auditor)
- **Finding:** The model is highly accurate ($99.32\%$) within its envelope, but fragile against real-world data diversity.
- **Proposal:** Standardize the input pipeline using a 5-stage architecture:
  $$\text{Soil Report Input} \to \text{Unit/Form Normalizer} \to \text{Agronomic Validator} \to \text{MinMaxScaler} \to \text{Random Forest}$$

### Agent 2 — Skeptic / Challenger
- **Challenge:** *"Why shouldn't we just retrain the model on Indian Soil Health Card data?"*
- **Resolution:** Retraining requires multi-regional agro-climatic datasets with multi-year yield data across all 22 crops. The immediate, non-breaking solution is to establish $\text{kg/ha}$ (elemental $N$, $P$, $K$) as AgriSense's documented input convention and provide clear unit conversion tooling.

### Agent 3 — Constraint Guardian
- **Enforcement:** Decision trees cannot extrapolate. Any input where $\text{scaled\_feature} \notin [0, 1]$ must either trigger a validation error or an explicit out-of-bounds warning.

### Agent 4 — User Advocate
- **Enforcement:** Farmers should not have to manually convert $P_2O_5$ to elemental $P$ or $K_2O$ to elemental $K$. The UI should offer intuitive unit selectors or clear helper tooltips with standard defaults.

### Agent 5 — Integrator / Arbiter
- **Final Disposition:** **APPROVED FOR AUDIT & STANDARDIZATION ROADMAP**. The model itself remains intact; the input contract, validation layer, and UI labeling must be upgraded.

---

## 9. CONCRETE ACTION PLAN & CODE RECOMMENDATIONS

### A. Recommended Frontend Labels (`translations.py` & `templates/index.html`)

| Parameter | Current Label / Placeholder | Recommended Label | Recommended Placeholder |
|---|---|---|---|
| **Nitrogen** | `Nitrogen` / `Enter Nitrogen` | `Nitrogen (N) [kg/ha]` | `e.g. 50 (0–140 kg/ha)` |
| **Phosphorus** | `Phosphorus` / `Enter Phosphorus` | `Phosphorus (P) [kg/ha]` | `e.g. 50 (5–145 kg/ha)` |
| **Potassium** | `Potassium` / `Enter Potassium` | `Potassium (K) [kg/ha]` | `e.g. 50 (5–205 kg/ha)` |
| **Temperature** | `Temperature` / `Enter Temperature (°C)` | `Temperature (°C)` | `e.g. 25.5 (9–44 °C)` |
| **Humidity** | `Humidity` / `Enter Humidity (%)` | `Relative Humidity (%)` | `e.g. 70 (15–100 %)` |
| **pH** | `pH Level` / `Enter pH Value` | `Soil pH (0–14)` | `e.g. 6.5 (3.5–9.5)` |
| **Rainfall** | `Rainfall` / `Enter Rainfall (mm)` | `Monthly Rainfall (mm)` | `e.g. 100 (20–300 mm)` |

---

### B. Recommended Backend Validation Layer (`app.py`)

Add a clean, lightweight validation dictionary in `app.py`:

```python
# ponytail: strict agricultural validation bounds matching model distribution
VALIDATION_BOUNDS = {
    "Nitrogen": {"min": 0, "max": 140, "unit": "kg/ha"},
    "Phosphorus": {"min": 5, "max": 145, "unit": "kg/ha"},
    "Potassium": {"min": 5, "max": 205, "unit": "kg/ha"},
    "Temperature": {"min": 8.0, "max": 45.0, "unit": "°C"},
    "Humidity": {"min": 14.0, "max": 100.0, "unit": "%"},
    "Ph": {"min": 3.5, "max": 10.0, "unit": "pH"},
    "Rainfall": {"min": 20.0, "max": 300.0, "unit": "mm"}
}

def validate_crop_inputs(data):
    errors = {}
    for field, bounds in VALIDATION_BOUNDS.items():
        val = data.get(field)
        if val is None or val < bounds["min"] or val > bounds["max"]:
            errors[field] = f"Please enter {field} between {bounds['min']} and {bounds['max']} {bounds['unit']}."
    return errors
```

---

### C. Standard Conversion Layer for Soil Health Cards

If supporting direct laboratory report inputs:

1. **Phosphate to Elemental Phosphorus:**
   $$P = P_2O_5 \times 0.4364$$
2. **Potash to Elemental Potassium:**
   $$K = K_2O \times 0.8302$$
3. **$\text{ppm} / \text{mg/kg}$ to $\text{kg/ha}$ (Standard furrow slice, $15\text{ cm}$ depth, $\rho = 1.33\text{ g/cm}^3$):**
   $$\text{kg/ha} = \text{ppm} \times 2.24$$
4. **Acres to Hectares:**
   $$\text{kg/ha} = \text{kg/acre} \times 2.471$$

---

### D. Model Retraining Verdict

- **Core Random Forest Model:** **DO NOT RETRAIN**. The current classifier has $99.32\%$ test accuracy and $99.45\%$ 5-fold cross-validation accuracy.
- **Production Readiness Strategy:** Keep the trained model and scaler intact; standardize and guard the input boundary layer through UI labeling, helper tooltips, and server-side range validation.
