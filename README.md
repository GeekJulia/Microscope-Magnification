# Microscope-Magnification
🔬 A multi-interface microscope specimen size calculator built with Python. Features a CLI, Tkinter desktop GUI, and Flask web app with live unit conversion (µm, nm, mm, m, pm). All interfaces share a common calculation engine and append results to a local CSV file.
# 🔬 Microscope Size Calculator — Student Project

## Project Structure

```
microscope_project/
│
├── core_logic.py        # Part A & B — Formula + CSV storage (shared module)
├── gui_tkinter.py       # Part C  — Desktop GUI (Tkinter)
├── web_streamlit.py     # Part D  — Web app (Streamlit)
├── requirements.txt     # Python dependencies
├── measurements.csv     # Auto-created on first run (not committed to Git)
└── README.md            # This file
```

---

## How to Run Each Part

### Part A & B — Core Logic (terminal demo)
```bash
python core_logic.py
```

### Part C — Desktop GUI
```bash
python gui_tkinter.py
```
> Tkinter ships with Python — no extra install needed.

### Part D — Web App
```bash
pip install -r requirements.txt
streamlit run web_streamlit.py
```
Opens automatically at http://localhost:8501

---

## Part E — Free Hosting Guide

### Option 1 — Streamlit Community Cloud (Easiest — Recommended)

**What it is:** Streamlit's own free hosting platform, purpose-built for Streamlit apps.  
**URL after deploy:** `https://<your-app-name>.streamlit.app`

#### Step-by-Step

1. **Push your project to GitHub**
   ```
   git init
   git add core_logic.py web_streamlit.py requirements.txt
   # Do NOT add measurements.csv — see storage note below
   echo "measurements.csv" >> .gitignore
   git commit -m "Initial commit"
   git remote add origin https://github.com/<you>/<repo>.git
   git push -u origin main
   ```

2. **Sign up / log in** at https://share.streamlit.io using your GitHub account.

3. **Click "New app"**  
   - Repository: your repo  
   - Branch: `main`  
   - Main file path: `web_streamlit.py`  
   - Click **Deploy**

4. **Done!** Streamlit builds the environment from `requirements.txt` automatically.

#### ⚠️ Important — File Storage on Free Tiers
> Free cloud platforms use **ephemeral (temporary) file systems**.  
> This means `measurements.csv` is created fresh each time the app restarts or redeploys,  
> and **all saved data is lost**.

**Workarounds for a student project:**

| Approach | Effort | Persistent? |
|---|---|---|
| Use the **Download CSV** button to save data locally before closing | None | Manual |
| Replace CSV with [Google Sheets API](https://docs.streamlit.io/develop/tutorials/databases/public-gsheet) | Low | ✅ Yes |
| Use [Supabase](https://supabase.com) free tier (PostgreSQL) | Medium | ✅ Yes |
| Use [Streamlit's `st.session_state`](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state) | Low | Per session only |

For a school demo, the **Download CSV button** approach is perfectly fine.

---

### Option 2 — Render (Alternative)

**What it is:** A general-purpose PaaS with a free web service tier.

#### Step-by-Step

1. Push code to GitHub (same as above).

2. Add a `Procfile` in your project root:
   ```
   web: streamlit run web_streamlit.py --server.port $PORT --server.address 0.0.0.0
   ```

3. Sign up at https://render.com and click **"New → Web Service"**.

4. Connect your GitHub repo, set:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** *(auto-read from Procfile)*
   - **Instance type:** Free

5. Click **Create Web Service** and wait ~3 minutes for the first build.

#### ⚠️ Same Storage Warning  
Render free tier also has an ephemeral disk — `measurements.csv` resets on restart.  
Use the same workarounds listed above.

---

## Formula Reference

```
Real Size (µm) = Image Size (µm) ÷ Magnification
```

| Image Size | Magnification | Actual Size |
|---|---|---|
| 2 mm (2000 µm) | 400× | 5 µm |
| 5 mm (5000 µm) | 100× | 50 µm |
| 0.5 mm (500 µm) | 1000× | 0.5 µm |