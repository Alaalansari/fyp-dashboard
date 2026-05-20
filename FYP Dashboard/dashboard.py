import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Thermal Feasibility Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CUSTOM CSS STYLE
# =========================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #061526 0%, #0A2342 55%, #102B4E 100%);
    color: white;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 1400px;
}

h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: white;
}

.main-title {
    font-size: 32px;
    font-weight: 800;
    color: white;
    line-height: 1.2;
}

.yellow-text {
    color: #FFD83D;
    font-size: 28px;
    font-weight: 500;
}

.card {
    background: rgba(3, 18, 35, 0.82);
    border: 1px solid rgba(65, 145, 220, 0.35);
    border-radius: 14px;
    padding: 22px;
    box-shadow: 0 0 20px rgba(0,0,0,0.25);
    min-height: 130px;
}

.card-small {
    background: rgba(3, 18, 35, 0.82);
    border: 1px solid rgba(65, 145, 220, 0.35);
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 0 20px rgba(0,0,0,0.25);
}

.orange {
    color: #FF7A1A;
    font-weight: 800;
}

.blue {
    color: #2FA8FF;
    font-weight: 800;
}

.green {
    color: #6ED34B;
    font-weight: 800;
}

.metric-label {
    font-size: 15px;
    font-weight: 700;
    color: #F5F5F5;
}

.metric-value {
    font-size: 38px;
    font-weight: 900;
    margin-top: 12px;
}

.info-strip {
    background: rgba(3, 18, 35, 0.75);
    border: 1px solid rgba(65, 145, 220, 0.35);
    border-radius: 12px;
    padding: 14px 24px;
    margin: 12px 0 22px 0;
}

.section-title {
    color: #FF9B21;
    font-size: 18px;
    font-weight: 900;
    margin-bottom: 12px;
}

.stSlider > div > div > div > div {
    background: #FF7A1A;
}

div[data-testid="stMetric"] {
    background: rgba(3, 18, 35, 0.82);
    border: 1px solid rgba(65, 145, 220, 0.35);
    padding: 18px;
    border-radius: 14px;
}

hr {
    border-color: rgba(255,255,255,0.15);
}

</style>
""", unsafe_allow_html=True)

# =========================
# DATA
# =========================

temperature_data = {
    100: 239.4, 150: 253.1, 200: 267.8, 250: 283.5, 300: 300.4,
    350: 317.3, 400: 335.1, 450: 353.5, 500: 372.3, 550: 391.4,
    600: 410.6, 650: 430.0, 700: 449.4, 750: 468.8, 800: 488.1,
    850: 507.3, 900: 526.4, 950: 545.4, 1000: 564.3, 1050: 583.0,
    1100: 601.8, 1150: 620.4, 1200: 639.2, 1250: 811.1,
    1300: 844.8, 1350: 879.9, 1400: 916.4, 1450: 954.9,
    1500: 995.6, 1550: 1039.0, 1600: 1085.0, 1650: 1135.0,
    1700: 1188.0, 1750: 1246.0, 1800: 1308.0, 1850: 1375.0,
    1900: 1447.0, 1950: 1523.0, 2000: 1604.0, 2050: 1688.0,
    2100: 1774.0, 2150: 1861.0, 2200: 1948.0, 2250: 2033.0,
    2300: 2116.0
}

# =========================
# HEADER
# =========================

col_logo1, col_title, col_logo2 = st.columns([1.2, 3.2, 1.2])

with col_logo1:
    st.markdown("""
    <div style="font-size:24px;font-weight:800;color:#FF1744;">
        ICEM
    </div>
    <div style="font-size:17px;color:#FF1744;">
        International College of<br>Engineering & Management
    </div>
    """, unsafe_allow_html=True)

with col_title:
    st.markdown("""
    <div class="yellow-text">MP3995 - Final Year Project</div>
    <div class="main-title">
    THERMAL FEASIBILITY EVALUATION OF WASTE HEAT TRANSFER FROM FLARING SYSTEMS TO PYROLYSIS REACTORS
    </div>
    """, unsafe_allow_html=True)

with col_logo2:
    st.markdown("""
    <div style="font-size:24px;font-weight:800;color:#1399D6;text-align:right;">
        University of<br>Lancashire
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="info-strip">
<b style="color:#FFD83D;">Name:</b> Alaa Adnan Al-Ansari &nbsp;&nbsp;&nbsp;&nbsp;
<b style="color:#FFD83D;">Student ID:</b> G21267518 - H23000206 &nbsp;&nbsp;&nbsp;&nbsp;
<b style="color:#FFD83D;">Date:</b> May 2026 &nbsp;&nbsp;&nbsp;&nbsp;
<b style="color:#FFD83D;">Supervisor:</b> Asif Zamir
</div>
""", unsafe_allow_html=True)

# =========================
# INPUTS
# =========================

left, right = st.columns([1.1, 3.4])

with left:
    st.markdown('<div class="card-small">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚙ SYSTEM CONTROLS</div>', unsafe_allow_html=True)

    flare_temp = st.slider(
        "Flare Heat Source Temperature (°C)",
        min_value=100,
        max_value=2300,
        value=1150,
        step=50
    )

    required_temp = st.slider(
        "Required Pyrolysis Temperature (°C)",
        min_value=400,
        max_value=650,
        value=520,
        step=10
    )

    include_losses = st.toggle("Include Estimated System Losses", value=True)

    loss_percent = st.slider(
        "Estimated System Losses (%)",
        min_value=0,
        max_value=40,
        value=20,
        step=5
    )

    operating_hours = st.slider(
        "Operating Hours",
        min_value=1,
        max_value=24,
        value=8
    )

    electricity_tariff = st.number_input(
        "Electricity Tariff (OMR/kWh)",
        min_value=0.000,
        value=0.020,
        step=0.001,
        format="%.3f"
    )

    show_electricity = st.checkbox("Show Electricity Saved", value=True)
    show_cost = st.checkbox("Show Cost Saved", value=True)
    show_co2 = st.checkbox("Show CO₂ Avoided", value=True)

    grid_emission_factor = st.number_input(
        "Grid Emission Factor (tCO₂/MWh)",
        min_value=0.000,
        value=0.400,
        step=0.010,
        format="%.3f"
    )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# CALCULATIONS
# =========================

molten_salt_temp = temperature_data[flare_temp]

available_heat_mw = flare_temp * 0.01

if include_losses:
    useful_heat_mw = available_heat_mw * (1 - loss_percent / 100)
    adjusted_temp = molten_salt_temp * (1 - loss_percent / 100)
else:
    useful_heat_mw = available_heat_mw
    adjusted_temp = molten_salt_temp

electricity_saved_mwh = useful_heat_mw * operating_hours
electricity_saved_kwh = electricity_saved_mwh * 1000
cost_saved_omr = electricity_saved_kwh * electricity_tariff
co2_avoided = electricity_saved_mwh * grid_emission_factor

feasible = adjusted_temp >= required_temp
temperature_margin = adjusted_temp - required_temp

# =========================
# OUTPUTS
# =========================

with right:
    r1c1, r1c2, r1c3 = st.columns(3)

    with r1c1:
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">🌡 FLARE HEAT SOURCE TEMPERATURE</div>
            <div class="metric-value orange">{flare_temp} °C</div>
        </div>
        """, unsafe_allow_html=True)

    with r1c2:
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">💧 MOLTEN SALT OUTLET TEMPERATURE</div>
            <div class="metric-value blue">{adjusted_temp:.1f} °C</div>
        </div>
        """, unsafe_allow_html=True)

    with r1c3:
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">🏭 REQUIRED PYROLYSIS TEMPERATURE</div>
            <div class="metric-value orange">{required_temp} °C</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    r2c1, r2c2, r2c3 = st.columns(3)

    with r2c1:
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">🔥 USEFUL HEAT DELIVERED</div>
            <div class="metric-value orange">{useful_heat_mw:.2f} MW</div>
        </div>
        """, unsafe_allow_html=True)

    with r2c2:
        margin_color = "green" if temperature_margin >= 0 else "orange"
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">📈 TEMPERATURE MARGIN</div>
            <div class="metric-value {margin_color}">{temperature_margin:.1f} °C</div>
        </div>
        """, unsafe_allow_html=True)

    with r2c3:
        losses_text = f"{loss_percent} %" if include_losses else "OFF"
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">📊 LOSSES APPLIED</div>
            <div class="metric-value orange">{losses_text}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    status_col, save_col1, save_col2, save_col3 = st.columns([1.8, 1, 1, 1])

    with status_col:
        if feasible:
            st.markdown("""
            <div class="card">
                <div class="green" style="font-size:20px;">✅ SYSTEM IS THERMALLY FEASIBLE</div>
                <p>The molten salt outlet temperature is sufficient to meet the selected pyrolysis requirement.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card">
                <div class="orange" style="font-size:20px;">❌ SYSTEM IS NOT THERMALLY FEASIBLE</div>
                <p>The molten salt outlet temperature is below the selected pyrolysis requirement.</p>
            </div>
            """, unsafe_allow_html=True)

    with save_col1:
        if show_electricity:
            st.markdown(f"""
            <div class="card">
                <div class="metric-label">ELECTRICITY SAVED</div>
                <div class="metric-value blue">{electricity_saved_mwh:.2f}</div>
                <div class="blue">MWh</div>
            </div>
            """, unsafe_allow_html=True)

    with save_col2:
        if show_cost:
            st.markdown(f"""
            <div class="card">
                <div class="metric-label">ESTIMATED COST SAVED</div>
                <div class="metric-value orange">{cost_saved_omr:.2f}</div>
                <div class="orange">OMR</div>
            </div>
            """, unsafe_allow_html=True)

    with save_col3:
        if show_co2:
            st.markdown(f"""
            <div class="card">
                <div class="metric-label">ESTIMATED CO₂ AVOIDED</div>
                <div class="metric-value green">{co2_avoided:.2f}</div>
                <div class="green">tCO₂</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    bottom1, bottom2 = st.columns([1.3, 1])

    with bottom1:
        st.markdown(f"""
        <div class="card-small">
            <div class="section-title">HEAT TRANSFER FLOW</div>
            <div style="font-size:20px;text-align:center;line-height:2;">
                🔥 → ♨️ → 🌡️ → 🏭
            </div>
            <div style="display:flex;justify-content:space-around;text-align:center;">
                <div><b>Flare Heat</b><br><span class="orange">{flare_temp} °C</span></div>
                <div><b>WHTU</b><br><span class="orange">{useful_heat_mw:.2f} MW</span></div>
                <div><b>Molten Salt</b><br><span class="blue">{adjusted_temp:.1f} °C</span></div>
                <div><b>Pyrolysis</b><br><span class="orange">{required_temp} °C</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with bottom2:
        st.markdown('<div class="card-small">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">ASPEN HYSYS SENSITIVITY DATA</div>', unsafe_allow_html=True)

        df = pd.DataFrame({
            "Flare Heat Source Temp (°C)": list(temperature_data.keys()),
            "Molten Salt Outlet Temp (°C)": list(temperature_data.values())
        })

        st.dataframe(df, use_container_width=True, height=260)

        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<br>
<div style="border-top:1px solid rgba(255,255,255,0.2);padding-top:18px;">
    <span style="color:#FF9B21;font-weight:800;font-size:18px;">
    💡 Towards Sustainable Energy Recovery and Industrial Decarbonization
    </span><br>
    <span style="color:white;">Transforming Waste Heat into Value</span>
</div>
""", unsafe_allow_html=True)