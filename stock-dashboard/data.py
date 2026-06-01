import streamlit as st
import yfinance as yf
import pandas as pd

TICKERS = {
    "PETR4.SA": "Petrobras",
    "ITUB4.SA": "Itaú",
    "VALE3.SA": "Vale",
}

COLORS = {
    "PETR4.SA": "#009B3A",
    "ITUB4.SA": "#EC7000",
    "VALE3.SA": "#005DAA",
}


@st.cache_data(ttl=3600)
def carregar_dados(periodo_inicio: str, periodo_fim: str) -> dict[str, pd.DataFrame]:
    dados = {}
    for ticker in TICKERS:
        df = yf.download(ticker, start=periodo_inicio, end=periodo_fim, progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.index = pd.to_datetime(df.index)
        df.index = df.index.tz_localize(None)
        dados[ticker] = df
    return dados


def calcular_retorno_acumulado(df: pd.DataFrame) -> pd.Series:
    close = df["Close"].dropna()
    if close.empty:
        return close
    return (close / close.iloc[0] - 1) * 100


def calcular_estatisticas(dados: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for ticker, nome in TICKERS.items():
        df = dados[ticker]
        close = df["Close"].dropna()
        if close.empty:
            continue
        retorno = (close.iloc[-1] / close.iloc[0] - 1) * 100
        rows.append({
            "Ação": f"{nome} ({ticker.replace('.SA', '')})",
            "Preço Atual (R$)": round(float(close.iloc[-1]), 2),
            "Mínimo (R$)": round(float(close.min()), 2),
            "Máximo (R$)": round(float(close.max()), 2),
            "Média (R$)": round(float(close.mean()), 2),
            "Volatilidade (%)": round(float(close.pct_change().std() * 100), 2),
            "Retorno 2025 (%)": round(float(retorno), 2),
        })
    return pd.DataFrame(rows).set_index("Ação")
