
// =====================================
// SITERESTORE AI — THEME MANAGEMENT
// =====================================

const themeToggle = document.getElementById("themeToggle");
const themeIcon = document.getElementById("themeIcon");

// Load previously selected theme
const savedTheme = localStorage.getItem("siteRestoreTheme") || "light";

// Apply theme
function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);

    // Update toggle icon
    themeIcon.textContent = theme === "dark" ? "☼" : "☾";

    // Update browser storage
    localStorage.setItem("siteRestoreTheme", theme);
}

// Initialize theme
applyTheme(savedTheme);

// Toggle between dark and light
themeToggle.addEventListener("click", () => {
    const currentTheme =
        document.documentElement.getAttribute("data-theme");

    const newTheme = currentTheme === "dark" ? "light" : "dark";

    applyTheme(newTheme);
});

// =====================================
// IMAGE UPLOAD AND PREVIEW
// =====================================

const imageInput = document.getElementById("imageInput");
const fileName = document.getElementById("fileName");
const previewArea = document.getElementById("previewArea");
const originalResult = document.getElementById("originalResult");

let selectedImage = null;
let imagePreviewURL = null;

imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) {
        return;
    }

    // Validate image type
    if (!file.type.startsWith("image/")) {
        alert("Please select a valid image file.");
        this.value = "";
        return;
    }

    // Release previous preview URL
    if (imagePreviewURL) {
        URL.revokeObjectURL(imagePreviewURL);
    }

    selectedImage = file;
    imagePreviewURL = URL.createObjectURL(file);

    // Display filename
    fileName.textContent = file.name;

    // Display preview
    previewArea.innerHTML = `
        <img src="${imagePreviewURL}" alt="Uploaded image preview">
    `;

    // Display original image in results
    originalResult.innerHTML = `
        <img src="${imagePreviewURL}" alt="Original uploaded image">
    `;
});

// =====================================
// IMAGE RESTORATION
// =====================================

const restoreButton = document.getElementById("restoreButton");
const categorySelect = document.getElementById("category");
const methodSelect = document.getElementById("method");
const restoredResult = document.getElementById("restoredResult");

let restoredImageURL = null;

restoreButton.addEventListener("click", async function () {

    // Check whether an image is selected
    if (!selectedImage) {
        alert("Please upload an image first.");
        return;
    }

    // Prepare image and settings
    const formData = new FormData();

    formData.append("image", selectedImage);
    formData.append("category", categorySelect.value);
    formData.append("method", methodSelect.value);

    // Show processing status
    restoreButton.disabled = true;
    restoreButton.textContent = "Processing...";

    restoredResult.textContent = "Restoration in progress...";
    document.getElementById("processingTime").textContent = "";
    try {

        // Send request to Flask
        const response = await fetch("/api/restore", {
            method: "POST",
            body: formData
        });

        // Handle errors returned by Flask
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Restoration failed.");
        }

        // Receive restored image
        const imageBlob = await response.blob();

        // Read processing time
        const processingTime =
            Number(response.headers.get("X-Processing-Time"));

        // Release previous restored image URL
        if (restoredImageURL) {
            URL.revokeObjectURL(restoredImageURL);
        }

        // Create URL for restored image
        restoredImageURL = URL.createObjectURL(imageBlob);

        // Display restored image
        restoredResult.innerHTML = `
            <img src="${restoredImageURL}"
                 alt="Restored telecom infrastructure image">
        `;

        // Display processing time
        // Display processing time below the image
        document.getElementById("processingTime").textContent =
            `Processing time: ${processingTime.toFixed(2)} seconds`;

    } catch (error) {

        restoredResult.textContent = "Restoration failed: " + error.message;

        console.error("Restoration error:", error);

    } finally {

        // Restore button
        restoreButton.disabled = false;
        restoreButton.textContent = "Start Restoration →";
    }
});
