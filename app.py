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

@app.route("/")
def index():
    lang = request.args.get('lang', 'en')
    return render_template("index.html", lang=lang, t=t)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return redirect(url_for("index", lang=request.args.get("lang", "en")))
    try:
        lang = request.args.get('lang', 'en')
        n = int(request.form["Nitrogen"])
        p = int(request.form["Phosphorus"])
        k = int(request.form["Potassium"])
        temp = float(request.form["Temperature"])
        humidity = float(request.form["Humidity"])
        ph = float(request.form["Ph"])
        rainfall = float(request.form["Rainfall"])

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

        return render_template("index.html", result=result,lang=lang, t=t, crop=crop)

    except Exception as e:
        print("ERROR:", e)
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(debug=True,port=5002)