# Finance Sandbox Pro

A responsive FinTech portfolio project with a React/Vite landing page and a standalone Streamlit financial analysis application.

## React portfolio

```bash
npm install
npm run dev
```

Open the local URL printed by Vite.

### Production build

```bash
npm run build
npm run preview
```

## Financial Analysis Studio (Streamlit Single App)

The `financial/` directory contains a standalone Streamlit app. It does not require FastAPI or a separate backend.

### Run on macOS

```bash
cd financial
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown in Terminal (normally http://localhost:8501).

### Features

- Five-year illustrative Income Statement and Balance Sheet dataset
- Current Ratio, Quick Ratio, Gross / Operating / Net Profit Margin
- ROA, ROE, D/E Ratio and Interest Coverage
- DuPont decomposition: Net Profit Margin × Asset Turnover × Equity Multiplier
- Thai-language dashboard, Plotly trends, KPI metrics and CSV export
- Simulated market signal terminal with 2–3 second refresh

## Project structure

- `src/App.jsx` — React landing page and portfolio content
- `src/index.css` — responsive FinTech design system
- `public/data/` — illustrative case-study datasets
- `public/templates/` — Excel-compatible CSV templates
- `financial/app.py` — complete Streamlit financial analysis app
- `financial/requirements.txt` — Python dependencies

## Deploy

React portfolio: import this repository into Vercel or Netlify with build command `npm run build` and output directory `dist`.

Streamlit app: deploy the `financial/app.py` entry point on Streamlit Community Cloud, setting the app path to `financial/app.py` and dependencies to `financial/requirements.txt`.

## Data disclaimer

All financial statements, ratios and market signals in the Streamlit app are illustrative educational data. They are not audited financial statements, live market data, investment recommendations or official forecasts. Validate assumptions against primary sources before using the model in professional analysis.
