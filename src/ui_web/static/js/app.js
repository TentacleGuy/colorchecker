// app.js
document.addEventListener("DOMContentLoaded", function () {
    const captureButton = document.getElementById("capture-button");
    const resultList = document.getElementById("result-list");
    const settingsForm = document.getElementById("settings-form");
    const videoStream = document.getElementById("video-stream");
    const reloadBtn = document.getElementById("reload-stream");
    const streamOverlay = document.getElementById("stream-overlay");

    captureButton.addEventListener("click", function () {
        fetch("/api/capture", {
            method: "POST"
        })
            .then(response => response.json())
            .then(data => {
                updateResults(data);
            })
            .catch(error => console.error("Error capturing image:", error));
    });

    settingsForm.addEventListener("submit", function (event) {
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

    // --- MJPEG Stream Handling ---
    function showOverlay(msg) {
        if (!streamOverlay) return;
        streamOverlay.textContent = msg;
        streamOverlay.classList.remove("hidden");
    }

    function hideOverlay() {
        if (!streamOverlay) return;
        streamOverlay.classList.add("hidden");
    }

    function reloadStream(force) {
        if (!videoStream) return;
        showOverlay("Lade Stream...");
        // Cache-Buster Query
        const base = "/stream";
        videoStream.src = base + (force ? ("?t=" + Date.now()) : "");
    }

    if (reloadBtn) {
        reloadBtn.addEventListener("click", () => reloadStream(true));
    }

    if (videoStream) {
        videoStream.addEventListener("load", () => {
            // load feuert bei img evtl. nicht zuverlässig für MJPEG; daher kurzer Delay
            setTimeout(() => hideOverlay(), 300);
        });
        videoStream.addEventListener("error", () => {
            showOverlay("Fehler beim Laden des Streams. Versuche Neuverbindung...");
            setTimeout(() => reloadStream(true), 2000);
        });
    }

    // Initial overlay (wird ausgeblendet sobald ein Frame kommt)
    showOverlay("Verbinde zum Kamera-Stream...");
});