from flask import Flask, request, render_template
import numpy as np
import pickle
import os
import asyncio
import edge_tts

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = pickle.load(open(os.path.join(BASE_DIR, "model.pkl"), "rb"))
ms = pickle.load(open(os.path.join(BASE_DIR, "minmaxscaler.pkl"), "rb"))

app = Flask(__name__)

VOICE = "en-US-JennyNeural"

async def generate_audio(text, path):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(path)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
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
        result = f"{prediction[0]} is the best crop to be cultivated right there."

        audio_path = os.path.join(BASE_DIR, "static", "result.mp3")
        asyncio.run(generate_audio(result, audio_path))
        print("Audio saved successfully!")

        return render_template("index.html", result=result)

    except Exception as e:
        print("ERROR:", e)
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(debug=True,port=5002)