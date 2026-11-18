"""
HADHED | Financial Analysis Studio
Single-app financial analytics built with Streamlit.
All sample financial statements and terminal signals are illustrative.
"""
from __future__ import annotations

import time
import random
from datetime import datetime
from typing import Dict

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# =============================================================================
# 1) CONFIGURATION & PRESENTATION
# =============================================================================
st.set_page_config(
    page_title="HADHED | Financial Analysis Studio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#10243A"
TEAL = "#18A999"
GOLD = "#F4B942"
RED = "#E05D5D"
MUTED = "#718096"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@300;400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'IBM Plex Sans Thai','Inter',sans-serif; }
.stApp { background: #F5F7FA; }
[data-testid="stSidebar"] { background: #10243A; }
[data-testid="stSidebar"] * { color: #F3F6FA !important; }
[data-testid="stMetric"] { background: white; border: 1px solid #E6EBF1;
  padding: 16px 18px; border-radius: 12px; }
[data-testid="stMetricLabel"] { color: #718096; }
[data-testid="stMetricValue"] { color: #10243A; }
.block-container { padding-top: 1.8rem; padding-bottom: 2rem; }
div[data-testid="stTabs"] button { font-weight: 600; }
.small-note { color: #718096; font-size: 0.84rem; }
.section-kicker { color: #18A999; font-size: .78rem; font-weight: 700; letter-spacing: .08em; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# 2) FINANCIAL ENGINE — SAMPLE DATA & RATIO CALCULATIONS
# =============================================================================
@st.cache_data
def build_sample_statements() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create five years of internally consistent illustrative statements (THB mm)."""
    years = np.arange(2021, 2026)
    revenue = np.array([820, 900, 990, 1100, 1220], dtype=float)
    cogs = revenue * np.array([.62, .615, .61, .60, .595])
    sga = revenue * np.array([.20, .198, .195, .19, .188])
    depreciation = np.array([28, 30, 33, 36, 40], dtype=float)
    interest = np.array([22, 23, 24, 25, 24], dtype=float)
    tax_rate = .20
    ebit = revenue - cogs - sga - depreciation
    ebt = ebit - interest
    net_income = ebt * (1 - tax_rate)

    income = pd.DataFrame({
        "ปี": years, "รายได้": revenue, "ต้นทุนขาย": cogs,
        "กำไรขั้นต้น": revenue - cogs, "ค่าใช้จ่ายดำเนินงาน": sga + depreciation,
        "EBIT": ebit, "ดอกเบี้ยจ่าย": interest, "กำไรก่อนภาษี": ebt,
        "ภาษี": ebt * tax_rate, "กำไรสุทธิ": net_income,
    })

    cash = np.array([95, 105, 118, 132, 150], dtype=float)
    receivables = revenue * np.array([.105, .104, .103, .102, .10])
    inventory = np.array([105, 112, 120, 128, 137], dtype=float)
    current_assets = cash + receivables + inventory + np.array([25, 27, 29, 31, 34])
    ppe = np.array([390, 420, 455, 490, 530], dtype=float)
    total_assets = current_assets + ppe
    current_liabilities = np.array([180, 190, 205, 218, 230], dtype=float)
    long_debt = np.array([260, 255, 250, 240, 225], dtype=float)
    total_liabilities = current_liabilities + long_debt
    equity = total_assets - total_liabilities

    balance = pd.DataFrame({
        "ปี": years, "เงินสด": cash, "ลูกหนี้การค้า": receivables,
        "สินค้าคงเหลือ": inventory, "สินทรัพย์หมุนเวียน": current_assets,
        "ที่ดินอาคารและอุปกรณ์": ppe, "สินทรัพย์รวม": total_assets,
        "หนี้สินหมุนเวียน": current_liabilities, "หนี้สินระยะยาว": long_debt,
        "หนี้สินรวม": total_liabilities, "ส่วนของผู้ถือหุ้น": equity,
    })
    return income, balance


def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    """Avoid division-by-zero and return NaN where denominator is zero."""
    return numerator.div(denominator.replace(0, np.nan))


def calculate_ratios(income: pd.DataFrame, balance: pd.DataFrame) -> pd.DataFrame:
    """Calculate liquidity, profitability, leverage and coverage ratios."""
    df = income.merge(balance, on="ปี", validate="one_to_one")
    quick_assets = df["เงินสด"] + df["ลูกหนี้การค้า"]
    avg_assets = (df["สินทรัพย์รวม"] + df["สินทรัพย์รวม"].shift(1)) / 2
    avg_equity = (df["ส่วนของผู้ถือหุ้น"] + df["ส่วนของผู้ถือหุ้น"].shift(1)) / 2
    # First year uses ending balances because opening balances are unavailable.
    avg_assets.iloc[0] = df["สินทรัพย์รวม"].iloc[0]
    avg_equity.iloc[0] = df["ส่วนของผู้ถือหุ้น"].iloc[0]

    ratios = pd.DataFrame({"ปี": df["ปี"]})
    ratios["Current Ratio"] = safe_divide(df["สินทรัพย์หมุนเวียน"], df["หนี้สินหมุนเวียน"])
    ratios["Quick Ratio"] = safe_divide(quick_assets, df["หนี้สินหมุนเวียน"])
    ratios["Gross Profit Margin"] = safe_divide(df["กำไรขั้นต้น"], df["รายได้"])
    ratios["Operating Profit Margin"] = safe_divide(df["EBIT"], df["รายได้"])
    ratios["Net Profit Margin"] = safe_divide(df["กำไรสุทธิ"], df["รายได้"])
    ratios["ROA"] = safe_divide(df["กำไรสุทธิ"], avg_assets)
    ratios["ROE"] = safe_divide(df["กำไรสุทธิ"], avg_equity)
    ratios["D/E Ratio"] = safe_divide(df["หนี้สินรวม"], df["ส่วนของผู้ถือหุ้น"])
    ratios["Interest Coverage"] = safe_divide(df["EBIT"], df["ดอกเบี้ยจ่าย"])

    # DuPont: ROE = Net Profit Margin × Asset Turnover × Equity Multiplier
    ratios["Asset Turnover"] = safe_divide(df["รายได้"], avg_assets)
    ratios["Equity Multiplier"] = safe_divide(avg_assets, avg_equity)
    ratios["DuPont ROE"] = (
        ratios["Net Profit Margin"] * ratios["Asset Turnover"] * ratios["Equity Multiplier"]
    )
    return ratios


def format_value(value: float, suffix: str = "", decimals: int = 2) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value:,.{decimals}f}{suffix}"


income_df, balance_df = build_sample_statements()
ratios_df = calculate_ratios(income_df, balance_df)
years = ratios_df["ปี"].astype(int).tolist()


# =============================================================================
# 3) SIDEBAR — GLOBAL FILTERS
# =============================================================================
with st.sidebar:
    st.markdown("## HADHED")
    st.caption("FINANCIAL ANALYSIS STUDIO")
    st.divider()
    st.markdown("### ตัวกรองข้อมูล")
    view_mode = st.radio("รูปแบบการแสดงผล", ["ภาพรวม 5 ปี", "วิเคราะห์รายปี"], index=0)
    selected_year = st.selectbox("เลือกปีงบการเงิน", years, index=len(years)-1)
    st.divider()
    st.markdown("### การตั้งค่าเทอร์มินัล")
    refresh_seconds = st.slider("ช่วงเวลาอัปเดต (วินาที)", 2, 3, 2)
    alert_drop = st.slider("เกณฑ์แจ้งเตือนราคาลดลง (%)", 1.0, 8.0, 3.0, 0.5)
    st.divider()
    st.caption("ข้อมูลจำลองเพื่อการศึกษา ไม่ใช่ข้อมูลบริษัทจดทะเบียนจริง")


# =============================================================================
# 4) HEADER & KPI HELPERS
# =============================================================================
st.markdown('<div class="section-kicker">CORPORATE FINANCE • ANALYTICS</div>', unsafe_allow_html=True)
st.title("Financial Analysis Dashboard")
st.markdown("วิเคราะห์ผลการดำเนินงาน สภาพคล่อง ความสามารถในการทำกำไร และโครงสร้างเงินทุน")
latest = ratios_df.loc[ratios_df["ปี"] == selected_year].iloc[0]
prior = ratios_df.loc[ratios_df["ปี"] == selected_year - 1]
has_prior = not prior.empty


def delta_text(metric: str) -> str | None:
    if not has_prior:
        return None
    old = float(prior.iloc[0][metric])
    new = float(latest[metric])
    return f"{(new-old)*100:+.2f} จุดเปอร์เซ็นต์" if metric.endswith("Margin") or metric in ("ROA", "ROE") else f"{new-old:+.2f}"


# =============================================================================
# 5) DASHBOARD TABS — OVERVIEW / RATIOS / DUPONT / TERMINAL
# =============================================================================
tab_overview, tab_ratios, tab_dupont, tab_terminal = st.tabs([
    "ภาพรวมกิจการ", "อัตราส่วนทางการเงิน", "DuPont Analysis", "เทอร์มินัลสัญญาณ"
])

with tab_overview:
    st.subheader(f"ผลการดำเนินงานปี {selected_year}")
    revenue_value = float(income_df.loc[income_df["ปี"] == selected_year, "รายได้"].iloc[0])
    net_income_value = float(income_df.loc[income_df["ปี"] == selected_year, "กำไรสุทธิ"].iloc[0])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("รายได้รวม", f"฿{revenue_value:,.1f} ลบ.")
    c2.metric("กำไรสุทธิ", f"฿{net_income_value:,.1f} ลบ.")
    c3.metric("ROE", format_value(latest["ROE"]*100, "%"), delta=delta_text("ROE"))
    c4.metric("Current Ratio", format_value(latest["Current Ratio"], " เท่า"), delta=delta_text("Current Ratio"))

    st.markdown("#### แนวโน้มรายได้และกำไรสุทธิ")
    trend = income_df.melt(id_vars="ปี", value_vars=["รายได้", "กำไรสุทธิ"],
                           var_name="รายการ", value_name="มูลค่า (ล้านบาท)")
    fig = px.line(trend, x="ปี", y="มูลค่า (ล้านบาท)", color="รายการ", markers=True,
                  color_discrete_sequence=[TEAL, GOLD])
    fig.update_layout(template="plotly_white", height=360, margin=dict(l=10,r=10,t=25,b=10),
                      legend_title_text="", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.markdown("#### สถานะทางการเงิน")
        bs = balance_df[["ปี", "สินทรัพย์รวม", "หนี้สินรวม", "ส่วนของผู้ถือหุ้น"]].melt(
            id_vars="ปี", var_name="รายการ", value_name="มูลค่า (ล้านบาท)")
        fig_bs = px.bar(bs, x="ปี", y="มูลค่า (ล้านบาท)", color="รายการ", barmode="group",
                        color_discrete_sequence=[NAVY, RED, TEAL])
        fig_bs.update_layout(template="plotly_white", height=330, legend_title_text="")
        st.plotly_chart(fig_bs, use_container_width=True)
    with right:
        st.markdown("#### งบกำไรขาดทุน")
        display_income = income_df[income_df["ปี"] == selected_year].drop(columns="ปี").T
        display_income.columns = ["ล้านบาท"]
        st.dataframe(display_income.style.format("{:,.2f}"), use_container_width=True, height=330)

    if view_mode == "วิเคราะห์รายปี":
        st.markdown("#### งบแสดงฐานะการเงิน")
        display_bs = balance_df[balance_df["ปี"] == selected_year].drop(columns="ปี").T
        display_bs.columns = ["ล้านบาท"]
        st.dataframe(display_bs.style.format("{:,.2f}"), use_container_width=True)

with tab_ratios:
    st.subheader("Financial Ratio Analysis")
    ratio_labels = {
        "Current Ratio": "Current Ratio", "Quick Ratio": "Quick Ratio",
        "Gross Profit Margin": "Gross Profit Margin", "Operating Profit Margin": "Operating Profit Margin",
        "Net Profit Margin": "Net Profit Margin", "ROA": "ROA", "ROE": "ROE",
        "D/E Ratio": "D/E Ratio", "Interest Coverage": "Interest Coverage",
    }
    selected_ratios = st.multiselect("เลือกอัตราส่วนที่ต้องการเปรียบเทียบ",
        list(ratio_labels.keys()), default=["Current Ratio", "Quick Ratio", "ROE", "D/E Ratio"])
    if selected_ratios:
        ratio_long = ratios_df.melt(id_vars="ปี", value_vars=selected_ratios,
                                    var_name="อัตราส่วน", value_name="ค่า")
        fig_ratio = px.line(ratio_long, x="ปี", y="ค่า", color="อัตราส่วน", markers=True)
        fig_ratio.update_layout(template="plotly_white", height=430, hovermode="x unified")
        st.plotly_chart(fig_ratio, use_container_width=True)
    else:
        st.info("เลือกอัตราส่วนอย่างน้อยหนึ่งรายการเพื่อแสดงกราฟ")

    st.markdown("#### ตารางอัตราส่วนทางการเงิน 5 ปี")
    ratio_table = ratios_df.set_index("ปี").copy()
    percent_cols = ["Gross Profit Margin", "Operating Profit Margin", "Net Profit Margin", "ROA", "ROE", "DuPont ROE"]
    ratio_table[percent_cols] = ratio_table[percent_cols] * 100
    st.dataframe(ratio_table.style.format("{:,.2f}"), use_container_width=True)
    st.caption("อัตรากำไร ROA และ ROE แสดงเป็นเปอร์เซ็นต์ ส่วนอัตราส่วนอื่นแสดงเป็นเท่า")

with tab_dupont:
    st.subheader("DuPont Analysis")
    st.markdown("แยกองค์ประกอบ ROE เพื่อระบุแหล่งที่มาของผลตอบแทนต่อส่วนของผู้ถือหุ้น")
    d = ratios_df.loc[ratios_df["ปี"] == selected_year].iloc[0]
    a, b, c, dcol = st.columns(4)
    a.metric("Net Profit Margin", f"{d['Net Profit Margin']*100:.2f}%")
    b.metric("Asset Turnover", f"{d['Asset Turnover']:.2f} เท่า")
    c.metric("Equity Multiplier", f"{d['Equity Multiplier']:.2f} เท่า")
    dcol.metric("DuPont ROE", f"{d['DuPont ROE']*100:.2f}%")

    # A transparent decomposition chart: profitability, efficiency and leverage.
    components = pd.DataFrame({
        "องค์ประกอบ": ["Net Profit Margin", "Asset Turnover", "Equity Multiplier"],
        "ค่า": [d["Net Profit Margin"]*100, d["Asset Turnover"], d["Equity Multiplier"]]
    })
    fig_d = go.Figure(go.Bar(x=components["องค์ประกอบ"], y=components["ค่า"],
                             marker_color=[TEAL, GOLD, NAVY], text=components["ค่า"].round(3),
                             textposition="outside"))
    fig_d.update_layout(template="plotly_white", height=340, title="องค์ประกอบของ DuPont (หน่วยตามตัวชี้วัด)")
    st.plotly_chart(fig_d, use_container_width=True)

    st.markdown("#### แนวโน้มองค์ประกอบ DuPont 5 ปี")
    dupont_long = ratios_df.melt(id_vars="ปี",
        value_vars=["Net Profit Margin", "Asset Turnover", "Equity Multiplier"],
        var_name="องค์ประกอบ", value_name="ค่า")
    fig_trio = px.line(dupont_long, x="ปี", y="ค่า", color="องค์ประกอบ", markers=True)
    fig_trio.update_layout(template="plotly_white", height=360, hovermode="x unified")
    st.plotly_chart(fig_trio, use_container_width=True)
    st.info("สูตร DuPont: ROE = Net Profit Margin × Asset Turnover × Equity Multiplier")

with tab_terminal:
    st.subheader("Trading / Signal Terminal")
    st.markdown("จำลองข้อมูลตลาดและสัญญาณเตือนแบบวนอัปเดต โดยไม่ใช้ WebSocket")
    st.caption(f"อัปเดตอัตโนมัติทุก {refresh_seconds} วินาที • สัญญาณจำลองเพื่อสาธิตเท่านั้น")

    # Streamlit reruns this section on a timer; no separate backend is required.
    st_autorefresh(interval=refresh_seconds * 1000, key="signal_terminal_refresh")
    if "market_price" not in st.session_state:
        st.session_state.market_price = 25.00
        st.session_state.signal_history = []

    change_pct = random.uniform(-2.8, 2.0)
    st.session_state.market_price *= (1 + change_pct / 100)
    volume = random.randint(80_000, 480_000)
    now = datetime.now().strftime("%H:%M:%S")
    if change_pct <= -alert_drop:
        signal, severity = "PRICE DROP ALERT", "HIGH"
    elif volume >= 400_000:
        signal, severity = "VOLUME SPIKE", "MEDIUM"
    elif change_pct >= 1.5:
        signal, severity = "POSITIVE MOMENTUM", "INFO"
    else:
        signal, severity = "MARKET NORMAL", "INFO"

    event = {"เวลา": now, "ราคาจำลอง": st.session_state.market_price,
             "เปลี่ยนแปลง (%)": change_pct, "ปริมาณซื้อขาย": volume,
             "สัญญาณ": signal, "ระดับ": severity}
    st.session_state.signal_history.insert(0, event)
    st.session_state.signal_history = st.session_state.signal_history[:20]

    p1, p2, p3 = st.columns(3)
    p1.metric("ราคาจำลอง", f"฿{st.session_state.market_price:,.2f}",
              f"{change_pct:+.2f}%")
    p2.metric("ปริมาณซื้อขาย", f"{volume:,} หุ้น")
    p3.metric("สถานะสัญญาณ", signal, severity)

    if severity == "HIGH":
        st.error(f"🚨 {signal}: ราคาปรับลดลง {change_pct:.2f}%")
    elif severity == "MEDIUM":
        st.warning(f"⚠️ {signal}: ปริมาณซื้อขายสูงผิดปกติ")
    else:
        st.success(f"● {signal}")

    st.markdown("#### ประวัติสัญญาณล่าสุด")
    history = pd.DataFrame(st.session_state.signal_history)
    st.dataframe(history, use_container_width=True, hide_index=True)
    if st.button("ล้างประวัติสัญญาณ"):
        st.session_state.signal_history = []
        st.rerun()


# =============================================================================
# 6) FOOTER & DATA EXPORT
# =============================================================================
st.divider()
export = ratios_df.to_csv(index=False).encode("utf-8-sig")
st.download_button("ดาวน์โหลดอัตราส่วนทางการเงิน (CSV)", export,
                   file_name="financial_ratios_5_years.csv", mime="text/csv")
st.markdown(
    '<p class="small-note">HADHED Financial Analysis Studio • Streamlit Single App • '
    'ข้อมูลจำลองเพื่อการศึกษา ไม่ใช่คำแนะนำในการลงทุน</p>',
    unsafe_allow_html=True,
)
