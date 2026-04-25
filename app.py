import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import plotly.colors as pc
import os

st.set_page_config(
    page_title="Product Optimization & Revenue Contribution Analysis for Afficionado Coffee Roasters",
    page_icon="☕",
    layout="wide",
)

bg_main = "#F5EFE6"  # light cream (main background)
bg_card = "#A8785B"  # your brown (cards)
bg_plot = "#FBF7F2"  # slightly off-white (charts)

text_color = "#2E2E2E"  # dark readable text
grid_color = "#D6CFC7"  # soft grid

accent = "#6F4E37"  # coffee brown (lines)
accent2 = "#C58940"  # caramel highlight
accent3 = "#5C7AEA"  # soft contrast blue

sidebar_bg = "#8B5E3C"

# ====== Mobile-specific ==========
st.markdown(
    """
<style>

/* MOBILE FIX */
@media (max-width: 768px) {
    @media (max-width: 768px) {

    /* Main content text */
    .stApp {
        color: #2E2E2E !important;
    }

    /* Sidebar stays white */
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* KPI text stays white */
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"] {
        color: #FFFFFF !important;
    }
}
}

</style>
""",
    unsafe_allow_html=True,
)
st.markdown(
    f"""
<style>

/* FORCE TEXT COLOR FIX */
html, body, [class*="css"] {{
    color: {text_color} !important;
}}

/* Fix markdown + labels */
p, span, label, div {{
    color: {text_color} !important;
}}
/* MAIN BACKGROUND */
.stApp {{
    background-color: {bg_main};
}}

[data-testid="stAppViewContainer"] {{
    background-color: {bg_main};
}}

[data-testid="stHeader"] {{
    background-color: {bg_main};
}}

/* SIDEBAR */
section[data-testid="stSidebar"] {{
    background-color: {sidebar_bg};
}}

section[data-testid="stSidebar"] * {{
    color: #FFFFFF !important;
}}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] p {{
    color: #FFFFFF !important;
}}

/* MULTISELECT TAGS 
[data-baseweb="tag"] {{
    background-color: {sidebar_bg} !important;  /* forest green */
    color: #F5F5F5 ;
}}*/

[data-baseweb="tag"] {{
    background-color: {bg_card} !important;  /* your green */
    color: white !important;
    border-radius: 8px;
}}

.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {{
    background-color: #8F6A52 !important;   /* light green */
    color: #FFFFFF !important;
    border-radius: 10px;
    border: 1px solid #A07A61;
}}

div[data-baseweb="select"] {{
    background-color: #9C755C !important;  /* beige tone */
    border: 1px solid #B0896F;
}}

/* KPI CARDS 
[data-testid="stMetric"] * {{
    background-color: {bg_card};
    color:white !important;
    padding: 12px;
    border-radius: 16px;
    border: 1px solid rgba(0,0,0,0.1);
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}}*/

[data-testid="stMetric"] {{
    background-color: #A8785B !important;
    border-radius: 16px;
    padding: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}}

/* Label (title) */
[data-testid="stMetricLabel"] {{
    color: #F5EFE6 !important;
    font-weight: 500;
}}

/* Value (big number) */
[data-testid="stMetricValue"] {{
    color: #FFFFFF !important;
    font-weight: 500 !important;   /* 👈 normal */
    font-size: 20px !important;    /* optional: slightly smaller */
}}

/* Delta (if any) */
[data-testid="stMetricDelta"] {{
    color: #D1FAE5 !important;
}}

/* TEXT */
h1, h2, h3, h4 {{
    color: {text_color};
}}

</style>
""",
    unsafe_allow_html=True,
)


def insight_card(title, content, color="#C58940"):
    st.markdown(
        f"""
        <div style="
            background:{bg_card};
            padding:18px;
            border-radius:16px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
            border-left: 6px solid {color};
            margin-top:10px;
        ">
            <div style="
                font-size:18px;
                font-weight:600;
                margin-bottom:8px;
                color:{text_color};
            ">
                {title}
            </div>
            <div style="
    font-size:15px;
    line-height:1.7;
    color:{text_color};
">
    {content}
</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -------- TITLE --------
st.title(
    "☕ Product Optimization & Revenue Contribution Analysis for Afficionado Coffee Roasters"
)
st.markdown("---")

plt.rcParams.update({"axes.titlesize": 14, "axes.labelsize": 11})

# ===== APPLY GLOBAL DARK THEME (FIXED) =====
plt.style.use("default")

plt.rcParams.update(
    {
        "figure.facecolor": bg_card,
        "axes.facecolor": bg_plot,
        "axes.edgecolor": bg_plot,
        "axes.labelcolor": text_color,
        "xtick.color": text_color,
        "ytick.color": text_color,
        "text.color": text_color,
        "axes.titlecolor": text_color,
        "grid.color": grid_color,
        "savefig.facecolor": bg_card,
        "savefig.transparent": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.spines.bottom": False,
        "axes.titlesize": 11,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
    }
)  # box-shadow: 0 6px 14px rgba(0,0,0,0.15);

# ---------------- LOAD DATA ----------------

try:
    file_path = os.path.join(
        os.path.dirname(__file__), "Afficionado Coffee Roasters.xlsx"
    )
    df = pd.read_excel(file_path)
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()


if df.empty:
    st.error("🚨 Data became empty after time parsing. Check your time format.")
    st.stop()

df["Revenue"] = df["transaction_qty"] * df["unit_price"]

# Detect if time is numeric (Excel format)
if np.issubdtype(df["transaction_time"].dtype, np.number):

    df["transaction_time"] = pd.to_timedelta(df["transaction_time"], unit="D")

    # Convert to datetime (attach dummy date)
    df["transaction_time"] = pd.to_datetime("1900-01-01") + df["transaction_time"]

else:
    df["transaction_time"] = pd.to_datetime(df["transaction_time"], errors="coerce")

# Now drop nulls
df = df.dropna(subset=["transaction_time"])

# Extract hour
df["Hour"] = df["transaction_time"].dt.hour


# # ---------------- CLEAN TIME (ROBUST FIX) ----------------

# df["transaction_time"] = df["transaction_time"].astype(str).str.strip()

# df["transaction_time"] = pd.to_datetime(
#     df["transaction_time"], format="%H:%M:%S", errors="coerce"
# )

# # Check how many rows failed
# null_time = df["transaction_time"].isna().sum()
# st.write(f"⚠ Failed time parsing rows: {null_time}")

# # Drop only if reasonable
# valid_rows = df["transaction_time"].notna().sum()
# st.write(f"✅ Valid time rows: {valid_rows}")

# if valid_rows == 0:
#     st.error("🚨 Time parsing failed completely. Check format.")
#     st.stop()

# df = df.dropna(subset=["transaction_time"])

# st.write("✅ Rows after time cleaning:", len(df))

# # ---------------- FEATURE ENGINEERING ----------------

# df["Hour"] = df["transaction_time"].dt.hour

# ---------------- NOW FILTER ----------------
filtered_df = df.copy()

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🔎 Filters")
    selected_category = st.multiselect(
        "Select Category",
        df["product_category"].dropna().unique(),
        default=filtered_df["product_category"].dropna().unique(),
        help="Filters are dependent on previous selections",
    )

    if selected_category:
        filtered_df = filtered_df[
            filtered_df["product_category"].isin(selected_category)
        ]

    top_n = st.slider("Top N Products", 5, 20, 10)

    selected_type = st.multiselect(
        "Select Product Type",
        filtered_df["product_type"].dropna().unique(),
        default=filtered_df["product_type"].dropna().unique(),
        help="Options update based on selected category",
    )
    if selected_type:
        filtered_df = filtered_df[filtered_df["product_type"].isin(selected_type)]

    selected_location = st.multiselect(
        "Select Store Location",
        filtered_df["store_location"].dropna().unique(),
        default=filtered_df["store_location"].dropna().unique(),
    )
    if selected_location:
        filtered_df = filtered_df[filtered_df["store_location"].isin(selected_location)]


if filtered_df.empty:
    st.warning("No data available. Please adjust filters.")
    st.stop()

metric_choice = st.radio("Rank By", ["Revenue", "Quantity"], horizontal=True)

if metric_choice == "Revenue":
    metric = "Revenue"
else:
    metric = "transaction_qty"

top_rev_series = (
    filtered_df.groupby("product_detail")[metric]
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
)
top_rev_type = (
    filtered_df.groupby("product_type")[metric]
    .sum()
    .sort_values(ascending=False)
    .head(top_n)
)

product_summary = (
    filtered_df.groupby(["product_detail", "product_category", "product_type"])
    .agg(Sales=("transaction_qty", "sum"), Revenue=("Revenue", "sum"))
    .reset_index()
)

# ================= METRICS =================
total_revenue = filtered_df["Revenue"].sum()

product_rev = filtered_df.groupby("product_detail")["Revenue"].sum()
product_comp = filtered_df.groupby("product_detail")[metric].sum()
top_product = product_comp.idxmax()
worst_product = product_comp.idxmin()

top_product_share = (product_rev.max() / total_revenue) * 100
sales_vol = filtered_df["transaction_qty"].sum()

# category_share = (
#     filtered_df.groupby("product_category")["Revenue"].sum() / df["Revenue"].sum()
# ).sum() * 100

category_share = (filtered_df["Revenue"].sum() / df["Revenue"].sum()) * 100
product_rev_full = (
    df.groupby("product_detail")["Revenue"].sum().sort_values(ascending=False)
)
cum = (product_rev_full / product_rev_full.sum()).cumsum()
top_80 = (cum <= 0.8).sum()
concentration = (top_80 / len(product_rev_full)) * 100

pro_rev = filtered_df.groupby("product_detail")["Revenue"].sum()
pro_sales = filtered_df.groupby("product_detail")["transaction_qty"].sum()
efficiency_score = total_revenue / sales_vol if sales_vol != 0 else 0


def show_kpis():
    col1, col2, col3, col4, col5 = st.columns(5, gap="small")
    col1.metric("Top Product Share (%)", f"{top_product_share:.2f}%")
    col2.metric("Sales Volume", int(sales_vol))
    col3.metric("Revenue Share (%)", f"{category_share:.2f}%")
    col4.metric("Concentration (%)", f"{concentration:.2f}%")
    col5.metric("Revenue per Unit ", f"{efficiency_score:.2f}")


# ================= TABS =================
tab1, tab2, tab3 = st.tabs(
    ["📊 Business Overview", "📈 Time & Demand Analysis", "📦 Product Intelligence"]
)

# ================= OVERVIEW =================
with tab1:
    show_kpis()

    st.markdown("## 🧁 Category Distribution")

    rev_cat = (
        filtered_df.groupby("product_category")
        .agg(
            Revenue=("Revenue", "sum"),
            Orders=("transaction_qty", "sum"),  # 👈 THIS WAS MISSING
        )
        .reset_index()
    )

    rev_cat.columns = ["Category", "Revenue", "Orders"]
    rev_cat["Perc"] = (rev_cat["Revenue"] / rev_cat["Revenue"].sum()) * 100

    small = rev_cat[rev_cat["Perc"] < 2]
    large = rev_cat[rev_cat["Perc"] >= 2]
    if len(small) > 1:
        large = pd.concat(
            [
                large,
                pd.DataFrame(
                    [["Others", small["Revenue"].sum(), small["Orders"].sum()]],
                    columns=["Category", "Revenue", "Orders"],
                ),
            ]
        )
    else:
        large = pd.concat([large, small])

    large["Perc"] = (large["Revenue"] / large["Revenue"].sum()) * 100

    final = large.set_index("Category")["Revenue"]

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_facecolor(bg_card)
    fig.patch.set_facecolor(bg_card)

    wedges, texts, autotexts = ax.pie(
        final.values,
        labels=final.index,
        autopct="%1.1f%%",
        colors=["#6F4E37", "#C58940", "#A8785B", "#D9A066", "#8B5E3C", "#E6B89C"],
        startangle=140,
        pctdistance=0.8,  # 🔥 FIX POSITION OF %
        labeldistance=1.05,  # 🔥 FIX LABEL POSITION
        wedgeprops=dict(width=0.4),
        textprops={"color": text_color, "fontsize": 11},
    )

    # ---- CENTER TEXT (Premium Look) ----

    total = final.sum()

    for autotext in autotexts:
        autotext.set_color(text_color)
        autotext.set_fontsize(11)

    for text in texts:
        text.set_fontsize(11)

    for w in wedges:
        w.set_edgecolor(bg_main)
    ax.tick_params(colors=text_color)

    ax.set_title("Revenue by Category", color=text_color, fontsize=10)
    plt.tight_layout(pad=1.5)
    st.container()
    st.pyplot(fig, use_container_width=True)
    for text in texts:
        text.set_color(text_color)

    # ================= TIME ANALYSIS =================

    # ================= DYNAMIC HOURLY REVENUE =================

    st.markdown("## ⏱ Revenue by Hour")

    # -------- DATA PREP --------
    hourly = filtered_df.groupby("Hour")["Revenue"].sum().sort_index()

    # Remove empty hours (important)
    hourly = hourly[hourly > 0]

    # -------- BUILD PLOTLY CHART --------

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=hourly.index,
            y=hourly.values,
            mode="lines+markers",
            line=dict(
                color="#F5EFE6", width=2  # thinner line (reduced by 1 as you asked)
            ),
            marker=dict(size=5, color="#C58940"),
            fill="tozeroy",
            fillcolor="rgba(111,78,55,0.25)",
            hovertemplate="<b>Hour:</b> %{x}<br>"
            + "<b>Revenue:</b> ₹%{y:,.0f}<extra></extra>",
        )
    )

    # -------- STYLING --------

    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor=bg_card,  # OUTER BG (no white)
        plot_bgcolor=bg_card,  # INNER BG (no white)
        font=dict(color=text_color),
        xaxis=dict(
            title=dict(text="Hour", font=dict(size=13, color="#F5EFE6")),
            tickmode="linear",
            dtick=1,
            showgrid=False,
            tickfont=dict(color=text_color),
        ),
        yaxis=dict(
            title=dict(text="Revenue", font=dict(size=13, color="#F5EFE6")),
            showgrid=True,
            gridcolor=grid_color,
            tickfont=dict(color=text_color),
        ),
        hovermode="x unified",  # smooth dynamic hover
    )

    st.plotly_chart(fig, use_container_width=True)

    # ========== INSIGHTS ==========

    peak_hour = hourly.idxmax()
    low_hour = hourly.idxmin()

    # ---- KPI STYLE INSIGHTS
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
        <div style="
            background:{bg_card};
            padding:14px 18px;
            border-radius:14px;
            display:flex;
            align-items:center;
            gap:10px;
            box-shadow: 0 6px 16px rgba(0,0,0,0.12);
            border-left:5px solid #2A9D8F;
        ">
            <div style="font-size:22px">📈</div>
            <div style="color:{text_color}; font-size:15px;;font-weight:500">
                <b>Peak Hour:</b> {peak_hour}:00
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div style="
            background:{bg_card};
            padding:14px 18px;
            border-radius:14px;
            display:flex;
            align-items:center;
            gap:10px;
            box-shadow: 0 6px 16px rgba(0,0,0,0.12);
            border-left:5px solid #9C2F2F;
        ">
            <div style="font-size:22px;">📉</div>
            <div style="color:{text_color}; font-size:14px;">
                <b>Lowest Hour:</b> {low_hour}:00
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-bottom:25px;'></div>", unsafe_allow_html=True)

    # ------------------ tree -------------------

    st.markdown("## 📊 Revenue Contribution Tree")

    tree_df = (
        filtered_df.groupby(["product_category", "product_type"])["Revenue"]
        .sum()
        .reset_index()
    )

    fig = px.treemap(
        tree_df,
        path=["product_category", "product_type"],
        values="Revenue",
        color="Revenue",
        color_continuous_scale=["#FBF7F2", "#E6B89C", "#C58940", "#A47148", "#6F4E37"],
    )

    fig.update_layout(
        height=420,
        margin=dict(t=30, l=10, r=10, b=10),
        paper_bgcolor=bg_card,
        plot_bgcolor=bg_card,
        font=dict(color=text_color),
        coloraxis_colorbar=dict(
            tickfont=dict(color=text_color),
            title=dict(text="Revenue", font=dict(color=text_color)),
        ),
    )

    fig.update_traces(
        textinfo="label+percent parent",
        hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:,.0f}<extra></extra>",
    )

    st.plotly_chart(fig, use_container_width=True)


with tab2:

    # ================ REVENUE VS ORDER ======================
    show_kpis()
    st.markdown("## 📊 Revenue vs Demand (Cluster View)")

    fig, ax1 = plt.subplots(figsize=(8, 4))  # 👈 increased size
    ax2 = ax1.twinx()
    x = np.arange(len(rev_cat["Category"]))
    width = 0.4  # balanced spacing

    ax1.bar(x - width / 2, rev_cat["Revenue"], width, label="Revenue", color="#6F4E37")

    ax2.bar(x + width / 2, rev_cat["Orders"], width, label="Orders", color="#C58940")

    # ---- STYLE ----
    ax1.set_facecolor(bg_card)
    fig.patch.set_facecolor(bg_card)

    ax1.set_xticks(x)
    ax1.set_xticklabels(rev_cat["Category"], rotation=25, ha="center")

    ax1.set_ylabel("Revenue", color="#F5EFE6")
    ax2.set_ylabel("Orders", color="#F5EFE6")

    ax1.tick_params(colors=text_color)
    ax2.tick_params(colors=text_color)

    for spine in ax1.spines.values():
        spine.set_visible(False)
    for spine in ax2.spines.values():
        spine.set_visible(False)

    ax.grid(axis="y", linestyle="--", alpha=0.3, color=grid_color)

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    legend = ax1.legend(
        handles1 + handles2,
        labels1 + labels2,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.15),  # 👈 moves legend above chart
        ncol=2,  # horizontal layout
        frameon=False,
        fontsize=10,
    )

    for text in legend.get_texts():
        text.set_color("#F5EFE6")  # 👈 readable on brown bg

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)

    # ============== Heatmap ==============

    st.markdown("## 🔥 Demand Heatmap (Category vs Hour)")

    heatmap_data = (
        filtered_df.groupby(["product_category", "Hour"])["Revenue"]
        .sum()
        .unstack()
        .fillna(0)
    )

    # Normalize (important for readability)
    heatmap_norm = heatmap_data.div(
        heatmap_data.max(axis=1).replace(0, np.nan), axis=0
    ).fillna(0)

    top_categories = (
        filtered_df.groupby("product_category")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(6)  # 👈 limit (5–7 best)
        .index
    )

    heatmap_data = heatmap_data.loc[top_categories]
    heatmap_norm = heatmap_norm.loc[top_categories]

    heatmap_norm.index = heatmap_norm.index.str.slice(0, 8)

    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_norm.values,
            x=heatmap_norm.columns,
            y=heatmap_norm.index,
            xgap=0.5,
            ygap=0.5,
            hoverongaps=False,
            colorscale=[
                [0.0, "#FFFFE5"],  # very light yellow
                [0.2, "#FFF7BC"],
                [0.4, "#FEC44F"],
                [0.6, "#FE9929"],
                [0.8, "#EC7014"],
                [1.0, "#CC4C02"],  # deep orange-brown
            ],
            hovertemplate="<b>%{y}</b><br>Hr: %{x}<br>₹ %{z:.2f}<extra></extra>",
            colorbar=dict(
                title="Intensity",
                tickfont=dict(color=text_color),
                title_font=dict(color=text_color),
            ),
        )
    )

    fig.update_layout(
        height=320,
        margin=dict(l=5, r=5, t=30, b=20),
        paper_bgcolor=bg_card,
        plot_bgcolor=bg_card,
        font=dict(color=text_color),
        xaxis=dict(
            title="Hour",
            showgrid=False,
            tickfont=dict(color=text_color, size=9),
        ),
        yaxis=dict(
            title="Category", tickfont=dict(color=text_color, size=9), automargin=True
        ),
    )

    st.plotly_chart(fig, use_container_width=True)
    insight_card(
        "🔥 Demand Behavior",
        """
<ul style="padding-left:18px; margin:0;">
<li>Demand varies across time & category</li>
<li>Some slots show strong spikes</li>
<li>Use targeted promotions</li>
</ul>
    """,
        color="#6F4E37",
    )
    st.markdown("<div style='margin-bottom:25px;'></div>", unsafe_allow_html=True)
# ================= PRODUCT ANALYSIS =================

with tab3:
    show_kpis()
    subtab1, subtab2, subtab3 = st.tabs(
        [
            "🏆 Product Ranking",
            "📊 Revenue Concentration (Pareto)",
            "🎯 Product Performance Matrix",
        ]
    )
    rank_col = "Revenue" if metric == "Revenue" else "Sales"

    with subtab1:
        col1, col2 = st.columns(2)

        value_col = "Revenue" if metric_choice == "Revenue" else "Sales"

        colors = [
            "#2F4858",  # deep blue-grey
            "#33658A",  # steel blue
            "#758E4F",  # muted green
            "#BC6C25",  # warm brown-orange
            "#DDA15E",  # sand
            "#6D597A",  # muted purple
            "#B56576",  # soft rose
            "#355070",  # navy
            "#588157",  # olive green
            "#E56B6F",  # soft red accent
        ][:top_n]
        top_products = product_summary.sort_values(by=rank_col, ascending=False).head(
            top_n
        )
        bottom_products = product_summary.sort_values(by=rank_col, ascending=True).head(
            top_n
        )

        top_products = top_products.sort_values(by=value_col, ascending=False)
        bottom_products = bottom_products.sort_values(by=value_col, ascending=False)

        # Top
        fig1, ax1 = plt.subplots(figsize=(6.5, 4))
        ax1.barh(top_products["product_detail"], top_products[value_col], color=colors)
        ax1.invert_yaxis()
        for bar in ax1.patches:
            bar.set_edgecolor("#2E2E2E")
            bar.set_linewidth(0.3)

        ax1.margins(y=0.02)
        title_metric = "Revenue" if metric_choice == "Revenue" else "Quantity"

        ax1.set_facecolor(bg_card)
        fig1.patch.set_facecolor(bg_card)
        ax1.tick_params(colors=text_color)
        ax1.grid(axis="x", linestyle="--", color=grid_color, alpha=0.3)
        ax1.set_title(f"Top {top_n} Products by {title_metric}", color=text_color)
        ax1.set_xlabel(value_col)
        ax1.xaxis.label.set_color(text_color)
        ax1.tick_params(colors=text_color)
        ax1.yaxis.label.set_color(text_color)
        ax1.set_axisbelow(True)

        for spine in ax1.spines.values():
            spine.set_visible(False)

        # Bottom
        fig2, ax2 = plt.subplots(figsize=(6.5, 4))
        ax2.barh(
            bottom_products["product_detail"],
            bottom_products[value_col],
            color=sns.color_palette(
                ["#264653", "#2A9D8F", "#8AB17D", "#E9C46A", "#F4A261", "#E76F51"][
                    :top_n
                ]
            ),
        )
        ax2.invert_yaxis()

        for spine in ax2.spines.values():
            spine.set_visible(False)

        for bar in ax2.patches:
            bar.set_edgecolor("#2E2E2E")
            bar.set_linewidth(0.3)

        ax2.set_facecolor(bg_plot)
        ax2.patch.set_alpha(0.95)
        ax2.margins(x=0.02)
        fig2.patch.set_facecolor(bg_card)
        ax2.set_facecolor(bg_card)

        ax2.grid(axis="x", linestyle="--", color=grid_color, alpha=0.3)
        ax2.set_axisbelow(True)

        ax2.set_title(f"Bottom {top_n} Products by {value_col}", color=text_color)
        ax2.set_xlabel(metric_choice)
        ax2.xaxis.label.set_color(text_color)
        ax2.tick_params(colors=text_color)
        ax2.yaxis.label.set_color(text_color)

        with col1:
            st.markdown("#### 🔝 Top Products")
            st.pyplot(fig1, use_container_width=True)

        with col2:
            st.markdown("#### 🔻 Bottom Products")
            st.pyplot(fig2, use_container_width=True)

        # Top Chart
        c1, c2 = st.columns(2)

        with c1:
            insight_card(
                "🏆 Top Performer",
                f"""
<ul style="padding-left:18px; margin:0;">
<li><b>{top_product}</b></li>
<li>Drives maximum {metric_choice.lower()}</li>
<li>Ensure high availability</li>
</ul>
        """,
                color="#C58940",
            )

        with c2:
            insight_card(
                "⚠ Low Performer",
                f"""
<ul style="padding-left:18px; margin:0;">
<li><b>{worst_product}</b></li>
<li>Low contribution</li>
<li>Improve or consider removal</li>
</ul>
        """,
                color="#9C2F2F",
            )
        st.markdown("<div style='margin-bottom:25px;'></div>", unsafe_allow_html=True)

    with subtab2:
        # --------------------- Pareto -------------------------------------

        st.markdown("### 📊 Advanced Pareto Analysis")

        pareto = product_summary.sort_values(by="Revenue", ascending=False).reset_index(
            drop=True
        )
        pareto["Cumulative %"] = pareto["Revenue"].cumsum() / pareto["Revenue"].sum()

        # LIMIT to top 15
        pareto_top = pareto.head(15)

        # -------- COLOR SCALE (AUTO GENERATE PERFECT GRADIENT) --------

        color_scale = pc.sample_colorscale(
            "Blues",  # clean, professional (NOT coffee, as you wanted)
            [1 - i / (len(pareto_top) - 1) for i in range(len(pareto_top))],
        )

        # -------- FIGURE --------
        fig = go.Figure()

        # Bars
        fig.add_bar(
            x=list(range(len(pareto_top))),
            y=pareto_top["Revenue"],
            name="Revenue",
            marker=dict(color=color_scale),
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
        )

        # Line
        fig.add_scatter(
            x=list(range(len(pareto_top))),
            y=pareto_top["Cumulative %"],
            name="Cumulative %",
            yaxis="y2",
            mode="lines+markers",
            line=dict(color="#2E2E2E", width=2),
            marker=dict(size=6),
            hovertemplate="Cumulative: %{y:.2%}<extra></extra>",
        )

        # Layout
        fig.update_layout(
            height=420,
            margin=dict(l=40, r=40, t=30, b=80),
            paper_bgcolor=bg_card,
            plot_bgcolor=bg_card,
            font=dict(color=text_color),
            bargap=0.25,
            xaxis=dict(
                title="Products",
                tickangle=30,
                showgrid=False,
                automargin=True,
                tickmode="array",
                tickvals=list(range(len(pareto_top))),
                ticktext=pareto_top["product_detail"],
                tickfont=dict(color=text_color, size=10),
                title_font=dict(color=text_color),
            ),
            yaxis=dict(
                title="Revenue",
                showgrid=True,
                gridcolor=grid_color,
                tickfont=dict(color=text_color),
                title_font=dict(color=text_color),
            ),
            yaxis2=dict(
                title="Cumulative %",
                overlaying="y",
                side="right",
                tickformat=".0%",
                showgrid=False,
                tickfont=dict(color=text_color),
                title_font=dict(color=text_color),
            ),
            legend=dict(
                bgcolor="rgba(0,0,0,0)",  # remove box
                font=dict(color=text_color),
                orientation="h",
                y=1.05,
                x=0.5,
                xanchor="center",
            ),
        )

        # 80% line (FIXED STYLE)
        fig.add_hline(y=0.8, line_dash="dot", line_color="#9C2F2F", opacity=0.6)

        st.plotly_chart(fig, use_container_width=True)

        # ============= INSIGHTS ====================

        total_products = len(pareto)
        top_80_products = (pareto["Cumulative %"] <= 0.8).sum()
        percent_products = (top_80_products / total_products) * 100

        low_contrib = pareto[pareto["Cumulative %"] > 0.8]
        tail_count = len(low_contrib)
        tail_revenue = low_contrib["Revenue"].sum()
        tail_percent = (tail_revenue / pareto["Revenue"].sum()) * 100

        col1, col2 = st.columns(2)

        with col1:
            insight_card(
                "📊 Revenue Concentration",
                f"""
<ul>
<li>Top <b>{top_80_products}</b> products (~{percent_products:.1f}%) generate <b>80% revenue</b></li>
<li>Remaining <b>{total_products - top_80_products}</b> contribute only <b>20%</b></li>
<li>Revenue is concentrated in few products → reducing low-impact items is safe</li>
</ul>
                """,
                color="#C58940",
            )

        with col2:
            insight_card(
                "📉 Long-Tail Impact",
                f"""
<ul>
<li><b>{tail_count}</b> products contribute only <b>{tail_percent:.2f}%</b></li>
<li>High SKU count → low efficiency</li>
<li>Bundle or remove low performers</li>
<li>Focus on top-selling items for growth</li>
</ul>
    """,
                color="#C58940",
            )
        st.markdown("<div style='margin-bottom:25px;'></div>", unsafe_allow_html=True)
        # ====== GAUGE ======

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=concentration,
                title={"text": "Menu Concentration (%)"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#C58940"},
                    "steps": [
                        {"range": [0, 40], "color": "#2A9D8F"},
                        {"range": [40, 70], "color": "#E9C46A"},
                        {"range": [70, 100], "color": "#9C2F2F"},
                    ],
                },
            )
        )

        fig.update_layout(
            height=370, paper_bgcolor=bg_card, font=dict(color=text_color)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            f"""
    <div style="
        background:{bg_card};
        padding:14px;
        border-radius:14px;
        margin-top:-10px;
        font-size:15px;
        line-height:1.6;
        color:{text_color};
    ">
    <b>📌 Interpretation Guide</b><br><br>

    <span style="color:#2A9D8F;">● </span>Low (0–40%) → Balanced Menu (Low Risk)<br>
    <span style="color:#E9C46A;">● </span>Medium (40–70%) → Moderate Dependency<br>
    <span style="color:#9C2F2F;">● </span>High (70–100%) → High Risk (Few products dominate)
    </div>
    """,
            unsafe_allow_html=True,
        )
        st.markdown("<div style='margin-bottom:25px;'></div>", unsafe_allow_html=True)

        if concentration > 70:
            insight_card(
                "⚠ High Risk Menu",
                "Business depends heavily on few products → high risk concentration",
                color="#9C2F2F",
            )
        elif concentration > 40:
            insight_card(
                "⚠ Moderate Concentration",
                "Some dependency on top products → monitor closely",
                color="#E9C46A",
            )
        else:
            insight_card(
                "✅ Balanced Portfolio",
                "Revenue is well distributed across products",
                color="#2A9D8F",
            )
        st.markdown("<div style='margin-bottom:25px;'></div>", unsafe_allow_html=True)

    with subtab3:

        # Scatter
        st.markdown("### 📊 Popularity vs Revenue")

        scatter_df = (
            filtered_df.groupby("product_detail")
            .agg({"transaction_qty": "sum", "Revenue": "sum"})
            .reset_index()
        )

        avg_sales = scatter_df["transaction_qty"].mean()
        avg_revenue = scatter_df["Revenue"].mean()

        def classify(row):
            if row["transaction_qty"] > avg_sales and row["Revenue"] > avg_revenue:
                return "Hero"
            elif row["transaction_qty"] < avg_sales and row["Revenue"] < avg_revenue:
                return "Dead"
            return "Potential"

        scatter_df["Category"] = scatter_df.apply(classify, axis=1)

        fig3, ax3 = plt.subplots(figsize=(6, 4))

        fig = px.scatter(
            scatter_df,
            x="transaction_qty",
            y="Revenue",
            color="Category",
            color_discrete_map={
                "Hero": "#2A9D8F",
                "Potential": "#E9C46A",
                "Dead": "#9C2F2F",
            },
            hover_data={
                "product_detail": True,
                "transaction_qty": True,
                "Revenue": ":,.0f",
            },
        )

        # ---- DOT STYLE (MAIN FIX) ----
        fig.update_traces(
            marker=dict(
                size=14,  # 🔥 bigger dots
                opacity=0.9,
                line=dict(
                    width=1.5,  # 🔥 border thickness
                    color="#2E2E2E",  # dark outline → visible on all colors
                ),
            ),
            hovertemplate="<b>%{customdata[0]}</b><br>"
            + "Sales: %{x}<br>"
            + "Revenue: ₹%{y:,.0f}<extra></extra>",
        )

        # ---- REMOVE WHITE GRID ----
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        # ---- AXIS + THEME ----
        fig.update_layout(
            height=420,
            paper_bgcolor=bg_card,
            plot_bgcolor=bg_card,
            font=dict(color=text_color),
            xaxis=dict(
                title="Sales Volume",
                title_font=dict(size=13, color="#000000"),
                tickfont=dict(color=text_color),
                zeroline=False,
            ),
            yaxis=dict(
                title="Revenue",
                title_font=dict(size=13, color="#000000"),  # coffee brown),
                tickfont=dict(color=text_color),
                zeroline=False,
            ),
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                font=dict(color=text_color),
                orientation="h",
                y=1.05,
                x=0.5,
                xanchor="center",
            ),
        )

        # ---- QUADRANT LINES (cleaner) ----
        fig.add_hline(
            y=avg_revenue,
            line_dash="dash",
            line_color="#6F4E37",
            opacity=0.6,
        )

        fig.add_vline(
            x=avg_sales,
            line_dash="dash",
            line_color="#6F4E37",
            opacity=0.6,
        )

        st.plotly_chart(fig, use_container_width=True)

        hero_count = (scatter_df["Category"] == "Hero").sum()
        dead_count = (scatter_df["Category"] == "Dead").sum()

        insight_card(
            "📊 Product Segmentation Insight",
            f"""
<div>
<b>{hero_count}</b> products are high performers (drive business)<br>
<b>{dead_count}</b> products are underperforming<br>
Focus: Scale heroes, optimize or remove dead products
</div>
""",
            color="#6F4E37",
        )
        st.markdown("<div style='margin-bottom:25px;'></div>", unsafe_allow_html=True)

        # ========== 2nd scatter ===========

        st.markdown("### ⚖ Volume vs Revenue Rank")

        rank_df = product_summary.copy()

        rank_df["Volume Rank"] = rank_df["Sales"].rank(ascending=False)
        rank_df["Revenue Rank"] = rank_df["Revenue"].rank(ascending=False)

        fig = px.scatter(
            rank_df,
            x="Volume Rank",
            y="Revenue Rank",
            color="Revenue",
            color_continuous_scale=[
                [0.0, "#4E79A7"],  # Muted blue
                [0.2, "#A0CBE8"],  # Soft sky blue
                [0.4, "#F28E2B"],  # Warm orange
                [0.6, "#FFBE7D"],  # Light peach
                [0.8, "#59A14F"],  # Balanced green
                [1.0, "#8CD17D"],  # Soft mint green
            ],
            hover_data={
                "product_detail": True,
                "Sales": True,
                "Revenue": ":,.0f",
                "Volume Rank": True,
                "Revenue Rank": True,
            },
        )

        # -------- STYLE --------
        fig.update_layout(
            height=400,
            paper_bgcolor=bg_card,
            plot_bgcolor=bg_card,
            font=dict(color=text_color),
            xaxis=dict(
                title="Volume Rank",
                autorange="reversed",
                showgrid=True,
                zeroline=False,
                gridcolor="rgba(255,255,255,0.15)",  # lighter grid
                griddash="dot",  # dotted lines
                title_font=dict(color=text_color),
                tickfont=dict(color=text_color),
            ),
            yaxis=dict(
                title="Revenue Rank",
                autorange="reversed",
                showgrid=True,
                gridcolor="rgba(255,255,255,0.15)",  # lighter grid
                griddash="dot",
                zeroline=False,
                title_font=dict(color=text_color),
                tickfont=dict(color=text_color),
            ),
            # 🔥 LEGEND TEXT COLOR FIX
            coloraxis_colorbar=dict(
                tickfont=dict(color=text_color),
                title=dict(text="Revenue", font=dict(color=text_color)),
            ),
        )

        # -------- HOVER STYLE --------
        fig.update_traces(
            marker=dict(
                size=12,
                opacity=0.85,
                # color="#C58940",
                line=dict(width=0.5, color="#2E2E2E"),
            ),
            hovertemplate="<b>%{customdata[0]}</b><br>"
            + "Sales: %{customdata[1]}<br>"
            + "Revenue: ₹%{customdata[2]:,.0f}<br>"
            + "Vol Rank: %{x}<br>"
            + "Rev Rank: %{y}<extra></extra>",
        )

        st.plotly_chart(fig, use_container_width=True)

        # -------- Drill-down ---------
        st.markdown(f"### 🔍 Product Drill-down Table(Ranked by {title_metric})")

        drill_df = (
            filtered_df.groupby(["product_detail", "product_type", "product_category"])
            .agg(Sales=("transaction_qty", "sum"), Revenue=("Revenue", "sum"))
            .reset_index()
            .sort_values(by="Revenue", ascending=False)
            .reset_index(drop=True)
        )

        drill_df["Rank"] = (
            drill_df[rank_col].rank(method="first", ascending=False).astype(int)
        )

        drill_df = drill_df.sort_values("Rank").reset_index(drop=True)
        cols = ["Rank"] + [col for col in drill_df.columns if col != "Rank"]
        drill_df = drill_df[cols]

        def highlight_top(val):
            if val <= 3:
                return "background-color: #065F46; color: white; font-weight: bold;"
            elif val <= 5:
                return "background-color: #064E3B; color: #D1FAE5;"
            return ""

        st.dataframe(
            drill_df.style.map(highlight_top, subset=["Rank"])
            .set_table_styles(
                [
                    {
                        "selector": "thead th",
                        "props": [
                            ("background-color", "#4E7A67"),
                            ("color", "white"),
                            ("font-weight", "bold"),
                        ],
                    }
                ]
            )
            .set_properties(
                **{
                    "background-color": bg_card,
                    "color": "#0F1A16",
                    "border-color": "#374151",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )
        st.markdown("## 🧠 Final Recommendations")

        insight_card(
            "🚀 Business Actions",
            """
<div>
• Focus marketing on top-performing products<br>
• Reduce long-tail SKUs to improve efficiency<br>
• Bundle slow-moving products<br>
• Optimize pricing for high-volume low-revenue items
</div>
""",
            color="#2A9D8F",
        )
        st.markdown("<div style='margin-bottom:25px;'></div>", unsafe_allow_html=True)
