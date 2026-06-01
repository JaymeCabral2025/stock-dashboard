import streamlit as st
from datetime import date
from data import carregar_dados, calcular_estatisticas, TICKERS, COLORS
from charts import plot_preco_historico, plot_performance_comparativa, plot_candlestick

st.set_page_config(
    page_title="Dashboard de Ações 2025",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Dashboard de Ações Brasileiras — 2025")
st.caption("Petrobras (PETR4) · Itaú (ITUB4) · Vale (VALE3)")

with st.sidebar:
    st.header("Filtros")
    opcao_periodo = st.radio(
        "Período",
        ["Ano todo (2025)", "Últimos 90 dias", "Últimos 30 dias"],
        index=0,
    )

hoje = date.today().isoformat()

if opcao_periodo == "Ano todo (2025)":
    inicio = "2025-01-01"
elif opcao_periodo == "Últimos 90 dias":
    from datetime import timedelta
    inicio = (date.today() - timedelta(days=90)).isoformat()
else:
    from datetime import timedelta
    inicio = (date.today() - timedelta(days=30)).isoformat()

with st.spinner("Carregando dados da B3..."):
    dados = carregar_dados(inicio, hoje)

# --- Cards de métricas ---
st.subheader("Resumo")
cols = st.columns(3)
for i, (ticker, nome) in enumerate(TICKERS.items()):
    df = dados[ticker]
    close = df["Close"].dropna()
    if close.empty:
        cols[i].metric(f"{nome}", "Sem dados")
        continue
    preco_atual = float(close.iloc[-1])
    preco_anterior = float(close.iloc[-2]) if len(close) > 1 else preco_atual
    variacao_dia = preco_atual - preco_anterior
    retorno_total = (preco_atual / float(close.iloc[0]) - 1) * 100
    cols[i].metric(
        label=f"{nome} ({ticker.replace('.SA', '')})",
        value=f"R$ {preco_atual:.2f}",
        delta=f"{variacao_dia:+.2f} hoje · {retorno_total:+.2f}% no período",
    )

st.divider()

# --- Abas de gráficos ---
aba1, aba2, aba3, aba4 = st.tabs([
    "📉 Preço Histórico",
    "🏆 Performance (%)",
    "🕯️ Candlestick",
    "📊 Estatísticas",
])

with aba1:
    st.plotly_chart(plot_preco_historico(dados), use_container_width=True)

with aba2:
    st.plotly_chart(plot_performance_comparativa(dados), use_container_width=True)

with aba3:
    ticker_selecionado = st.selectbox(
        "Selecione a ação",
        list(TICKERS.keys()),
        format_func=lambda t: f"{TICKERS[t]} ({t.replace('.SA', '')})",
    )
    st.plotly_chart(plot_candlestick(dados, ticker_selecionado), use_container_width=True)

with aba4:
    stats = calcular_estatisticas(dados)
    st.dataframe(
        stats.style.format({
            "Preço Atual (R$)": "R$ {:.2f}",
            "Mínimo (R$)": "R$ {:.2f}",
            "Máximo (R$)": "R$ {:.2f}",
            "Média (R$)": "R$ {:.2f}",
            "Volatilidade (%)": "{:.2f}%",
            "Retorno 2025 (%)": "{:+.2f}%",
        }),
        use_container_width=True,
    )
