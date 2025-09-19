from flask import Flask, render_template, request
import pickle
import re

app = Flask(__name__)

# Load model and vectorizer
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Text cleaning
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)  # remove special chars/numbers
    return text

# Rule-based + ML prediction
scam_words = ["registration fee", "bank account", "earn", "congratulations", "limited seats","free","no interview"]

def predict_job(text):
    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]

    # Rule-based check
    if any(word in cleaned for word in scam_words):
        return "❌ Fake Job"
    return "❌ Fake Job" if prediction == 1 else "✅ Real Job"

# Routes
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        job_text = request.form["job_text"]
        result = predict_job(job_text)   # <-- predict_job is defined above
        return render_template("result.html", prediction=result, job_text=job_text)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
