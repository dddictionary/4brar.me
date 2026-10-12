// static/js/ascii-cam.js
//
// Webcam -> ASCII, using textura's wasm build (github.com/dddictionary/ascii-rs).
// The browser does capture and scaling: each frame is drawn into a canvas that
// is exactly cols x rows pixels, so one pixel maps to one glyph. Rust turns
// those pixels into glyphs; colour is read back from the same pixels here.
import init, { Converter, fitGrid, presetNames } from "/static/wasm/textura/textura.js";

// Character cells are about twice as tall as they are wide. Mirrors
// layout::DEFAULT_CELL_ASPECT in ascii-rs.
const CELL_ASPECT = 2.0;
// IBM Plex Mono advances 0.6em per glyph, so this font size fills a cell's width.
const FONT_SCALE = 1 / 0.6;

const video = document.getElementById("camVideo");
const output = document.getElementById("asciiOutput");
const stage = output.parentElement;
const toggle = document.getElementById("camToggle");
const rampSelect = document.getElementById("rampSelect");
const detailRange = document.getElementById("detailRange");
const normalizeToggle = document.getElementById("normalizeToggle");
const status = document.getElementById("camStatus");

const sample = document.createElement("canvas");
const sampleCtx = sample.getContext("2d", { willReadFrequently: true });
const outCtx = output.getContext("2d");

let converter;
let stream = null;
let frameId = 0;
let grid = { cols: 0, rows: 0, cellW: 0, cellH: 0 };

function setStatus(text) {
    status.textContent = text;
    status.hidden = !text;
}

// Sizes the sampling canvas to the glyph grid and the output canvas to fill
// the stage at device resolution.
function layout() {
    if (!video.videoWidth) return;

    const maxCols = Number(detailRange.value);
    const [cols, rows] = fitGrid(video.videoWidth, video.videoHeight, maxCols, maxCols, CELL_ASPECT);
    sample.width = cols;
    sample.height = rows;

    const cssW = stage.clientWidth;
    const cellW = cssW / cols;
    const cellH = cellW * CELL_ASPECT;
    const cssH = cellH * rows;
    const dpr = window.devicePixelRatio || 1;

    output.style.height = `${cssH}px`;
    output.width = Math.round(cssW * dpr);
    output.height = Math.round(cssH * dpr);
    outCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
    outCtx.font = `${cellW * FONT_SCALE}px 'IBM Plex Mono', monospace`;
    outCtx.textBaseline = "middle";

    grid = { cols, rows, cellW, cellH };
}

function draw() {
    const { cols, rows, cellW, cellH } = grid;

    // Mirror horizontally so it behaves like a mirror, not a camera.
    sampleCtx.setTransform(-1, 0, 0, 1, cols, 0);
    sampleCtx.drawImage(video, 0, 0, cols, rows);
    const pixels = sampleCtx.getImageData(0, 0, cols, rows).data;

    const lines = converter.render(pixels, cols, rows).split("\n");

    outCtx.clearRect(0, 0, cols * cellW, rows * cellH);
    for (let y = 0; y < rows; y++) {
        // Array.from splits by code point, so block and braille ramps line up.
        const glyphs = Array.from(lines[y] || "");
        const cy = y * cellH + cellH / 2;
        for (let x = 0; x < cols; x++) {
            const glyph = glyphs[x];
            if (!glyph || glyph === " ") continue;

            // Glyph density already carries brightness, so lift the colour
            // toward full intensity and let it carry hue.
            const i = (y * cols + x) * 4;
            const r = pixels[i], g = pixels[i + 1], b = pixels[i + 2];
            const k = Math.min(3, 255 / Math.max(r, g, b, 1));
            outCtx.fillStyle = `rgb(${r * k | 0},${g * k | 0},${b * k | 0})`;
            outCtx.fillText(glyph, x * cellW, cy);
        }
    }
}

function loop() {
    if (video.readyState >= video.HAVE_CURRENT_DATA && grid.cols) draw();
    frameId = requestAnimationFrame(loop);
}

async function start() {
    toggle.disabled = true;
    setStatus("Waiting for camera permission…");
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    } catch (err) {
        stream = null;
        toggle.disabled = false;
        if (err.name === "NotAllowedError") setStatus("Camera permission was denied.");
        else if (err.name === "NotFoundError") setStatus("No camera found.");
        else setStatus(`Could not start the camera: ${err.message}`);
        return;
    }

    video.srcObject = stream;
    await video.play();
    layout();
    setStatus("");
    toggle.textContent = "Stop camera";
    toggle.disabled = false;
    frameId = requestAnimationFrame(loop);
}

function stop() {
    cancelAnimationFrame(frameId);
    stream.getTracks().forEach((track) => track.stop());
    stream = null;
    video.srcObject = null;
    outCtx.clearRect(0, 0, output.width, output.height);
    toggle.textContent = "Start camera";
    setStatus("Camera stopped.");
}

async function main() {
    if (!navigator.mediaDevices?.getUserMedia) {
        setStatus("This browser can't access a camera here (it needs HTTPS or localhost).");
        return;
    }

    await init();
    converter = new Converter();

    for (const name of presetNames().split("\n")) {
        rampSelect.add(new Option(name, name));
    }
    rampSelect.value = "classic-heavy";
    converter.setPreset(rampSelect.value);

    rampSelect.addEventListener("change", () => converter.setPreset(rampSelect.value));
    normalizeToggle.addEventListener("change", () => converter.setNormalize(normalizeToggle.checked));
    detailRange.addEventListener("input", layout);
    // Only width drives the layout; layout() itself changes the stage height.
    let stageWidth = 0;
    new ResizeObserver(([entry]) => {
        if (entry.contentRect.width === stageWidth) return;
        stageWidth = entry.contentRect.width;
        layout();
    }).observe(stage);
    toggle.addEventListener("click", () => (stream ? stop() : start()));

    toggle.disabled = false;
    setStatus("Press start to turn on your camera.");
}

main().catch((err) => setStatus(`Failed to load: ${err.message}`));
