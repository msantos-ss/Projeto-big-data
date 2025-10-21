import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud

# ===================== CONFIGURAÇÃO =====================
st.set_page_config(page_title="Dashboard Restaurante", layout="wide")
sns.set(style="whitegrid", palette="muted")

# ===================== LISTA DE MESES =====================
meses_oficiais = [
    "janeiro","fevereiro","março","abril","maio","junho",
    "julho","agosto","setembro","outubro","novembro","dezembro"
]

# ===================== CARREGAR DADOS =====================
@st.cache_data
def carregar_dados():
    df = pd.read_csv("vendas_restaurante_2024_2025.csv", parse_dates=["data"])
    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month.apply(lambda x: meses_oficiais[x-1])  # <-- FIX
    df["hora"] = df["data"].dt.hour
    return df

df = carregar_dados()

st.title("📊 Dashboard de Vendas — Restaurante & Pizzaria")
st.markdown("Análise de dados simulados de um restaurante com almoço e pizzas à noite (2023–2025).")

# ===================== FILTROS =====================
col1, col2, col3 = st.columns([1,1,1])

# Opção 'Todos' no filtro de anos
anos_disponiveis = sorted(df["ano"].unique())
anos_opcoes = ["Todos"] + [str(ano) for ano in anos_disponiveis]
with col1:
    ano_filtro = st.selectbox("Selecione o ano:", options=anos_opcoes)

# Se "Todos" foi selecionado, considerar todos os dados
if ano_filtro == "Todos":
    df_ano = df.copy()
else:
    df_ano = df[df["ano"] == int(ano_filtro)]

# Meses disponíveis para o ano(s) selecionado(s)
meses_disponiveis = sorted(df_ano["mes"].unique(), key=lambda x: meses_oficiais.index(x))
with col2:
    mes_filtro = st.selectbox("Selecione o mês:", options=["Todos"] + meses_disponiveis)
with col3:
    periodo_filtro = st.selectbox("Selecione o período:", options=["Todos", "Dia", "Noite"])

# Aplicar filtros
df_filtrado = df_ano.copy()
if mes_filtro != "Todos":
    df_filtrado = df_filtrado[df_filtrado["mes"] == mes_filtro]
if periodo_filtro != "Todos":
    df_filtrado = df_filtrado[df_filtrado["periodo"] == periodo_filtro]

# ===================== MÉTRICAS GERAIS =====================
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Faturamento Total", f"R$ {df_filtrado['valor_total'].sum():,.2f}")
col2.metric("🧾 Nº de Vendas", f"{len(df_filtrado):,}")
col3.metric("⭐ Avaliação Média", f"{df_filtrado['avaliacao'].mean():.2f}")
col4.metric("❌ Pedidos Cancelados", f"{df_filtrado['cancelado'].sum()}")

# ===================== GRÁFICOS =====================
st.markdown("---")
st.header("📈 Análises Gerais")

# --- Gênero dos Clientes ---
fig, ax = plt.subplots(figsize=(5,4))
sns.countplot(data=df_filtrado, x="sexo", palette="pastel", ax=ax)
ax.set_title("Distribuição de Clientes por Gênero")
ax.set_xlabel("Gênero")
ax.set_ylabel("Quantidade")
st.pyplot(fig)

# --- Formas de Pagamento ---
formas_pgto = df_filtrado["forma_pagamento"].value_counts(normalize=True) * 100
fig, ax = plt.subplots(figsize=(5,5))
ax.pie(formas_pgto, labels=formas_pgto.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set3"))
ax.set_title("💳 Porcentagem das Formas de Pagamento")
st.pyplot(fig)

# --- Avaliações ---
fig, ax = plt.subplots(figsize=(6,4))
sns.countplot(data=df_filtrado, x="avaliacao", palette="mako", ax=ax, order=sorted(df_filtrado['avaliacao'].unique()))
ax.set_title("⭐ Distribuição das Avaliações")
ax.set_xlabel("Nota de Avaliação (1 a 5)")
ax.set_ylabel("Quantidade")
st.pyplot(fig)

# ===================== SEÇÃO: PIZZAS =====================
st.markdown("---")
st.header("🍕 Análise de Vendas de Pizzas")

pizzas = df_filtrado[df_filtrado["tipo_cardapio"].str.contains("pizza", case=False, na=False)]
if len(pizzas) > 0:
    pizza_counts = pizzas["prato"].value_counts()

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(6,4))
        sns.barplot(x=pizza_counts.values, y=pizza_counts.index, palette="rocket", ax=ax)
        ax.set_title("Sabores de Pizza Mais Vendidos")
        ax.set_xlabel("Quantidade")
        ax.set_ylabel("Sabores")
        st.pyplot(fig)
    with col2:
        pizza_percent = (pizza_counts / pizza_counts.sum()) * 100
        fig, ax = plt.subplots(figsize=(5,5))
        ax.pie(pizza_percent, labels=pizza_percent.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
        ax.set_title("Porcentagem de Vendas por Sabor")
        st.pyplot(fig)
else:
    st.info("Nenhuma venda de pizza para o filtro selecionado.")

# ===================== SEÇÃO: TEMPO E FATURAMENTO =====================
st.markdown("---")

# Horário de pico
# ===================== HORÁRIO DE PICO (VERSÃO MELHORADA) =====================
st.markdown("---")
st.header("⏰ Horário de Pico de Vendas")

# Contagem de vendas por hora
vendas_por_hora = df_filtrado.groupby("hora")["valor_total"].count().reset_index()
vendas_por_hora.rename(columns={"valor_total": "qtd_vendas"}, inplace=True)

fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(data=vendas_por_hora, x="hora", y="qtd_vendas", color="#2E86C1", linewidth=3, marker="o")

ax.set_title("⏰ Horários com Mais Vendas", fontsize=14, weight="bold")
ax.set_xlabel("Hora do Dia", fontsize=12)
ax.set_ylabel("Quantidade de Vendas", fontsize=12)
ax.set_xticks(range(11, 24))
ax.grid(True, linestyle="--", alpha=0.4)

# Destacar o horário de maior movimento
hora_pico = vendas_por_hora.loc[vendas_por_hora["qtd_vendas"].idxmax()]
ax.axvline(hora_pico["hora"], color="red", linestyle="--", alpha=0.7)
ax.text(hora_pico["hora"], hora_pico["qtd_vendas"]+5, f"Pico às {int(hora_pico['hora'])}h", 
        color="red", ha="center", fontsize=10, weight="bold")

st.pyplot(fig)


# Faturamento por mês (para o ano e filtro selecionado)
if mes_filtro == "Todos":
    vendas_mes = df_filtrado.groupby("mes")["valor_total"].sum()
    vendas_mes = vendas_mes.reindex(meses_oficiais).dropna()
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x=vendas_mes.index.str.capitalize(), y=vendas_mes.values, palette="flare", ax=ax)
    ax.set_title("📅 Faturamento Total por Mês")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Faturamento (R$)")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

# Rendimento anual (comparativo geral - todos os anos)
# Rendimento anual (comparativo geral - todos os anos)
vendas_ano = df.groupby("ano")["valor_total"].sum()

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(
    x=vendas_ano.index.astype(str),
    y=vendas_ano.values,
    palette="crest",
    ax=ax
)

ax.set_title("💰 Rendimento Total por Ano", fontsize=14, weight="bold")
ax.set_xlabel("Ano", fontsize=12)
ax.set_ylabel("Faturamento (R$)", fontsize=12)

# Formatar eixo Y como valores monetários legíveis (ex: R$ 100.000)
import matplotlib.ticker as mticker
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('R$ {x:,.0f}'))

# Mostrar valores exatos acima das barras
for i, v in enumerate(vendas_ano.values):
    ax.text(i, v + (v * 0.01), f"R$ {v:,.0f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

st.pyplot(fig)


# ===================== SEÇÃO: WORDCLOUD =====================
st.markdown("---")
st.header("☁️ WordCloud — Palavras Relacionadas ao Restaurante")

palavras = """
restaurante comida almoço jantar prato refeição sabor pizza pudim mousse lasanha parmegiana
batata feijão arroz suco refrigerante sobremesa atendimento cliente garçons delivery cozinha
gastronomia culinária cardápio experiência saborosa ambiente agradável bebida sobremesa
massa queijo carne frango peixe sobremesa satisfação qualidade custo-benefício família amigos
rodízio porção combo lanche artesanal forno tradicional italiano brasileiro tempero caseiro
"""

wordcloud = WordCloud(width=900, height=500, background_color='white', colormap='plasma').generate(palavras)
fig, ax = plt.subplots(figsize=(10,5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

st.markdown("Desenvolvido para fins acadêmicos — Projeto Big Data 🍽️")
