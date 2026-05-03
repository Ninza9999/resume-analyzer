const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");

fileInput.addEventListener("change", () => {
    fileName.innerText = fileInput.files[0].name;
});

async function uploadFile() {
    const file = fileInput.files[0];
    const result = document.getElementById("result");
    const loader = document.getElementById("loader");

    if (!file) {
        alert("Upload a file first");
        return;
    }

    loader.style.display = "block";
    result.innerHTML = "";

    const formData = new FormData();
    formData.append("resume", file);

    try {
        const response = await fetch("https://resume-analyzer-ehx2.onrender.com/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        loader.style.display = "none";

        // Chart
        const ctx = document.getElementById("scoreChart").getContext("2d");
        new Chart(ctx, {
            type: "doughnut",
            data: {
                datasets: [{
                    data: [data.match_percentage, 100 - data.match_percentage]
                }]
            },
            options: {
                cutout: "70%"
            }
        });

        result.innerHTML = `
            <div class="card">🔥 Score: ${data.score}/10</div>
            <div class="card">📊 Match: ${data.match_percentage}%</div>
            <div class="card">🧠 Skills: ${data.skills.join(", ")}</div>
            <div class="card">⚠ Missing: ${data.missing.join(", ")}</div>
            <div class="card">💡 ${data.evaluation}</div>
        `;

    } catch (err) {
        loader.style.display = "none";
        result.innerHTML = "❌ Backend error";
    }
}