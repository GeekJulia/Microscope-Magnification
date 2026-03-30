"""
core_logic.py — Part A & B: Core Calculation Logic & CSV Storage
=================================================================
Formula: Real Size = Image Size / Magnification
This module handles the calculation and stores results in measurements.csv.
"""

import csv
import os
from datetime import datetime

# ── Configuration ──────────────────────────────────────────────
CSV_FILE = "measurements.csv"
FIELDNAMES = ["timestamp", "username", "image_size_um", "magnification", "actual_size_um"]


# ── CSV Helpers ─────────────────────────────────────────────────

def ensure_csv_exists():
    """Create measurements.csv with a header row if the file does not exist yet."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
        print(f"[INFO] Created '{CSV_FILE}' with headers.")


def append_measurement(username: str, image_size_um: float, magnification: float, actual_size_um: float):
    """
    Append one measurement record to the CSV file.

    Parameters
    ----------
    username       : Name of the person who took the measurement.
    image_size_um  : Size of the specimen as it appears in the image (µm).
    magnification  : Magnification factor of the microscope (e.g. 400).
    actual_size_um : Calculated real-life size of the specimen (µm).
    """
    ensure_csv_exists()
    row = {
        "timestamp":      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username":       username.strip(),
        "image_size_um":  round(image_size_um, 4),
        "magnification":  round(magnification, 4),
        "actual_size_um": round(actual_size_um, 6),
    }
    with open(CSV_FILE, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(row)
    print(f"[INFO] Saved → {row}")


# ── Core Calculation ────────────────────────────────────────────

def calculate_real_size(image_size_um: float, magnification: float) -> float:
    """
    Calculate the real-life size of a specimen.

    Formula : Real Size (µm) = Image Size (µm) / Magnification

    Parameters
    ----------
    image_size_um : Size measured on the microscope image (µm).
    magnification : Magnification used (must be > 0).

    Returns
    -------
    float : Actual specimen size in micrometres (µm).

    Raises
    ------
    ValueError : If either value is non-positive.
    """
    if image_size_um <= 0:
        raise ValueError("Image size must be a positive number.")
    if magnification <= 0:
        raise ValueError("Magnification must be a positive number.")
    return image_size_um / magnification


def run_measurement(username: str, image_size_um: float, magnification: float) -> float:
    """
    Convenience wrapper: calculate + save in one call.

    Returns the calculated actual size (µm).
    """
    actual_size = calculate_real_size(image_size_um, magnification)
    append_measurement(username, image_size_um, magnification, actual_size)
    return actual_size


# ── CLI Demo (run this file directly to test) ───────────────────

if __name__ == "__main__":
    print("=== Microscope Size Calculator — Core Logic Demo ===\n")
    try:
        name  = input("Enter your username : ").strip() or "demo_user"
        img   = float(input("Image size (µm)     : "))
        mag   = float(input("Magnification       : "))

        result = run_measurement(name, img, mag)
        print(f"\n✅  Actual specimen size ≈ {result:.6f} µm  ({result * 1000:.4f} nm)")
        print(f"    Data saved to '{CSV_FILE}'.")
    except ValueError as e:
        print(f"❌  Input error: {e}")