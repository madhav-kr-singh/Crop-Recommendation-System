
# AgriSense — Input Contract Fix

## Goal

Fix the broken input contract: add `kg/ha` units to N/P/K labels, `mm/month` to rainfall, upper-bound `max` on all HTML inputs, and server-side validation that blocks OOD values before `model.predict()`.
**Model, scaler, and training notebook untouched.**

---

## Tasks

- [ ] **Task 1 — `app.py`: Add `VALIDATION_BOUNDS` + `validate_inputs()` + wire into `/predict`**Insert after line 12 (after scaler load). Call `validate_inputs()` at top of `predict()` before `ms.transform()`. Return 400 with field errors on failure.→ Verify: `curl -X POST http://localhost:5002/predict -d "Nitrogen=600&..."` returns 400 with error message.
- [ ] **Task 2 — `translations.py` English block (lines 10–23): Update N/P/K labels + all placeholders**

  - `"nitrogen"` → `"Nitrogen (N) [kg/ha]"`
  - `"enter_nitrogen"` → `"e.g. 50  (0–140 kg/ha)"`
  - `"phosphorus"` → `"Phosphorus (P) [kg/ha]"`
  - `"enter_phosphorus"` → `"e.g. 50  (5–145 kg/ha)"`
  - `"potassium"` → `"Potassium (K) [kg/ha]"`
  - `"enter_potassium"` → `"e.g. 50  (5–205 kg/ha)"`
  - `"enter_temperature"` → `"e.g. 25.5  (9–44 °C)"`
  - `"enter_humidity"` → `"e.g. 70  (15–100 %)"`
  - `"enter_ph"` → `"e.g. 6.5  (3.5–9.5)"`
  - `"enter_rainfall"` → `"e.g. 100  (20–300 mm/month)"`
  - `"rainfall"` → `"Monthly Rainfall (mm)"`
    → Verify: Reload `http://localhost:5002` — English placeholders show ranges with units.
- [ ] **Task 3 — `translations.py` all 11 other language blocks: update N/P/K unit suffix + rainfall key**For each language (`hi`, `te`, `ta`, `kn`, `mr`, `bn`, `gu`, `ml`, `pa`, `or`, `ur`):

  - Append `[kg/ha]` to the `nitrogen`, `phosphorus`, `potassium` label values
  - Update `enter_nitrogen/phosphorus/potassium` to include `(0–140 kg/ha)` etc.
  - Update `enter_rainfall` to `(20–300 mm/month)`
    → Verify: Switch to Hindi (`?lang=hi`) — N/P/K labels show `[kg/ha]`.
- [ ] **Task 4 — `templates/index.html`: Add `max` + update `min` on all 7 inputs**Find the 7 `<input type="number">` elements and set:

  - Nitrogen: `min="0" max="140"`
  - Phosphorus: `min="5" max="145"`
  - Potassium: `min="5" max="205"`
  - Temperature: `min="8" max="44"`
  - Humidity: `min="14" max="100"`
  - pH: `min="3.5" max="10"`
  - Rainfall: `min="20" max="300"`
    → Verify: In browser, type 999 into Nitrogen — browser native validation rejects it.
- [ ] **Task 5 — Delete `standscaler.pkl` (dead artifact)**`Remove-Item "standscaler.pkl"` in the project root.→ Verify: File no longer appears in `dir`. No import of it exists in `app.py` (confirmed: it doesn't).
- [ ] **Task 6 — Git: commit all changes + push to `main`**

  ```
  git add app.py translations.py templates/index.html
  git commit -m "fix: add input validation, kg/ha units, HTML bounds (AgriSense input contract)"
  git push origin main
  ```

  → Verify: `git log --oneline -1` shows the commit on `main`.

---

## Done When

- [ ] `POST /predict` with `Nitrogen=600` returns HTTP 400 with a human-readable error
- [ ] English UI shows `Nitrogen (N) [kg/ha]` label and `e.g. 50  (0–140 kg/ha)` placeholder
- [ ] All 7 inputs have `max` attributes; browser rejects out-of-range values natively
- [ ] `standscaler.pkl` is deleted
- [ ] Changes are on `origin/main`

---

## Notes

- `ponytail:` no new libraries, no new files, no schema migrations — pure label + validation edits
- Task 3 is repetitive but necessary; do it in one pass with find-and-replace per language block
- Do NOT touch `model.pkl`, `minmaxscaler.pkl`, or the training notebook
- If any language block is missing a `nitrogen`/`phosphorus`/`potassium` key, add it; don't skip
