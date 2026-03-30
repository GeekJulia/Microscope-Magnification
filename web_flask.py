"""
web_flask.py — Part D (Flask rewrite)
======================================
Run with:
    pip install flask
    python web_flask.py
Then open http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, jsonify, send_file
import io, csv, os
from core_logic import run_measurement, CSV_FILE, FIELDNAMES, ensure_csv_exists

app = Flask(__name__)

# ── Unit conversion table (all relative to µm) ─────────────────
UNIT_FACTORS = {
    "µm": 1,
    "nm": 1_000,
    "mm": 1e-3,
    "cm": 1e-4,
    "m":  1e-6,
    "pm": 1e9,
}


def convert(value_um: float, unit: str) -> float:
    """Convert a value in µm to the requested unit."""
    return value_um * UNIT_FACTORS.get(unit, 1)


# ── Routes ─────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main page."""
    ensure_csv_exists()
    return render_template("index.html", units=list(UNIT_FACTORS.keys()))


@app.route("/calculate", methods=["POST"])
def calculate():
    """
    Receive JSON from the frontend, calculate, save, and return result.
    Expected JSON body: { username, image_size, magnification, unit }
    """
    data = request.get_json(force=True)

    username      = (data.get("username") or "").strip()
    unit          = data.get("unit", "µm")

    # --- Validate ---
    errors = []
    if not username:
        errors.append("Username cannot be empty.")

    try:
        image_size    = float(data.get("image_size", 0))
        magnification = float(data.get("magnification", 0))
        if image_size <= 0:
            errors.append("Image size must be greater than 0.")
        if magnification <= 0:
            errors.append("Magnification must be greater than 0.")
    except (TypeError, ValueError):
        errors.append("Image size and magnification must be valid numbers.")

    if errors:
        return jsonify({"ok": False, "errors": errors}), 400

    # --- Calculate & save ---
    actual_um = run_measurement(username, image_size, magnification)
    displayed = convert(actual_um, unit)

    return jsonify({
        "ok":           True,
        "actual_um":    actual_um,
        "displayed":    displayed,
        "unit":         unit,
        "image_size":   image_size,
        "magnification": magnification,
        "username":     username,
    })


@app.route("/history")
def history():
    """Return all CSV rows as JSON for the live table."""
    ensure_csv_exists()
    rows = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline="") as f:
            rows = list(csv.DictReader(f))
    return jsonify(list(reversed(rows)))   # newest first


@app.route("/download")
def download():
    """Stream the CSV file as a download."""
    ensure_csv_exists()
    return send_file(
        os.path.abspath(CSV_FILE),
        mimetype="text/csv",
        as_attachment=True,
        download_name="measurements.csv",
    )


# ── Dev server ─────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)