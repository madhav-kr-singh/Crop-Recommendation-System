from flask import Flask, request, render_template, redirect, url_for
import numpy as np
import pickle
import os
import asyncio
import edge_tts
from translations import t, TRANSLATIONS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = pickle.load(open(os.path.join(BASE_DIR, "model.pkl"), "rb"))
ms = pickle.load(open(os.path.join(BASE_DIR, "minmaxscaler.pkl"), "rb"))

app = Flask(__name__)

VOICES = {
    "en": "en-US-JennyNeural",
    "hi": "hi-IN-SwaraNeural",
    "te": "te-IN-MohanNeural",
    "ta": "ta-IN-PallaviNeural",
    "kn": "kn-IN-GaganNeural",
    "mr": "mr-IN-AarohiNeural",
    "bn": "bn-IN-TanishaaNeural",
    "gu": "gu-IN-DhwaniNeural",
    "ml": "ml-IN-SobhanaNeural",
    "pa": "pa-IN-GurpreetNeural",
    "or": "or-IN-SubhasiniNeural",
    "ur": "ur-IN-GulNeural"
}

async def generate_audio(text, path, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(path)

# ponytail: strict agricultural validation bounds matching model training envelope
VALIDATION_BOUNDS = {
    "Nitrogen":    (0.0,  140.0, "kg/ha"),
    "Phosphorus":  (5.0,  145.0, "kg/ha"),
    "Potassium":   (5.0,  205.0, "kg/ha"),
    "Temperature": (8.0,  44.0,  "°C"),
    "Humidity":    (0.0,  100.0, "%"),
    "Ph":          (3.5,  10.0,  "pH"),
    "Rainfall":    (20.0, 300.0, "mm/month"),
}

def convert_input_value(field, val, unit_type="default"):
    """
    Convert real-world farmer lab inputs / units into model base metric units:
    - P2O5 -> elemental P (x 0.4364)
    - K2O -> elemental K (x 0.8302)
    - ppm (mg/kg) -> kg/ha (x 2.24)
    - kg/acre -> kg/ha (x 2.471)
    - °F -> °C ((°F - 32) * 5/9)
    - inches -> mm (x 25.4)
    - annual rainfall -> monthly average (/ 12)
    """
    u = (unit_type or "").lower().strip()
    if u in ("p2o5",) and field == "Phosphorus":
        val *= 0.4364
    elif u in ("k2o",) and field == "Potassium":
        val *= 0.8302
    elif u in ("ppm", "mg/kg") and field in ("Nitrogen", "Phosphorus", "Potassium"):
        val *= 2.24
    elif u in ("kg/acre", "kg_acre") and field in ("Nitrogen", "Phosphorus", "Potassium"):
        val *= 2.471
    elif u in ("f", "fahrenheit", "°f") and field == "Temperature":
        val = (val - 32.0) * 5.0 / 9.0
    elif u in ("in", "inch", "inches") and field == "Rainfall":
        val *= 25.4
    elif u in ("annual", "yearly") and field == "Rainfall":
        val /= 12.0
    return val

def validate_inputs(form_data):
    errors = {}
    parsed = {}
    for field, (lo, hi, unit) in VALIDATION_BOUNDS.items():
        raw = form_data.get(field, "").strip()
        if not raw:
            errors[field] = f"{field} is required."
            continue
        try:
            val = float(raw)
            unit_type = form_data.get(f"unit_{field}", "default")
            converted_val = convert_input_value(field, val, unit_type)
            if not (lo <= converted_val <= hi):
                errors[field] = f"{field} must be between {lo:g} and {hi:g} {unit}. (Entered: {val:g})"
            else:
                parsed[field] = converted_val
        except ValueError:
            errors[field] = f"Please enter a valid number for {field}."
    return errors, parsed

@app.route("/")
def index():
    lang = request.args.get('lang', 'en')
    return render_template("index.html", lang=lang, t=t)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return redirect(url_for("index", lang=request.args.get("lang", "en")))
    
    lang = request.args.get('lang', 'en')
    errors, parsed = validate_inputs(request.form)
    if errors:
        return render_template("index.html", errors=errors, form_data=request.form, lang=lang, t=t), 400

    try:
        n = parsed["Nitrogen"]
        p = parsed["Phosphorus"]
        k = parsed["Potassium"]
        temp = parsed["Temperature"]
        humidity = parsed["Humidity"]
        ph = parsed["Ph"]
        rainfall = parsed["Rainfall"]

        features = np.array([[n, p, k, temp, humidity, ph, rainfall]])
        features = ms.transform(features)

        prediction = model.predict(features)
        crop = prediction[0]
        result = crop

        # ponytail: dynamic multilingual TTS speech text & voice selection
        translated_crop = t(crop, lang)
        recommend_title = t("recommend_title", lang)
        tts_text = f"{recommend_title} {translated_crop}."
        voice = VOICES.get(lang, VOICES["en"])

        audio_path = os.path.join(BASE_DIR, "static", "result.mp3")
        asyncio.run(generate_audio(tts_text, audio_path, voice))
        print("Audio saved successfully!")

        return render_template("index.html", result=result, lang=lang, t=t, crop=crop, form_data=request.form)

    except Exception as e:
        print("ERROR:", e)
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(debug=True,port=5002)