const fileInput = document.getElementById("fileInput");
const fileStatus = document.getElementById("fileStatus");

fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        fileStatus.innerText = "✔ " + fileInput.files[0].name;
    }
});

async function uploadFile() {

    const file = fileInput.files[0];
    const loader = document.getElementById("loader");
    const result = document.getElementById("result");

    if (!file) {
        alert("Upload a resume first!");
        return;
    }

    loader.classList.remove("hidden");
    result.innerHTML = "Analyzing your resume...";

    const formData = new FormData();
    formData.append("resume", file);

    try {
        const response = await fetch("https://resume-analyzer-ehx2.onrender.com/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        result.innerHTML = `
            <div class="result-card">🔥 Score: ${data.score}/10</div>
            <div class="result-card">📊 Match: ${data.match_percentage}%</div>
            <div class="result-card">🧠 Skills: ${data.skills.join(", ")}</div>
            <div class="result-card">⚠ Missing: ${data.missing.join(", ")}</div>
            <div class="result-card">💡 ${data.evaluation}</div>
        `;

    } catch (err) {
        result.innerHTML = "❌ Backend error";
    }

    loader.classList.add("hidden");
}