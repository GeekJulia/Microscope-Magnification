"""
gui_tkinter.py — Part C: Desktop GUI with Tkinter
==================================================
A polished Tkinter window that collects inputs, runs the calculation,
and appends each measurement to measurements.csv.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from core_logic import run_measurement, CSV_FILE, FIELDNAMES, ensure_csv_exists

# ── Colour palette (dark-lab aesthetic) ────────────────────────
BG        = "#0f1117"   # deep background
SURFACE   = "#1c1f2b"   # card / entry background
ACCENT    = "#00d4aa"   # teal highlight
TEXT      = "#e8eaf0"   # primary text
SUBTEXT   = "#7b8099"   # secondary / label text
SUCCESS   = "#2ecc71"
ERROR     = "#e74c3c"
FONT_HEAD = ("Courier New", 18, "bold")
FONT_LBL  = ("Courier New", 10)
FONT_BODY = ("Courier New", 11)
FONT_BTN  = ("Courier New", 11, "bold")


class MicroscopeApp(tk.Tk):
    """Main application window for the Microscope Size Calculator."""

    def __init__(self):
        super().__init__()
        self.title("🔬 Microscope Size Calculator")
        self.geometry("520x620")
        self.resizable(False, False)
        self.configure(bg=BG)

        # Make sure the CSV exists before we try to read it
        ensure_csv_exists()

        self._build_ui()

    # ── UI Construction ────────────────────────────────────────

    def _build_ui(self):
        """Assemble all widgets."""
        # ── Header ──
        header_frame = tk.Frame(self, bg=ACCENT, pady=14)
        header_frame.pack(fill="x")
        tk.Label(
            header_frame, text="🔬  MICROSCOPE CALCULATOR",
            font=FONT_HEAD, bg=ACCENT, fg=BG
        ).pack()
        tk.Label(
            header_frame, text="Real Size  =  Image Size  ÷  Magnification",
            font=FONT_LBL, bg=ACCENT, fg=BG
        ).pack()

        # ── Input card ──
        card = tk.Frame(self, bg=SURFACE, padx=30, pady=24)
        card.pack(fill="x", padx=24, pady=(20, 0))

        self.entry_username  = self._labelled_entry(card, "Username",          row=0)
        self.entry_img_size  = self._labelled_entry(card, "Image Size (µm)",   row=1)
        self.entry_magnify   = self._labelled_entry(card, "Magnification (×)", row=2)

        # ── Calculate button ──
        tk.Button(
            self, text="⚡  CALCULATE & SAVE",
            font=FONT_BTN, bg=ACCENT, fg=BG,
            activebackground="#00b894", activeforeground=BG,
            relief="flat", cursor="hand2", pady=10,
            command=self._on_calculate
        ).pack(fill="x", padx=24, pady=14)

        # ── Result label ──
        self.result_var = tk.StringVar(value="— enter values and press Calculate —")
        self.result_lbl = tk.Label(
            self, textvariable=self.result_var,
            font=("Courier New", 12, "bold"), bg=BG, fg=SUBTEXT,
            wraplength=460, justify="center"
        )
        self.result_lbl.pack(pady=(0, 14))

        # ── History table ──
        tk.Label(
            self, text="SAVED MEASUREMENTS",
            font=("Courier New", 9, "bold"), bg=BG, fg=SUBTEXT
        ).pack(anchor="w", padx=24)

        table_frame = tk.Frame(self, bg=BG)
        table_frame.pack(fill="both", expand=True, padx=24, pady=(4, 16))

        cols = ("timestamp", "username", "image_µm", "magnification", "actual_µm")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=7)
        widths    = (130, 90, 80, 110, 90)
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        # Style the treeview
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview",
                         background=SURFACE, foreground=TEXT,
                         fieldbackground=SURFACE, rowheight=22,
                         font=("Courier New", 8))
        style.configure("Treeview.Heading",
                         background=ACCENT, foreground=BG,
                         font=("Courier New", 8, "bold"))
        style.map("Treeview", background=[("selected", "#2d3250")])

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._refresh_table()

    def _labelled_entry(self, parent, label_text: str, row: int) -> tk.Entry:
        """Helper: create a label + styled entry in a grid row."""
        tk.Label(
            parent, text=label_text, font=FONT_LBL,
            bg=SURFACE, fg=SUBTEXT, anchor="w"
        ).grid(row=row*2, column=0, sticky="w", pady=(10, 2))

        entry = tk.Entry(
            parent, font=FONT_BODY, bg=BG, fg=TEXT,
            insertbackground=ACCENT, relief="flat",
            highlightthickness=1, highlightbackground=SUBTEXT,
            highlightcolor=ACCENT, width=28
        )
        entry.grid(row=row*2+1, column=0, sticky="ew", ipady=6)
        parent.columnconfigure(0, weight=1)
        return entry

    # ── Event Handlers ─────────────────────────────────────────

    def _on_calculate(self):
        """Validate inputs, run calculation, save to CSV, refresh table."""
        username = self.entry_username.get().strip()
        img_raw  = self.entry_img_size.get().strip()
        mag_raw  = self.entry_magnify.get().strip()

        # Validation
        if not username:
            return self._show_error("Username cannot be empty.")
        try:
            image_size  = float(img_raw)
            magnification = float(mag_raw)
        except ValueError:
            return self._show_error("Image size and magnification must be numbers.")

        try:
            actual = run_measurement(username, image_size, magnification)
        except ValueError as e:
            return self._show_error(str(e))

        # Update result label
        msg = f"✅  Actual Size = {actual:.6f} µm  ({actual*1000:.4f} nm)"
        self.result_var.set(msg)
        self.result_lbl.configure(fg=SUCCESS)
        self._refresh_table()

        # Clear numeric fields for next entry
        self.entry_img_size.delete(0, tk.END)
        self.entry_magnify.delete(0, tk.END)

    def _show_error(self, message: str):
        self.result_var.set(f"❌  {message}")
        self.result_lbl.configure(fg=ERROR)

    def _refresh_table(self):
        """Re-read the CSV and repopulate the Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not os.path.exists(CSV_FILE):
            return

        with open(CSV_FILE, newline="") as f:
            for record in csv.DictReader(f):
                self.tree.insert("", "end", values=(
                    record.get("timestamp", ""),
                    record.get("username", ""),
                    record.get("image_size_um", ""),
                    record.get("magnification", ""),
                    record.get("actual_size_um", ""),
                ))
        # Scroll to newest entry
        children = self.tree.get_children()
        if children:
            self.tree.see(children[-1])


# ── Entry Point ────────────────────────────────────────────────

if __name__ == "__main__":
    app = MicroscopeApp()
    app.mainloop()