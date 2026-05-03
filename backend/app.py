from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2

app = Flask(__name__)
CORS(app)  # allows frontend (Netlify) to talk to backend

# 🔥 Skills database (you can expand this later)
SKILLS_DB = [
    "Python", "Machine Learning", "Deep Learning",
    "Flask", "Django", "SQL", "Data Science",
    "Pandas", "NumPy", "TensorFlow", "PyTorch"
]

# 📄 Extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text.lower()

# 🚀 Analyze Resume
@app.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        file = request.files.get('resume')

        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        # Extract text
        resume_text = extract_text_from_pdf(file)

        # Detect skills
        found_skills = []
        missing_skills = []

        for skill in SKILLS_DB:
            if skill.lower() in resume_text:
                found_skills.append(skill)
            else:
                missing_skills.append(skill)

        # Score calculation
        score = round(len(found_skills) / len(SKILLS_DB) * 10)
        match_percentage = round(len(found_skills) / len(SKILLS_DB) * 100)

        # Smart evaluation
        if score >= 8:
            evaluation = "Excellent profile 🚀"
        elif score >= 5:
            evaluation = "Good profile, can improve 👍"
        else:
            evaluation = "Needs improvement ⚠️"

        return jsonify({
            "score": score,
            "match_percentage": match_percentage,
            "skills": found_skills,
            "missing": missing_skills,
            "evaluation": evaluation,
            "summary": f"Detected {len(found_skills)} relevant skills."
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 👇 Important for Render deployment
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
