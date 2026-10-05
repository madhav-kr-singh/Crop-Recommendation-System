"""Run: python test_app.py   (no network needed; TTS is stubbed)"""
import os, shutil
import app

RICE = {"Nitrogen": "90", "Phosphorus": "42", "Potassium": "43", "Temperature": "20.9",
        "Humidity": "82", "Ph": "6.5", "Rainfall": "203"}
TTS_DIR = os.path.join(app.BASE_DIR, "static", "tts")


def demo():
    shutil.rmtree(TTS_DIR, ignore_errors=True)
    c = app.app.test_client()

    async def ok(text, path, voice):
        open(path, "wb").write(b"mp3")
    app.generate_audio = ok
    r = c.post("/predict?lang=hi", data=RICE)
    assert r.status_code == 200 and b"tts/hi_rice.mp3" in r.data, "per-crop clip URL"
    assert os.path.exists(os.path.join(TTS_DIR, "hi_rice.mp3"))
    assert not [f for f in os.listdir(TTS_DIR) if f.endswith(".tmp")], "temp file left behind"

    r = c.post("/predict?lang=../../evil", data=RICE)
    assert r.status_code == 200 and b"tts/en_rice.mp3" in r.data, "unknown lang must not reach the path"

    async def boom(text, path, voice):
        raise ConnectionError("no network")
    app.generate_audio = boom
    os.remove(os.path.join(TTS_DIR, "hi_rice.mp3"))
    r = c.post("/predict?lang=hi", data=RICE)
    assert r.status_code == 200 and b"result-card" in r.data, "TTS failure must still show the crop"
    assert b"<audio id=\"result-audio\"" not in r.data, "no audio player when TTS failed"

    # unit conversion used by the paper (oxide basis -> element)
    assert abs(app.convert_input_value("Phosphorus", 100, "p2o5") - 43.64) < 1e-9
    assert abs(app.convert_input_value("Temperature", 212, "fahrenheit") - 100) < 1e-9

    shutil.rmtree(TTS_DIR, ignore_errors=True)
    print("all checks passed")


if __name__ == "__main__":
    demo()
