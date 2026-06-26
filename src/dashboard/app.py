import streamlit as st
import pandas as pd
import plotly.express as px

# ================= CONFIG =================
st.set_page_config(
    page_title="RetailMax Executive Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DATA_PATH = "/home/hadoop/data/kpi_sales.csv"

# Paleta corporativa clara
COLORS = {
    "primary": "#2563EB",     # azul corporativo
    "secondary": "#0EA5E9",   # azul cielo
    "accent": "#F59E0B",      # ámbar
    "success": "#10B981",     # verde
    "danger": "#EF4444",      # rojo
    "purple": "#8B5CF6",
    "bg": "#F8FAFC",
    "card": "#FFFFFF",
    "text": "#0F172A",        # casi negro, para máximo contraste en ejes/etiquetas
    "muted": "#475569",       # gris medio (NO gris claro) para texto secundario
    "border": "#E2E8F0",
}

PALETTE = ["#2563EB", "#0EA5E9", "#8B5CF6", "#F59E0B", "#10B981", "#EF4444", "#EC4899", "#14B8A6"]

# ================= ESTILOS =================
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {COLORS['bg']};
        }}
        .block-container {{
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }}
        .dashboard-header {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
            padding: 1.3rem 1.8rem;
            border-radius: 14px;
            margin-bottom: 1.2rem;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.18);
        }}
        .dashboard-header h1 {{
            color: white;
            font-size: 1.6rem;
            font-weight: 700;
            margin: 0;
        }}
        .dashboard-header p {{
            color: rgba(255,255,255,0.92);
            margin: 0.2rem 0 0 0;
            font-size: 0.9rem;
        }}
        .kpi-card {{
            background: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            padding: 1.1rem 1.3rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            border-left: 4px solid {COLORS['primary']};
        }}
        .kpi-label {{
            color: {COLORS['muted']};
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }}
        .kpi-value {{
            color: {COLORS['text']};
            font-size: 1.8rem;
            font-weight: 700;
            margin-top: 0.2rem;
        }}
        .chart-card {{
            background: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            padding: 1rem 1.2rem 0.4rem 1.2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            margin-bottom: 1rem;
        }}
        .chart-title {{
            color: {COLORS['text']};
            font-size: 0.95rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- Estilo de ejes forzado: evita el gris claro por defecto de Plotly ----
AXIS_STYLE = dict(
    color=COLORS["text"],
    tickfont=dict(color=COLORS["text"], size=12),
    title_font=dict(color=COLORS["text"], size=12),
    gridcolor=COLORS["border"],
    linecolor=COLORS["muted"],
    zerolinecolor=COLORS["muted"],
    showline=True,
)

BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=COLORS["text"], family="Arial, sans-serif", size=12),
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(
        orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5,
        font=dict(color=COLORS["text"], size=11),
    ),
)


def style_fig(fig, height=300, show_legend=None):
    """Aplica el layout base y refuerza el color de ejes, ticks, etiquetas de
    categoría, colorbar y texto interno (pie/heatmap) en TODOS los subejes que
    Plotly genere, para evitar el gris claro por defecto."""
    layout_kwargs = dict(BASE_LAYOUT, height=height)
    if show_legend is not None:
        layout_kwargs["showlegend"] = show_legend
    fig.update_layout(**layout_kwargs)
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    fig.update_coloraxes(colorbar=dict(tickfont=dict(color=COLORS["text"])))
    return fig


# ================= LOAD DATA =================
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors="coerce")
    df["discount_pct"] = pd.to_numeric(df["discount_pct"], errors="coerce")
    return df


df = load_data()

# ================= HEADER =================
st.markdown(
    """
    <div class="dashboard-header">
        <h1>📊 RetailMax — Executive Analytics Dashboard</h1>
        <p>Resumen ejecutivo de ventas, descuentos y comportamiento de clientes</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ================= FILTROS (opcional, sobre region si existe) =================
if "region" in df.columns:
    regiones = ["Todas"] + sorted(df["region"].dropna().unique().tolist())
    sel_region = st.selectbox("Filtrar por región", regiones, label_visibility="collapsed")
    if sel_region != "Todas":
        df = df[df["region"] == sel_region]

# ================= KPIs =================
k1, k2, k3, k4 = st.columns(4)

kpi_data = [
    ("💰 VENTAS TOTALES", f"S/ {df['sales_amount'].sum():,.0f}"),
    ("🧾 TICKET PROMEDIO", f"S/ {df['sales_amount'].mean():,.2f}"),
    ("🏷️ DESCUENTO PROMEDIO", f"{df['discount_pct'].mean():.2f}%"),
    ("📦 TOTAL TRANSACCIONES", f"{len(df):,}"),
]

for col, (label, value) in zip([k1, k2, k3, k4], kpi_data):
    col.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# ================= FILA 1: Categoría (dona) | Región (barras) | Tendencia (línea) =================
row1 = st.columns([1, 1, 1.3])

with row1[0]:
    st.markdown('<div class="chart-card"><div class="chart-title">📦 Ventas por Categoría</div>', unsafe_allow_html=True)
    cat = df.groupby("category")["sales_amount"].sum().sort_values(ascending=False).reset_index()
    fig = px.pie(cat, names="category", values="sales_amount", hole=0.55, color_discrete_sequence=PALETTE)
    fig.update_traces(
        textinfo="percent+label",
        textfont=dict(color=COLORS["text"], size=11),
        outsidetextfont=dict(color=COLORS["text"]),
    )
    style_fig(fig, height=300, show_legend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with row1[1]:
    st.markdown('<div class="chart-card"><div class="chart-title">📍 Ventas por Región</div>', unsafe_allow_html=True)
    reg = df.groupby("region")["sales_amount"].sum().sort_values(ascending=True).reset_index()
    fig = px.bar(reg, x="sales_amount", y="region", orientation="h", color_discrete_sequence=[COLORS["primary"]])
    style_fig(fig, height=300)
    fig.update_layout(xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with row1[2]:
    st.markdown('<div class="chart-card"><div class="chart-title">📈 Tendencia de Ventas</div>', unsafe_allow_html=True)
    date_col = next((c for c in ["date", "order_date", "sale_date", "fecha"] if c in df.columns), None)
    if date_col:
        tmp = df.copy()
        tmp[date_col] = pd.to_datetime(tmp[date_col], errors="coerce")
        trend = tmp.groupby(tmp[date_col].dt.to_period("M"))["sales_amount"].sum().reset_index()
        trend[date_col] = trend[date_col].astype(str)
        fig = px.line(trend, x=date_col, y="sales_amount", markers=True,
                       color_discrete_sequence=[COLORS["secondary"]])
    else:
        reg_trend = df.groupby("region")["sales_amount"].sum().reset_index()
        fig = px.line(reg_trend, x="region", y="sales_amount", markers=True,
                       color_discrete_sequence=[COLORS["secondary"]])
    fig.update_traces(line_width=3, marker_size=8)
    style_fig(fig, height=300)
    fig.update_layout(xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= FILA 2: Canal (área) | Segmento (dona) | Top Productos =================
row2 = st.columns([1, 1, 1.3])

with row2[0]:
    st.markdown('<div class="chart-card"><div class="chart-title">🛒 Ventas por Canal</div>', unsafe_allow_html=True)
    ch = df.groupby("sales_channel")["sales_amount"].sum().reset_index()
    fig = px.area(ch, x="sales_channel", y="sales_amount", color_discrete_sequence=[COLORS["accent"]])
    fig.update_traces(line_width=2)
    style_fig(fig, height=300)
    fig.update_layout(xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with row2[1]:
    st.markdown('<div class="chart-card"><div class="chart-title">👥 Segmento de Cliente</div>', unsafe_allow_html=True)
    seg = df.groupby("customer_segment")["sales_amount"].sum().reset_index()
    fig = px.pie(seg, names="customer_segment", values="sales_amount", hole=0.55, color_discrete_sequence=PALETTE)
    fig.update_traces(
        textinfo="percent+label",
        textfont=dict(color=COLORS["text"], size=11),
        outsidetextfont=dict(color=COLORS["text"]),
    )
    style_fig(fig, height=300, show_legend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with row2[2]:
    st.markdown('<div class="chart-card"><div class="chart-title">🏆 Top 10 Productos</div>', unsafe_allow_html=True)
    top = (
        df.groupby("product_name")["sales_amount"]
        .sum()
        .sort_values(ascending=True)
        .tail(10)
        .reset_index()
    )
    fig = px.bar(top, x="sales_amount", y="product_name", orientation="h",
                 color="sales_amount", color_continuous_scale="Blues")
    style_fig(fig, height=300)
    fig.update_layout(xaxis_title=None, yaxis_title=None, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= FILA 3: Métodos de pago (dona) | Heatmap descuentos | Grupo edad =================
row3 = st.columns([1, 1.3, 1])

with row3[0]:
    st.markdown('<div class="chart-card"><div class="chart-title">💳 Métodos de Pago</div>', unsafe_allow_html=True)
    payment = df.groupby("payment_method")["sales_amount"].sum().reset_index()
    fig = px.pie(payment, names="payment_method", values="sales_amount", hole=0.55, color_discrete_sequence=PALETTE)
    fig.update_traces(
        textinfo="percent+label",
        textfont=dict(color=COLORS["text"], size=11),
        outsidetextfont=dict(color=COLORS["text"]),
    )
    style_fig(fig, height=300, show_legend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with row3[1]:
    st.markdown('<div class="chart-card"><div class="chart-title">📊 Descuento Promedio: Categoría × Canal</div>', unsafe_allow_html=True)
    pivot = df.pivot_table(
        index="category", columns="sales_channel", values="discount_pct", aggfunc="mean"
    )
    fig = px.imshow(
        pivot,
        text_auto=".1f",
        color_continuous_scale="Blues",
        aspect="auto",
    )
    fig.update_traces(textfont=dict(color=COLORS["text"], size=12))
    style_fig(fig, height=300)
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with row3[2]:
    st.markdown('<div class="chart-card"><div class="chart-title">🎂 Ventas por Grupo de Edad</div>', unsafe_allow_html=True)
    age = df.groupby("customer_age_group")["sales_amount"].sum().reset_index()
    fig = px.bar(age, x="customer_age_group", y="sales_amount", color_discrete_sequence=[COLORS["purple"]])
    style_fig(fig, height=300)
    fig.update_layout(xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= TABLA DETALLE TOP PRODUCTOS =================
with st.expander("📋 Ver detalle de Top 10 Productos"):
    top_detail = (
        df.groupby("product_name")["sales_amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    top_detail.columns = ["Producto", "Ventas (S/)"]
    st.dataframe(top_detail, use_container_width=True, hide_index=True)