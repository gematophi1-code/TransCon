const IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "bmp", "webp"];
const IMAGE_FORMATS = ["jpeg", "png", "gif", "bmp", "webp"];

const fileInput = document.getElementById("file");
const formatSelect = document.getElementById("target_format");

function normalize(extension) {
    return extension === "jpg" ? "jpeg" : extension;
}

fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (!file) return;

    const extension = normalize(file.name.split(".").pop().toLowerCase());
    let options = [];

    if (IMAGE_EXTENSIONS.includes(extension)) {
        options = IMAGE_FORMATS.filter((format) => format !== extension);
    } else if (extension === "txt") {
        options = ["pdf"];
    } else if (extension === "pdf") {
        options = ["txt"];
    }

    formatSelect.innerHTML = "";

    if (options.length === 0) {
        formatSelect.innerHTML = '<option value="">формат не поддерживается</option>';
        formatSelect.disabled = true;
        return;
    }

    formatSelect.disabled = false;
    for (const format of options) {
        const option = document.createElement("option");
        option.value = format;
        option.textContent = format.toUpperCase();
        formatSelect.appendChild(option);
    }
});