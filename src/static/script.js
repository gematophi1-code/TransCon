const IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "bmp", "webp"];
const IMAGE_FORMATS = ["jpeg", "png", "gif", "bmp", "webp"];

const fileInput = document.getElementById("file");
const drop = document.getElementById("drop");
const dropTitle = document.getElementById("drop-title");
const dropHint = document.getElementById("drop-hint");
const chips = document.getElementById("chips");
const empty = document.getElementById("empty");
const target = document.getElementById("target_format");
const submitButton = document.getElementById("submit");

const normalize = (ext) => (ext === "jpg" ? "jpeg" : ext);

function optionsFor(name) {
    const ext = normalize((name.split(".").pop() || "").toLowerCase());
    if (IMAGE_EXTENSIONS.includes(ext)) return IMAGE_FORMATS.filter((f) => f !== ext);
    if (ext === "txt") return ["pdf", "docx"];
    if (ext === "pdf") return ["txt", "docx"];
    if (ext === "docx") return ["txt", "pdf"];
    return [];
}

function select(format) {
    target.value = format;
    for (const chip of chips.children) chip.classList.toggle("is-active", chip.dataset.format === format);
    submitButton.disabled = false;
    submitButton.textContent = "Конвертировать → " + format.toUpperCase();
}

function render(file) {
    const options = optionsFor(file.name);
    chips.innerHTML = "";
    target.value = "";
    submitButton.disabled = true;
    submitButton.textContent = "Конвертировать";

    dropTitle.textContent = file.name;
    dropHint.textContent = "нажмите, чтобы заменить";

    if (!options.length) {
        empty.textContent = "формат не поддерживается";
        return;
    }

    for (const format of options) {
        const chip = document.createElement("button");
        chip.type = "button";
        chip.className = "chip";
        chip.dataset.format = format;
        chip.textContent = format.toUpperCase();
        chip.addEventListener("click", () => select(format));
        chips.appendChild(chip);
    }
    select(options[0]);
}

fileInput.addEventListener("change", () => {
    if (fileInput.files[0]) render(fileInput.files[0]);
});

drop.addEventListener("dragover", (e) => {
    e.preventDefault();
    drop.classList.add("is-over");
});
drop.addEventListener("dragleave", () => drop.classList.remove("is-over"));
drop.addEventListener("drop", (e) => {
    e.preventDefault();
    drop.classList.remove("is-over");
    const file = e.dataTransfer.files[0];
    if (!file) return;
    fileInput.files = e.dataTransfer.files;
    render(file);
});

// фоновый «дождь» глифов
(function rain() {
    const canvas = document.getElementById("rain");
    if (!canvas || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const ctx = canvas.getContext("2d");
    const glyphs = "01アイウエオカキクケコサシスセソナニヌネノハヒフヘホ<>{}[]/\\|+=".split("");
    const size = 14;
    let cols = [], w = 0, h = 0;

    function resize() {
        const rect = canvas.getBoundingClientRect();
        w = canvas.width = Math.max(1, rect.width);
        h = canvas.height = Math.max(1, rect.height);
        cols = new Array(Math.ceil(w / size)).fill(0).map(() => Math.random() * -60);
    }
    resize();
    window.addEventListener("resize", resize);

    let last = 0;
    function tick(t) {
        requestAnimationFrame(tick);
        if (t - last < 70) return;
        last = t;
        ctx.fillStyle = "rgba(8,10,9,0.18)";
        ctx.fillRect(0, 0, w, h);
        ctx.font = size + "px 'JetBrains Mono', monospace";
        for (let i = 0; i < cols.length; i++) {
            const y = cols[i] * size;
            ctx.fillStyle = Math.random() > 0.94 ? "#c9ffe0" : "#3ddc8a";
            ctx.fillText(glyphs[(Math.random() * glyphs.length) | 0], i * size, y);
            cols[i] = y > h && Math.random() > 0.975 ? 0 : cols[i] + 1;
        }
    }
    requestAnimationFrame(tick);
})();
