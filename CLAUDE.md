# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A Streamlit dashboard for Brazilian stock market data (B3), tracking Petrobras (PETR4), Itaú (ITUB4), and Vale (VALE3) via Yahoo Finance.

## Commands

All commands should be run from inside `stock-dashboard/`.

```powershell
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

## Architecture

Three-file layout with a clear separation of concerns:

- **`data.py`** — data layer. Defines `TICKERS` and `COLORS` dicts (the single source of truth for which stocks are tracked). `carregar_dados()` fetches OHLCV data from Yahoo Finance via `yfinance` and is cached with `@st.cache_data(ttl=3600)` to avoid redundant API calls within an hour.
- **`charts.py`** — presentation layer. Pure functions that accept the `dados` dict (returned by `carregar_dados`) and return Plotly `Figure` objects. Imports `TICKERS`, `COLORS`, and `calcular_retorno_acumulado` from `data.py`.
- **`app.py`** — Streamlit entrypoint. Owns all UI state (sidebar period filter, tab selection, ticker selectbox), calls `data.py` to load data, and passes results to `charts.py` functions for rendering.

**Adding a new stock:** add it to `TICKERS` and `COLORS` in `data.py` — no changes needed elsewhere.

**Period filtering** is date-string based (`YYYY-MM-DD`); `app.py` computes `inicio`/`hoje` strings and passes them to `carregar_dados`.

**yfinance quirk:** when downloading multiple tickers, columns come back as a `MultiIndex`; `carregar_dados` flattens this with `get_level_values(0)` and strips timezone info from the index so Plotly handles dates correctly.
