from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "AI Resume Analyzer Backend Running 🚀"

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['resume']

    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""

        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        text = text.lower()

        skills_list = ["python", "machine learning", "data science", "sql", "flask", "deep learning"]
        found_skills = [skill for skill in skills_list if skill in text]
        missing_skills = [skill for skill in skills_list if skill not in text]

        score = len(found_skills) * 2
        match_percentage = int((len(found_skills) / len(skills_list)) * 100)

        return jsonify({
            "score": score,
            "match_percentage": match_percentage,
            "skills": found_skills,
            "missing": missing_skills,
            "evaluation": "Strong profile 🚀" if score >= 6 else "Needs improvement ⚠️",
            "summary": f"Found {len(found_skills)} relevant skills in your resume."
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
