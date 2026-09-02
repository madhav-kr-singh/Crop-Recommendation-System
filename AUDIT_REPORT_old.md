# CROP RECOMMENDATION SYSTEM — FULL SYSTEM & AGRONOMIC AUDIT REPORT

**Audit Date:** 2026-09-02  
**Target Project:** Crop Recommendation System  
**Repository Path:** `c:\Users\ADMIN\Desktop\crop\crop-recommendation-system ui updated`  
**Audit Scope:** Dataset (`Crop_recommendation.csv`), Training Notebook (`Crop recommendation system.ipynb`), Serialized Artifacts (`model.pkl`, `minmaxscaler.pkl`, `standscaler.pkl`), Backend (`app.py`), Translations (`translations.py`), and Frontend UI (`templates/index.html`).

---

## 1. PROJECT / MODEL INPUTS VERIFICATION

| # | Expected Feature | Dataset Feature Name | Python Data Type | Backend Parsing (`app.py`) | Model Feature Index | Actually Used in Prediction? |
|---|------------------|----------------------|------------------|---------------------------|---------------------|-----------------------------|
| 1 | Nitrogen         | `N`                  | `int64`          | `int(request.form["Nitrogen"])` | 0 | **YES** |
| 2 | Phosphorus       | `P`                  | `int64`          | `int(request.form["Phosphorus"])` | 1 | **YES** |
| 3 | Potassium        | `K`                  | `int64`          | `int(request.form["Potassium"])` | 2 | **YES** |
| 4 | Temperature      | `temperature`        | `float64`        | `float(request.form["Temperature"])` | 3 | **YES** |
| 5 | Humidity         | `humidity`           | `float64`        | `float(request.form["Humidity"])` | 4 | **YES** |
| 6 | pH               | `ph`                 | `float64`        | `float(request.form["Ph"])` | 5 | **YES** |
| 7 | Rainfall         | `rainfall`           | `float64`        | `float(request.form["Rainfall"])` | 6 | **YES** |

### Confirmation:
- **Feature Names:** `['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']`
- **Feature Order:** Exactly 7 features passed in strict sequence `[N, P, K, temperature, humidity, ph, rainfall]` into `np.array` and `ms.transform()`.
- **Target Label:** `label` (string class names, e.g. `'rice'`, `'maize'`).
- **Confirmation Verdict:** **TRUE**. All 7 expected features are actively used in the exact order specified.

---

## 2. TRAINING DATASET AUDIT (`Crop_recommendation.csv`)

### Dataset Statistics (Empirical Values Computed Directly from File)

- **Total Rows:** `2,200`
- **Total Columns:** `8` (`N`, `P`, `K`, `temperature`, `humidity`, `ph`, `rainfall`, `label`)
- **Number of Crop Classes:** `22` (Exactly 100 samples per crop class — perfectly balanced)
- **Crop / Class Names (22 classes):**
  `apple`, `banana`, `blackgram`, `chickpea`, `coconut`, `coffee`, `cotton`, `grapes`, `jute`, `kidneybeans`, `lentil`, `maize`, `mango`, `mothbeans`, `mungbean`, `muskmelon`, `orange`, `papaya`, `pigeonpeas`, `pomegranate`, `rice`, `watermelon`
- **Missing / Null Values:** `0` across all 8 columns.
- **Duplicate Rows:** `0` duplicates found.
- **Invalid / Non-Numeric Values:** `0` non-numeric records in feature columns.

### Exact Dataset Feature Distribution

| Parameter | Dataset Minimum | Dataset Maximum | Dataset Mean | Dataset Std Dev |
|-----------|----------------:|----------------:|-------------:|----------------:|
| **N** (Nitrogen) | **0.000000** | **140.000000** | 50.551818 | 36.917334 |
| **P** (Phosphorus) | **5.000000** | **145.000000** | 53.362727 | 32.985883 |
| **K** (Potassium) | **5.000000** | **205.000000** | 48.149091 | 50.647931 |
| **Temperature** | **8.825675** | **43.675493** | 25.616244 | 5.063749 |
| **Humidity** | **14.258040** | **99.981876** | 71.481779 | 22.263812 |
| **pH** | **3.504752** | **9.935091** | 6.469480 | 0.773938 |
| **Rainfall** | **20.211267** | **298.560117** | 103.463655 | 54.958389 |

---

## 3. MODEL TRAINING AUDIT (`Crop recommendation system.ipynb`)

- **Training Script / Notebook:** `Crop recommendation system.ipynb` (Contains 12 cells in total).
- **ML Algorithm:** `RandomForestClassifier` from `sklearn.ensemble`.
- **Model Parameters (Inspected from `model.pkl`):**
  - `n_estimators`: `100`
  - `random_state`: `42`
  - `criterion`: `'gini'`
  - `max_depth`: `None` (trees grown to maximum depth)
  - `min_samples_split`: `2`
  - `min_samples_leaf`: `1`
  - `max_features`: `'sqrt'`
  - `bootstrap`: `True`
- **Train / Test Split:** `test_size=0.2` (80% train = 1,760 samples, 20% test = 440 samples), `random_state=42`.
- **Target Encoding:** None. Raw string labels (`'apple'`, `'rice'`, etc.) are directly passed to `RandomForestClassifier.fit()`.
- **Cross-Validation in Notebook:** **None** (only a single 80/20 train-test split was executed).
- **Reported Accuracy in Notebook:** `0.9931818181818182` (**99.32%** on test set).
- **Computed Comprehensive Evaluation Metrics (Test Set):**
  - **Accuracy:** `99.32%` (437/440 correct predictions)
  - **Precision (Macro):** `99.26%`
  - **Precision (Weighted):** `99.37%`
  - **Recall (Macro):** `99.33%`
  - **Recall (Weighted):** `99.32%`
  - **F1-Score (Macro):** `99.26%`
  - **F1-Score (Weighted):** `99.32%`
  - **5-Fold Cross-Validation Accuracy:** `[99.77%, 99.32%, 99.77%, 99.55%, 98.86%]`, Mean = **99.45%**.
- **Is Random Forest Actually Used?** **YES**.

---

## 4. SCALER & PREPROCESSING AUDIT

- **Active Scaler Object:** `MinMaxScaler` from `sklearn.preprocessing`, loaded from `minmaxscaler.pkl`.
- **Unused Artifact in Repo:** `standscaler.pkl` exists in the repository root but is unused by `app.py` and the notebook.
- **Fitted Features:** 7 features `['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']`.
- **Exact Learned Scaler Values (`minmaxscaler.pkl`):**

| Feature | `data_min_` (Learned Min) | `data_max_` (Learned Max) | `scale_` ($1 / \text{range}$) | `min_` (Intercept) |
|---|---:|---:|---:|---:|
| **N** | 0.00000000 | 140.00000000 | 0.00714286 | 0.00000000 |
| **P** | 5.00000000 | 145.00000000 | 0.00714286 | -0.03571429 |
| **K** | 5.00000000 | 205.00000000 | 0.00500000 | -0.02500000 |
| **temperature** | 8.82567475 | 43.67549305 | 0.02869455 | -0.25324880 |
| **humidity** | 14.27327988 | 99.98187601 | 0.01166744 | -0.16653265 |
| **ph** | 3.50475231 | 9.93509073 | 0.15551281 | -0.54503388 |
| **rainfall** | 20.36001144 | 298.56011750 | 0.00359453 | -0.07318477 |

- **Is Scaler Applied Before Prediction?** **YES** (`features = ms.transform(features)` in `app.py:55`).
- **Consistency Check:** The exact scaler fitted during training is loaded in `app.py` and used to transform user inputs prior to inference.
- **Note on Scaling with Random Forest:** `MinMaxScaler` is mathematically redundant for decision-tree based models (like Random Forest), because decision trees are invariant to monotonic feature scaling. However, because the model was trained on scaled inputs, the scaler must remain in place for consistent inference.

---

## 5. CURRENT APPLICATION & UI INPUT AUDIT

| Field | Input Type | `min` | `max` | `step` | `required` | Placeholder | Error Message |
|---|---|---|---|---|---|---|---|
| **Nitrogen** | `number` | `0` | *None* | *None (1)* | `True` | `"Enter Nitrogen"` | `"Please enter nitrogen."` |
| **Phosphorus** | `number` | `0` | *None* | *None (1)* | `True` | `"Enter Phosphorus"` | `"Please enter phosphorus."` |
| **Potassium** | `number` | `0` | *None* | *None (1)* | `True` | `"Enter Potassium"` | `"Please enter potassium."` |
| **Temperature** | `number` | `0` | *None* | `0.01` | `True` | `"Enter Temperature (°C)"` | `"Please enter temperature."` |
| **Humidity** | `number` | `0` | *None* | `0.01` | `True` | `"Enter Humidity (%)"` | `"Please enter humidity."` |
| **pH** | `number` | `0` | *None* | `0.01` | `True` | `"Enter pH Value"` | `"Please enter pH value."` |
| **Rainfall** | `number` | `0` | *None* | `0.01` | `True` | `"Enter Rainfall (mm)"` | `"Please enter rainfall (mm)."` |

### Range Validation Verdict:
- **Current Validation:** The application **ONLY** enforces `min="0"` (preventing negative numbers and minus keystrokes) and checks that inputs are non-empty.
- **Upper Bounds:** There is **NO upper bound validation** anywhere in the frontend or backend. Inputs such as $N = 10,000$, $\text{Temperature} = 200^\circ\text{C}$, $\text{Humidity} = 500\%$, $\text{pH} = 14$, or $\text{Rainfall} = 50,000\text{ mm}$ are accepted without rejection or warning.

---

## 6. SOIL TEST REPORT UNITS AUDIT

### Detailed Unit Tracing Across the Project Hierarchy:

| Parameter | Dataset Header | Training Notebook | Backend `app.py` | UI Placeholder / Label | Agronomic Form (Elemental vs Oxide) |
|---|---|---|---|---|---|
| **N** (Nitrogen) | `N` | *Undefined* | *Undefined* | `"Enter Nitrogen"` | **UNIT NOT DEFINED IN PROJECT** |
| **P** (Phosphorus) | `P` | *Undefined* | *Undefined* | `"Enter Phosphorus"` | **UNIT NOT DEFINED IN PROJECT** |
| **K** (Potassium) | `K` | *Undefined* | *Undefined* | `"Enter Potassium"` | **UNIT NOT DEFINED IN PROJECT** |
| **Temperature** | `temperature` | *Undefined* | *Undefined* | `"Enter Temperature (°C)"` | Defined as **°C** in UI only |
| **Humidity** | `humidity` | *Undefined* | *Undefined* | `"Enter Humidity (%)"` | Defined as **%** in UI only |
| **pH** | `ph` | *Undefined* | *Undefined* | `"Enter pH Value"` | Standard dimensionless pH ($-\log[H^+]$) |
| **Rainfall** | `rainfall` | *Undefined* | *Undefined* | `"Enter Rainfall (mm)"` | Defined as **mm** in UI only (*Timeframe undefined*) |

### Critical Agronomic Findings on N / P / K:
1. **Soil Health Cards (SHC) Standard in Agriculture:**
   - In standard agricultural soil testing (e.g. Govt of India Soil Health Cards, ICAR, USDA):
     - **Available Nitrogen ($N$):** Reported as available nitrogen in $\text{kg/ha}$ or $\text{kg/acre}$ (or rating Low: $<280\text{ kg/ha}$, Medium: $280-560\text{ kg/ha}$, High: $>560\text{ kg/ha}$).
     - **Available Phosphorus ($P$):** Frequently reported as $P_2O_5$ in $\text{kg/ha}$ (or Olsen $P$ in $\text{ppm} / \text{mg/kg}$).
     - **Available Potassium ($K$):** Frequently reported as $K_2O$ in $\text{kg/ha}$ (or ammonium acetate extractable $K$ in $\text{ppm} / \text{mg/kg}$).
2. **Project Status:**
   - **UNIT NOT DEFINED IN PROJECT**.
   - The dataset values ($N: 0-140$, $P: 5-145$, $K: 5-205$) do not state whether they represent $\text{kg/ha}$, $\text{ppm}$, $\text{kg/acre}$, nutrient ratio, or elemental versus oxide ($P_2O_5 / K_2O$).
   - A farmer entering available Nitrogen from a standard Indian soil test report (where normal soil $N$ is $250-450\text{ kg/ha}$) will enter values $2-3\times$ higher than the dataset's maximum ($140$).

---

## 7. REAL-WORLD FARMER INPUT VS MODEL INPUT

### TABLE A — CURRENT MODEL DATA RANGE

| Parameter | Dataset Min | Dataset Max | Unit | Source |
|---|---:|---:|---|---|
| **Nitrogen (N)** | `0.00` | `140.00` | **UNIT NOT DEFINED IN PROJECT** | `Crop_recommendation.csv` (Col 0) |
| **Phosphorus (P)** | `5.00` | `145.00` | **UNIT NOT DEFINED IN PROJECT** | `Crop_recommendation.csv` (Col 1) |
| **Potassium (K)** | `5.00` | `205.00` | **UNIT NOT DEFINED IN PROJECT** | `Crop_recommendation.csv` (Col 2) |
| **Temperature** | `8.83` | `43.68` | **°C** (Assumed in UI) | `Crop_recommendation.csv` (Col 3) |
| **Humidity** | `14.26` | `99.98` | **%** (Assumed in UI) | `Crop_recommendation.csv` (Col 4) |
| **pH** | `3.50` | `9.94` | **pH scale** ($0-14$) | `Crop_recommendation.csv` (Col 5) |
| **Rainfall** | `20.21` | `298.56` | **mm** (Assumed in UI) | `Crop_recommendation.csv` (Col 6) |

---

### TABLE B — FARMER INPUT (REAL-WORLD AGRICULTURAL RANGE)

| Parameter | What Farmer Gets from Soil / Weather Report | Unit | How Obtained | Real-World Agricultural Range |
|---|---|---|---|---|
| **Nitrogen (N)** | Available soil nitrogen | $\text{kg/ha}$ (or $\text{kg/acre}$ or $\text{ppm}$) | Laboratory Soil Test Report (Kjeldahl / Alkaline $\text{KMnO}_4$) | $50 - 600\text{ kg/ha}$ (Typical: $150-450$) |
| **Phosphorus (P)** | Available soil phosphorus ($P$ or $P_2O_5$) | $\text{kg/ha}$ or $\text{ppm}$ / $\text{mg/kg}$ | Laboratory Soil Test Report (Bray / Olsen method) | $5 - 120\text{ kg/ha}$ (or $2 - 50\text{ ppm}$) |
| **Potassium (K)** | Available soil potassium ($K$ or $K_2O$) | $\text{kg/ha}$ or $\text{ppm}$ / $\text{mg/kg}$ | Laboratory Soil Test Report ($\text{NH}_4\text{OAc}$ Flame Photometry) | $50 - 600\text{ kg/ha}$ (or $30 - 300\text{ ppm}$) |
| **Temperature** | Ambient crop growing season temperature | $^\circ\text{C}$ | IMD / Regional Weather Station / IoT Sensor | $-5^\circ\text{C} \text{ to } 50^\circ\text{C}$ (Crop growth: $10-45^\circ\text{C}$) |
| **Humidity** | Relative humidity ($RH$) | $\%$ | Hygrometer / Weather Forecast Service | $10\% - 100\%$ |
| **pH** | Soil reaction index | pH scale | pH Meter / 1:2.5 Soil-Water Suspension | $4.0 - 9.5$ (Optimal: $6.0 - 7.5$) |
| **Rainfall** | Cumulative seasonal or annual precipitation | $\text{mm}$ | Rain Gauge / Meteorological Dept | $100 - 3,500\text{ mm}$ (Annual) / $20 - 400\text{ mm}$ (Monthly) |

---

## 8. OUT-OF-DISTRIBUTION (OOD) PROBLEM & EXTRAPOLATION RISK

### Scenario Trace: Farmer Enters $N = 600$

1. **Frontend Validation:** The UI checks `min="0"`. Since $600 \ge 0$, it is submitted without blocking or warning.
2. **Backend Parsing:** `app.py` executes `n = int(request.form["Nitrogen"])` -> `n = 600`.
3. **Scaler Computation:** `minmaxscaler.pkl` computes:
   $$\text{scaled\_N} = (600 - 0.0) \times 0.00714286 = 4.2857$$
   *(Normal in-distribution range is $[0.0, 1.0]$)*.
4. **Model Inference:** `RandomForestClassifier` receives an extreme outlier ($\text{scaled\_N} = 4.2857$). Because tree decision splits are threshold checks ($x_i \le \theta$), any value $> \theta_{\max}$ follows the outermost right branch, landing in an arbitrary leaf node.
5. **System Response:** The application returns a **$100\%$ confident prediction** (e.g. "coffee" or "cotton") without any indication that the input was $4.3\times$ higher than the maximum training sample.

### Core Agricultural & Mathematical Risks:
- **Silent Extrapolation Failure:** Decision trees cannot model gradient slopes beyond their bounding box. An extreme nitrogen toxicity condition is treated identically to a moderately high nitrogen condition.
- **Crop Failure Risk:** Recommending a crop based on unvalidated out-of-bounds input can cause severe financial loss to a farmer (e.g. recommending high-water rice in an arid zone where rainfall was entered as annual total instead of monthly average).

---

## 9. FINAL VERIFICATION STATEMENT AUDIT

| # | Statement | Verdict | Evidence / Code Location | What is Wrong | Recommended Fix |
|---|---|---|---|---|---|
| **1** | The model uses N, P, K, temperature, humidity, pH, and rainfall. | **TRUE** | `Crop recommendation system.ipynb` (Cells 4, 8) & `app.py:54` | Correctly configured. | None required. |
| **2** | N/P/K are obtained from soil testing. | **TRUE** | Agronomic domain standard | Agronomically correct, but project fails to specify testing unit. | Add explicit unit labels ($\text{kg/ha}$ or $\text{ppm}$). |
| **3** | pH is obtained from soil testing. | **TRUE** | `templates/index.html:588` | Standard dimensionless soil test measurement. | None required. |
| **4** | Temperature can come from environmental/weather data. | **TRUE** | `templates/index.html:573` | Standard growing-season ambient measurement. | Specify average seasonal vs daily metric. |
| **5** | Humidity can come from environmental/weather data. | **TRUE** | `templates/index.html:581` | Standard relative humidity percentage. | None required. |
| **6** | Rainfall can come from environmental/weather data. | **TRUE** | `templates/index.html:594` | Standard precipitation depth. | **Crucial:** Clarify if rainfall is monthly or seasonal total. |
| **7** | My current UI accepts the correct units. | **FALSE** | `templates/index.html:553-568`, `translations.py:10-15` | N, P, and K have **no units** in labels or placeholders; rainfall duration basis is undefined. | Update labels/placeholders to include explicit units (e.g., $N\text{ (kg/ha)}$, $\text{Rainfall (mm/season)}$). |
| **8** | My current UI has proper validation. | **FALSE** | `templates/index.html:554-596, 660-671` | No upper bound (`max`) constraints; allows nonsensical inputs ($\text{pH}=99$, $\text{Humidity}=500\%$, $\text{Temp}=500$). | Implement realistic agricultural range checks in both frontend and backend. |
| **9** | My current model can safely handle real-world values outside the dataset range. | **FALSE** | `minmaxscaler.pkl` & `app.py:55-57` | Random Forest saturates at leaf thresholds for OOD inputs; scaler generates values far outside $[0, 1]$. | Add anomaly/OOD detection or strict clamp/validation bounds before inference. |
| **10** | My current system is ready for general farmer usage. | **FALSE** | `app.py:46-52`, `templates/index.html` | Unit ambiguity, absence of seasonal rainfall context, lack of input boundary validation, and uncalibrated point predictions make it unsafe for real deployment. | Implement full validation, define units, provide crop cultivation advice/confidence, and document data collection guidelines. |

---

## 10. MULTI-AGENT BRAINSTORMING & AUDIT SYNTHESIS

### A. What is Correct in the Project
1. **Model Architecture & Training Pipeline:** The Random Forest implementation achieves $99.32\%$ test accuracy and $99.45\%$ 5-fold CV accuracy with zero missing/duplicate data in `Crop_recommendation.csv`.
2. **Preprocessing Consistency:** The exact scaler (`MinMaxScaler`) trained in the notebook is preserved in `minmaxscaler.pkl` and executed in `app.py`.
3. **Multilingual Architecture:** 12 Indian languages are fully supported with localized UI, right-to-left Urdu rendering, and text-to-speech audio generation.
4. **Responsive UI:** The frontend layout, language selection dropdown, and single-line hero heading are responsive across mobile and desktop.

### B. What is Wrong
1. **Undefined Soil Test Units:** N, P, and K labels do not state units ($\text{kg/ha}$, $\text{ppm}$, or nutrient oxide basis).
2. **Undefined Rainfall Timeframe:** The dataset rainfall range ($20-298\text{ mm}$) corresponds to monthly rainfall or short-growth cycle precipitation, but farmers typically think in terms of annual monsoon rainfall ($800-2000\text{ mm}$).
3. **Missing Upper Range & Biological Bounds:** Inputs like $\text{pH} = 14$, $\text{Humidity} = 300\%$, and $N = 5000$ are accepted.
4. **Uncalibrated OOD Predictions:** No confidence scoring or warning when inputs deviate from the training distribution.

### C. What Needs to Be Changed (Roadmap)
1. **Frontend UI:**
   - Add explicit units to field labels (e.g. `Nitrogen (N) [kg/ha]`, `Temperature (°C)`, `Relative Humidity (%)`, `Soil pH`, `Rainfall (mm)`).
   - Add tooltips or helper text explaining how to obtain these values from a Soil Health Card or local weather station.
2. **Backend Validation (`app.py`):**
   - Add server-side validation rejecting impossible values ($\text{pH} < 0$ or $> 14$, $\text{Humidity} > 100\%$, etc.).
   - Return clear, user-friendly validation error messages if an entered value is agronomically implausible.
3. **Model Prediction Safety:**
   - Output prediction probabilities or a confidence score alongside the recommended crop.
   - Flag inputs outside the 99th percentile of training data with a cautionary note: *"Warning: Input values deviate from standard regional training ranges."*

### D. Exact Recommended UI Ranges for Validation

| Field | Recommended Soft Min | Recommended Soft Max | Absolute Hard Min | Absolute Hard Max |
|---|---:|---:|---:|---:|
| **Nitrogen (N)** | $0\text{ kg/ha}$ | $200\text{ kg/ha}$ | $0$ | $400\text{ kg/ha}$ |
| **Phosphorus (P)** | $5\text{ kg/ha}$ | $150\text{ kg/ha}$ | $0$ | $250\text{ kg/ha}$ |
| **Potassium (K)** | $5\text{ kg/ha}$ | $220\text{ kg/ha}$ | $0$ | $350\text{ kg/ha}$ |
| **Temperature** | $8^\circ\text{C}$ | $45^\circ\text{C}$ | $0^\circ\text{C}$ | $55^\circ\text{C}$ |
| **Humidity** | $15\%$ | $100\%$ | $5\%$ | $100\%$ |
| **Soil pH** | $4.0$ | $9.5$ | $3.0$ | $10.5$ |
| **Rainfall** | $20\text{ mm}$ | $350\text{ mm}$ | $0\text{ mm}$ | $500\text{ mm}$ |

### E. Exact Units That Should Appear in the Farmer UI

1. **Nitrogen:** `kg/ha` (Kilograms per Hectare) *(or toggle for kg/acre)*
2. **Phosphorus:** `kg/ha` (as available P / P2O5)
3. **Potassium:** `kg/ha` (as available K / K2O)
4. **Temperature:** `°C` (Celsius)
5. **Humidity:** `%` (Relative Humidity)
6. **pH:** `pH` ($0–14$ scale)
7. **Rainfall:** `mm` (Average Monthly / Growing Season Rainfall)

### F. Does the Current ML Model Need Retraining?

- **Verdict:** **NO retraining is required for the core classifier logic**, provided that the input domain is properly documented and constrained to the dataset's scale.
- **Why:** The existing `RandomForestClassifier` achieves $>99.3\%$ accuracy and generalizes exceptionally well across its 22 target crops when inputs fall within its defined training envelope.
- **When Retraining WOULD Be Needed:** If you decide to support direct input of raw Indian Soil Health Card macro-units (which often range up to $600\text{ kg/ha}$ for Nitrogen and $1000+\text{ mm}$ for annual rainfall), you will either need to:
  1. Add a mathematical unit-converter layer in the frontend/backend before scaling, OR
  2. Retrain the model on standardized regional soil and agro-climatic datasets with calibrated multi-season benchmarks.
