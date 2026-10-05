# 🌿 AgriSense — AI-Powered Crop Recommendation System

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9.0-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Multilingual](https://img.shields.io/badge/Languages-12_Regional-16a34a?style=for-the-badge)

**AgriSense** is an intelligent, multilingual agricultural decision support platform. It empowers farmers, agronomists, and agricultural researchers to predict the optimal crop for cultivation based on soil nutrient profiles ($N, P, K$), climate parameters (Temperature, Humidity, Rainfall), and Soil pH levels.

---

## ✨ Key Features

- 🧠 **Machine Learning Engine**: Trained using Ensemble Machine Learning algorithms (`RandomForestClassifier`, `DecisionTreeClassifier`, and `MinMaxScaler`) to provide high-precision crop recommendations across 22 major crop categories.
- 🌐 **12 Regional & International Languages**: Complete end-to-end localization support for:
  - English (`en`), Hindi (`hi`), Telugu (`te`), Tamil (`ta`), Kannada (`kn`), Marathi (`mr`), Bengali (`bn`), Gujarati (`gu`), Malayalam (`ml`), Punjabi (`pa`), Odia (`or`), Urdu (`ur`).
- 🔊 **Voice Speech Synthesis (Edge-TTS)**: Automatically generates natural spoken audio recommendations in local regional voices for enhanced accessibility.
- 📐 **Embedded Unit Selectors & Real-Time Math Conversion**: Supports 15 agricultural unit formats across input fields, automatically standardizing custom units (e.g., $kg/acre$, $ppm$, $P_2O_5$, $K_2O$, $^{\circ}F$, $mm/year$) before machine learning inference.
- 🎛️ **Interactive Stepper Controls**: Contextual up/down stepper arrows (`▲▼`) that appear on input focus or data fill, supporting precise numeric stepping.
- 🛡️ **Agricultural Validation Envelope**: Server-side and client-side bounds checking localized per language to prevent out-of-range lab data entries.
- 🎨 **Modern Responsive UI**: Clean card-based design system with `#ffffff` input boxes, glassmorphic hover feedback, custom dropdown controls, and z-index dropdown layering.

---

## 🔄 Supported Agricultural Unit Conversions

AgriSense allows farmers to input data in their local lab test units. All non-metric inputs are converted into standard metric units before executing ML prediction:

| Parameter | Default Base Unit | Supported Custom Units | Conversion Math |
| :--- | :--- | :--- | :--- |
| **Nitrogen ($N$)** | `kg/ha` | `kg/acre`, `ppm` | $\text{kg/acre} \times 2.471$, $\text{ppm} \times 2.24$ |
| **Phosphorus ($P$)** | `kg/ha (P)` | `kg/ha (P₂O₅)`, `ppm`, `kg/acre` | $\text{P}_2\text{O}_5 \times 0.4364$, $\text{ppm} \times 2.24$, $\text{kg/acre} \times 2.471$ |
| **Potassium ($K$)** | `kg/ha (K)` | `kg/ha (K₂O)`, `ppm`, `kg/acre` | $\text{K}_2\text{O} \times 0.8302$, $\text{ppm} \times 2.24$, $\text{kg/acre} \times 2.471$ |
| **Temperature** | $^{\circ}\text{C}$ | $^{\circ}\text{F}$ | $({^{\circ}\text{F}} - 32) \times \frac{5}{9}$ |
| **Humidity** | $\%$ | $-$ | Standard Percentage |
| **Soil pH** | $\text{pH}$ | $-$ | Standard pH Scale ($3.5 - 10.0$) |
| **Rainfall** | `mm/month` | `mm/year` | $\text{Annual Rainfall} \div 12$ |

---

## 📊 Agricultural Training Bounds Envelope

| Input Field | Minimum Bound | Maximum Bound | Standard Unit |
| :--- | :--- | :--- | :--- |
| **Nitrogen ($N$)** | `0.0` | `140.0` | `kg/ha` |
| **Phosphorus ($P$)** | `5.0` | `145.0` | `kg/ha` |
| **Potassium ($K$)** | `5.0` | `205.0` | `kg/ha` |
| **Temperature** | `8.0` | `44.0` | $^{\circ}\text{C}$ |
| **Humidity** | `0.0` | `100.0` | $\%$ |
| **Soil pH** | `3.5` | `10.0` | $\text{pH}$ |
| **Rainfall** | `20.0` | `300.0` | `mm/month` |

---

## 📁 Project Architecture & Directory Structure

```
crop-recommendation-system ui updated/
├── app.py                   # Main Flask application & ML inference pipeline
├── translations.py          # Multilingual dictionary (12 languages)
├── model.pkl                # Pre-trained Ensemble ML Classifier
├── minmaxscaler.pkl         # Feature Scaling Model
├── requirements.txt         # Project Python dependencies
├── static/                  # Static assets & generated media
│   ├── Hero_img.webp        # Hero section graphic asset
│   ├── Hero_img2.ico        # Browser tab favicon
│   ├── nav emoji.webp       # Brand navbar badge
│   ├── tts/                 # Cached TTS clips, one per language+crop (generated, git-ignored)
│   └── [crop images].webp   # Crop visual recommendation badges
└── templates/
    └── index.html           # Core HTML template, CSS design system, & JS logic
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Clone Repository & Setup Environment
```bash
git clone https://github.com/madhav-kr-singh/Crop-Recommendation-System.git
cd "Crop-Recommendation-System"
```

### 3. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Local Development Server
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5002` (or `http://localhost:5002`).

---

## 🛣️ API & Route Documentation

### `GET /`
- **Query Parameter**: `lang` (optional, default: `en`).
- **Response**: Renders main form in the requested language interface.

### `POST /predict`
- **Query Parameter**: `lang` (optional, default: `en`).
- **Form Data**:
  - `Nitrogen`, `Phosphorus`, `Potassium`, `Temperature`, `Humidity`, `Ph`, `Rainfall`.
  - `unit_Nitrogen`, `unit_Phosphorus`, `unit_Potassium`, `unit_Temperature`, `unit_Rainfall`.
- **Logic**:
  1. Validates input values against agricultural envelope.
  2. Converts custom units into standard metric base format.
  3. Scales features via `minmaxscaler.pkl`.
  4. Runs classifier prediction via `model.pkl`.
  5. Generates TTS speech audio via `edge_tts`.
- **Response**: Renders updated `index.html` displaying the predicted crop card, audio playback control, and localized success feedback.

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome!
1. Fork the project repository.
2. Create your feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'feat: add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for details.
