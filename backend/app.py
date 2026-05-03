from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2

app = Flask(__name__)
CORS(app)

def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text

def analyze_text(text):
    skills_list = [
        "python", "machine learning", "sql",
        "data science", "deep learning", "flask"
    ]

    found_skills = []
    missing_skills = []

    text_lower = text.lower()

    for skill in skills_list:
        if skill in text_lower:
            found_skills.append(skill.title())
        else:
            missing_skills.append(skill.title())

    score = int((len(found_skills) / len(skills_list)) * 10)
    match_percentage = int((len(found_skills) / len(skills_list)) * 100)

    return found_skills, missing_skills, score, match_percentage

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    file = request.files.get('resume')
    job_role = request.form.get('job_role', 'General Role')

    if file is None:
        return jsonify({"error": "No file received"}), 400

    text = extract_text(file)

    if text.strip() == "":
        return jsonify({"error": "Could not extract text"}), 400

    skills, missing, score, match_percentage = analyze_text(text)

    if score >= 8:
        evaluation = "Strong profile with good technical skills."
    elif score >= 5:
        evaluation = "Average profile with room for improvement."
    else:
        evaluation = "Weak profile, needs improvement."

    summary = f"For a {job_role}, your resume shows strength in {', '.join(skills[:2])}. Improve {', '.join(missing[:2])}."

    return jsonify({
        "score": score,
        "match_percentage": match_percentage,
        "skills": skills,
        "missing": missing,
        "evaluation": evaluation,
        "summary": summary,
        "recommendation": f"Focus on improving: {', '.join(missing)}"
    })

if __name__ == "__main__":
    app.run(debug=True)
if __name__ == "__main__":
    app.run()
