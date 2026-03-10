import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="FINSENTSIS | Intelligence Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== ENHANCED CSS STYLING ==============
st.markdown("""
<style>
    /* Import premium fonts */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Clash+Display:wght@400;500;600;700&display=swap');

    /* Global styles with dark theme */
    .stApp {
        background: radial-gradient(circle at 100% 0%, #1a1f2c, #0d1117);
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Header styling */
    .header-text {
        font-family: 'Clash Display', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        background: linear-gradient(135deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .subheader-text {
        font-family: 'Clash Display', sans-serif;
        color: #94a3b8;
        font-size: 1rem;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }

    /* Metric card styling */
    .metric-card {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(129, 140, 248, 0.1));
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }

    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #38bdf8;
        box-shadow: 0 8px 30px rgba(56, 189, 248, 0.3);
    }

    .metric-label {
        color: #94a3b8;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        color: #e2e8f0;
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1.2;
    }

    .metric-trend {
        font-size: 0.9rem;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
        margin-top: 0.5rem;
    }

    .trend-positive {
        background: rgba(34, 197, 94, 0.2);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }

    .trend-negative {
        background: rgba(239, 68, 68, 0.2);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* Chart container */
    .chart-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .chart-title {
        color: #38bdf8;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(56, 189, 248, 0.3);
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }

    .sidebar-header {
        padding: 2rem 1rem;
        text-align: center;
        border-bottom: 1px solid rgba(56, 189, 248, 0.2);
        margin-bottom: 2rem;
    }

    .sidebar-menu-item {
        padding: 0.75rem 1rem;
        margin: 0.25rem 1rem;
        border-radius: 12px;
        color: #94a3b8;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .sidebar-menu-item:hover {
        background: rgba(56, 189, 248, 0.1);
        color: #38bdf8;
        transform: translateX(5px);
    }

    .sidebar-menu-item.active {
        background: linear-gradient(135deg, #38bdf8, #818cf8);
        color: white;
    }

    /* Live indicator */
    .live-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 0.5rem 1rem;
        background: rgba(34, 197, 94, 0.1);
        border-radius: 30px;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        background: #4ade80;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
        100% { opacity: 1; transform: scale(1); }
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #475569;
        font-size: 0.9rem;
        border-top: 1px solid rgba(56, 189, 248, 0.2);
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ============== DATA FUNCTIONS ==============
def get_region_data(region):
    """Return data based on selected region"""
    data_map = {
        "🌍 GLOBAL CONTEXT": {
            'fine_distribution': [40, 30, 15, 15],
            'fine_amounts': [45.2, 28.7, 18.3, 12.8],
            'risk_probability': "14.2%",
            'risk_trend': "-2.1%",
            'compliance_score': "88/100",
            'compliance_trend': "▲ 4",
            'entities': "4,291",
            'entities_trend': "▲ 127",
            'total_fines': "$1.2B",
            'fines_trend': "▲ 5.4%"
        },
        "🇪🇺 EU JURISDICTION": {
            'fine_distribution': [20, 10, 50, 20],
            'fine_amounts': [23.4, 15.6, 42.1, 18.9],
            'risk_probability': "18.7%",
            'risk_trend': "+3.2%",
            'compliance_score': "76/100",
            'compliance_trend': "▼ 5",
            'entities': "2,847",
            'entities_trend': "▲ 89",
            'total_fines': "$892M",
            'fines_trend': "▲ 8.2%"
        },
        "🌏 APAC REGION": {
            'fine_distribution': [50, 20, 10, 20],
            'fine_amounts': [52.8, 18.3, 12.7, 16.2],
            'risk_probability': "22.4%",
            'risk_trend': "+5.7%",
            'compliance_score': "71/100",
            'compliance_trend': "▼ 8",
            'entities': "3,562",
            'entities_trend': "▲ 156",
            'total_fines': "$1.8B",
            'fines_trend': "▲ 12.3%"
        },
        "🌎 AMERICAS": {
            'fine_distribution': [30, 40, 10, 20],
            'fine_amounts': [35.6, 42.3, 11.8, 21.3],
            'risk_probability': "16.5%",
            'risk_trend': "-1.8%",
            'compliance_score': "82/100",
            'compliance_trend': "▲ 2",
            'entities': "3,895",
            'entities_trend': "▲ 102",
            'total_fines': "$1.4B",
            'fines_trend': "▲ 4.7%"
        }
    }
    return data_map.get(region, data_map["🌍 GLOBAL CONTEXT"])

def get_regional_risk_data():
    """Return regional risk data"""
    return pd.DataFrame({
        'Region': ['United States', 'Japan', 'United Kingdom', 'Germany', 'France', 'Singapore'],
        'Risk Score': [2251, 2210, 1182, 839, 756, 623],
        'Entities': [1250, 980, 650, 420, 380, 290]
    })

def get_audit_data():
    """Return audit trail data"""
    return pd.DataFrame({
        'Timestamp': ['2026-03-09 14:02:23', '2026-03-09 12:45:17', '2026-03-09 09:12:45',
                      '2026-03-08 23:30:12', '2026-03-08 18:15:33', '2026-03-08 15:42:08'],
        'Entity': ['Global Corp A', 'Tech Hub Ltd', 'FinServe Inc', 'DataCore Systems', 'MedTech Solutions', 'EuroBank Group'],
        'Violation': ['Tax Evasion', 'ESG Non-Compliance', 'Data Breach', 'Labor Violation', 'Cyber Attack', 'Money Laundering'],
        'Risk Level': ['🔴 CRITICAL', '🟡 HIGH', '🔴 CRITICAL', '🟢 LOW', '🟡 HIGH', '🟠 MEDIUM'],
        'Amount': ['$45.2M', '$12.8M', '$89.3M', '$3.2M', '$67.1M', '$234.5M'],
        'Status': ['Investigation', 'Pending Review', 'Enforcement', 'Resolved', 'Investigation', 'Pending Review']
    })

# ============== SIDEBAR ==============
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div style="font-family: 'Clash Display', sans-serif; font-size: 2rem; font-weight: 700; background: linear-gradient(135deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            FINSENTSIS
        </div>
        <div style="color: #64748b; font-size: 0.9rem; margin-top: 0.5rem;">
            INTELLIGENCE PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main Navigation - Only Dashboard
    st.markdown("### NAVIGATION")
    st.markdown('<div class="sidebar-menu-item active">📊 DASHBOARD</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Domain Selection
    st.markdown("### OPERATIONAL DOMAIN")
    region = st.selectbox(
        "",
        ["🌍 GLOBAL CONTEXT", "🇪🇺 EU JURISDICTION", "🌏 APAC REGION", "🌎 AMERICAS"],
        label_visibility="collapsed",
        key="region_selector"
    )

    # Time Range
    st.markdown("### TIME RANGE")
    time_range = st.selectbox(
        "",
        ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Last Quarter", "Year to Date"],
        label_visibility="collapsed",
        key="time_range"
    )

    st.markdown("---")

    # Live Status
    st.markdown("""
    <div class="live-indicator">
        <div class="pulse-dot"></div>
        <span style="color: #4ade80;">LIVE DATA FEED</span>
    </div>
    <div style="margin-top: 0.5rem; color: #64748b; font-size: 0.85rem;">
        Last sync: 2 seconds ago
    </div>
    """, unsafe_allow_html=True)

# ============== MAIN CONTENT ==============
def main():
    # Get data for selected region
    region_data = get_region_data(region)

    # Header
    st.markdown('<div class="header-text">FINSENTSIS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader-text">Enterprise Compliance & Risk Intelligence Platform</div>', unsafe_allow_html=True)

    # Regional Risk Monitor Header
    st.markdown(f'<h2 style="color: #e2e8f0; margin: 2rem 0 1rem 0;">📊 REGIONAL RISK MONITOR: {region}</h2>', unsafe_allow_html=True)

    # ============== KPI METRICS ==============
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        trend_class = "trend-negative" if "-" in region_data['risk_trend'] else "trend-positive"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">RISK PROBABILITY</div>
            <div class="metric-value">{region_data['risk_probability']}</div>
            <div class="metric-trend {trend_class}">{region_data['risk_trend']} vs yesterday</div>
            <div style="color: #64748b; font-size: 0.85rem; margin-top: 0.5rem;">Confidence: 95%</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        trend_class = "trend-positive" if "▲" in region_data['compliance_trend'] else "trend-negative"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">COMPLIANCE SCORE</div>
            <div class="metric-value">{region_data['compliance_score']}</div>
            <div class="metric-trend {trend_class}">{region_data['compliance_trend']} vs last week</div>
            <div style="color: #64748b; font-size: 0.85rem; margin-top: 0.5rem;">Above threshold: +8%</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ENTITIES MONITORED</div>
            <div class="metric-value">{region_data['entities']}</div>
            <div class="metric-trend trend-positive">{region_data['entities_trend']} new entities</div>
            <div style="color: #64748b; font-size: 0.85rem; margin-top: 0.5rem;">Coverage: 98.3%</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL FINES (EST)</div>
            <div class="metric-value">{region_data['total_fines']}</div>
            <div class="metric-trend trend-positive">{region_data['fines_trend']} vs forecast</div>
            <div style="color: #64748b; font-size: 0.85rem; margin-top: 0.5rem;">YTD: $847M collected</div>
        </div>
        """, unsafe_allow_html=True)

    # ============== MAIN VISUALIZATIONS ==============
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">💰 FINE DISTRIBUTION BY CATEGORY</div>', unsafe_allow_html=True)

        # Create enhanced donut chart with region data
        fig_pie = go.Figure()

        fig_pie.add_trace(go.Pie(
            labels=['Tax Evasion', 'Labor Violations', 'ESG Non-Compliance', 'Cyber Security'],
            values=region_data['fine_distribution'],
            hole=0.7,
            marker=dict(
                colors=['#ef4444', '#f59e0b', '#10b981', '#3b82f6'],
                line=dict(color='#1e293b', width=2)
            ),
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(color='#e2e8f0', size=12),
            hoverinfo='label+value+percent',
            hovertemplate='<b>%{label}</b><br>Value: %{value}%<br>Amount: $%{customdata}B<extra></extra>',
            customdata=[region_data['fine_amounts']]
        ))

        total_fines = sum(region_data['fine_amounts'])
        fig_pie.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=0, b=0, l=0, r=0),
            height=400,
            showlegend=False,
            annotations=[
                dict(
                    text=f"${total_fines:.1f}B",
                    x=0.5, y=0.5,
                    font=dict(size=24, color='#38bdf8', family='Clash Display'),
                    showarrow=False
                )
            ]
        )

        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📊 RISK SENSITIVITY MATRIX</div>', unsafe_allow_html=True)

        # Risk matrix data
        risk_levels = ['Critical (L1)', 'High (L2)', 'Medium (L3)', 'Low (L4)']
        risk_values = [region_data['fine_distribution'][0] * 2.5,
                      region_data['fine_distribution'][1] * 2,
                      region_data['fine_distribution'][2] * 1.5,
                      region_data['fine_distribution'][3]]

        fig_bar = go.Figure()

        fig_bar.add_trace(go.Bar(
            x=risk_levels,
            y=risk_values,
            marker=dict(
                color=risk_values,
                colorscale='RdYlGn_r',
                showscale=False  # Set to False for compatibility
            ),
            text=[f"{v:.0f}" for v in risk_values],
            textposition='outside',
            textfont=dict(color='#e2e8f0')
        ))

        fig_bar.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=20, b=40, l=40, r=40),
            height=400,
            xaxis=dict(
                tickfont=dict(color='#94a3b8'),
                gridcolor='rgba(56, 189, 248, 0.1)'
            ),
            yaxis=dict(
                title="Risk Score",
                titlefont=dict(color='#94a3b8'),
                tickfont=dict(color='#94a3b8'),
                gridcolor='rgba(56, 189, 248, 0.1)'
            )
        )

        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ============== REGIONAL ANALYSIS ==============
    st.markdown("## 🌍 REGIONAL RISK ANALYSIS")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🏢 TOP REGIONS BY RISK EXPOSURE</div>', unsafe_allow_html=True)

        # Regional data
        regions_df = get_regional_risk_data()

        fig_regions = px.bar(
            regions_df,
            x='Region',
            y='Risk Score',
            color='Risk Score',
            color_continuous_scale='RdYlGn_r',
            text='Risk Score',
            hover_data=['Entities']
        )

        fig_regions.update_traces(
            texttemplate='%{text}',
            textposition='outside',
            marker_line_color='rgba(56, 189, 248, 0.3)',
            marker_line_width=1
        )

        fig_regions.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=20, b=40, l=40, r=40),
            height=350,
            xaxis=dict(tickfont=dict(color='#94a3b8'), gridcolor='rgba(56, 189, 248, 0.1)'),
            yaxis=dict(title="Risk Score", titlefont=dict(color='#94a3b8'), tickfont=dict(color='#94a3b8'), gridcolor='rgba(56, 189, 248, 0.1)'),
            coloraxis_showscale=False
        )

        st.plotly_chart(fig_regions, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📈 RISK TREND ANALYSIS (30 DAYS)</div>', unsafe_allow_html=True)

        # Generate trend data with some variation based on region
        np.random.seed(hash(region) % 100)
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')

        # Adjust trends based on region
        region_multiplier = {
            "🌍 GLOBAL CONTEXT": 1.0,
            "🇪🇺 EU JURISDICTION": 0.8,
            "🌏 APAC REGION": 1.3,
            "🌎 AMERICAS": 0.9
        }
        multiplier = region_multiplier.get(region, 1.0)

        trend_data = pd.DataFrame({
            'Date': dates,
            'Critical': np.random.normal(45 * multiplier, 8, 30).cumsum(),
            'High': np.random.normal(78 * multiplier, 12, 30).cumsum(),
            'Medium': np.random.normal(123 * multiplier, 15, 30).cumsum(),
            'Low': np.random.normal(245 * multiplier, 20, 30).cumsum()
        })

        fig_trend = go.Figure()

        fig_trend.add_trace(go.Scatter(
            x=trend_data['Date'],
            y=trend_data['Critical'],
            name='Critical',
            line=dict(color='#ef4444', width=3),
            fill='tonexty',
            fillcolor='rgba(239, 68, 68, 0.1)'
        ))

        fig_trend.add_trace(go.Scatter(
            x=trend_data['Date'],
            y=trend_data['High'],
            name='High',
            line=dict(color='#f59e0b', width=3),
            fill='tonexty',
            fillcolor='rgba(245, 158, 11, 0.1)'
        ))

        fig_trend.add_trace(go.Scatter(
            x=trend_data['Date'],
            y=trend_data['Medium'],
            name='Medium',
            line=dict(color='#facc15', width=3),
            fill='tonexty',
            fillcolor='rgba(250, 204, 21, 0.1)'
        ))

        fig_trend.add_trace(go.Scatter(
            x=trend_data['Date'],
            y=trend_data['Low'],
            name='Low',
            line=dict(color='#4ade80', width=3),
            fill='tonexty',
            fillcolor='rgba(74, 222, 128, 0.1)'
        ))

        fig_trend.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=20, b=40, l=40, r=40),
            height=350,
            xaxis=dict(tickfont=dict(color='#94a3b8'), gridcolor='rgba(56, 189, 248, 0.1)'),
            yaxis=dict(title="Number of Cases", titlefont=dict(color='#94a3b8'), tickfont=dict(color='#94a3b8'), gridcolor='rgba(56, 189, 248, 0.1)'),
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color='#94a3b8')
            )
        )

        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ============== AUDIT TRAIL ==============
    st.markdown("## 🗃️ LIVE AUDIT TRAIL: COMPLIANCE BREACHES")

    # Get audit data
    audit_data = get_audit_data()

    # Create styled table
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    # Create interactive table
    fig_audit = go.Figure(data=[go.Table(
        header=dict(
            values=['<b>TIMESTAMP</b>', '<b>ENTITY</b>', '<b>VIOLATION</b>', '<b>RISK LEVEL</b>', '<b>AMOUNT</b>', '<b>STATUS</b>'],
            fill_color='rgba(56, 189, 248, 0.2)',
            align='left',
            font=dict(color='#38bdf8', size=12, family='Space Grotesk'),
            height=40
        ),
        cells=dict(
            values=[audit_data.Timestamp, audit_data.Entity, audit_data.Violation,
                    audit_data['Risk Level'], audit_data.Amount, audit_data.Status],
            fill_color='rgba(255, 255, 255, 0.02)',
            align='left',
            font=dict(color='#e2e8f0', size=12, family='Space Grotesk'),
            height=35
        )
    )])

    fig_audit.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=300,
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig_audit, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ============== RISK METRICS ==============
    st.markdown("## 📊 ADDITIONAL RISK METRICS")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">AVERAGE RESPONSE TIME</div>
            <div class="metric-value">4.2h</div>
            <div class="metric-trend trend-positive">▼ 12% improvement</div>
            <div style="color: #64748b; font-size: 0.85rem; margin-top: 0.5rem;">Target: < 6h</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">COMPLIANCE COST</div>
            <div class="metric-value">$3.8M</div>
            <div class="metric-trend trend-negative">▲ 8.3% QoQ</div>
            <div style="color: #64748b; font-size: 0.85rem; margin-top: 0.5rem;">Budget: $4.2M</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">AUDIT SUCCESS RATE</div>
            <div class="metric-value">92.5%</div>
            <div class="metric-trend trend-positive">▲ 3.2% vs target</div>
            <div style="color: #64748b; font-size: 0.85rem; margin-top: 0.5rem;">Passed: 185/200</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">RISK COVERAGE</div>
            <div class="metric-value">97.8%</div>
            <div class="metric-trend trend-positive">▲ 1.4% expansion</div>
            <div style="color: #64748b; font-size: 0.85rem; margin-top: 0.5rem;">Entities: 4,291/4,387</div>
        </div>
        """, unsafe_allow_html=True)

    # ============== FOOTER ==============
    st.markdown("""
    <div class="footer">
        <div style="margin-bottom: 1rem;">
            <span style="color: #38bdf8; font-weight: 600;">FINSENTSIS</span> Intelligence Platform
        </div>
        <div style="display: flex; justify-content: center; gap: 2rem;">
            <span style="color: #64748b;">© 2026 FINSENTSIS. All rights reserved.</span>
            <span style="color: #38bdf8;">●</span>
            <span style="color: #64748b;">Data refreshed in real-time</span>
            <span style="color: #38bdf8;">●</span>
            <span style="color: #64748b;">v2.4.0</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Run the main function
if __name__ == "__main__":
    main()
