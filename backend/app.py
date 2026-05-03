from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2

app = Flask(__name__)
CORS(app)

SKILLS = ["python", "machine learning", "sql", "data science", "flask", "deep learning"]

def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.lower()

@app.route('/')
def home():
    return "Backend running"

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get("resume")

    if not file:
        return jsonify({"error": "No file"}), 400

    text = extract_text(file)

    found = [s for s in SKILLS if s in text]
    missing = [s for s in SKILLS if s not in text]

    score = round(len(found)/len(SKILLS)*10)
    match = round(len(found)/len(SKILLS)*100)

    return jsonify({
        "score": score,
        "match_percentage": match,
        "skills": found,
        "missing": missing,
        "evaluation": "Good profile" if score >=5 else "Needs improvement"
    })

if __name__ == "__main__":
    app.run()
