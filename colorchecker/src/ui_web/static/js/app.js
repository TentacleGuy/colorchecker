// app.js
document.addEventListener("DOMContentLoaded", function() {
    const captureButton = document.getElementById("capture-button");
    const resultList = document.getElementById("result-list");
    const settingsForm = document.getElementById("settings-form");

    captureButton.addEventListener("click", function() {
        fetch("/api/capture", {
            method: "POST"
        })
        .then(response => response.json())
        .then(data => {
            updateResults(data);
        })
        .catch(error => console.error("Error capturing image:", error));
    });

    settingsForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const formData = new FormData(settingsForm);
        fetch("/api/settings", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log("Settings updated:", data);
        })
        .catch(error => console.error("Error updating settings:", error));
    });

    function updateResults(data) {
        resultList.innerHTML = "";
        data.results.forEach(result => {
            const listItem = document.createElement("li");
            listItem.textContent = `Name: ${result.name}, RGB: ${result.rgb}, ΔE: ${result.deltaE}`;
            resultList.appendChild(listItem);
        });
    }
});