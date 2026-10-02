import streamlit as st
import pandas as pd
import random
import time
import os
import base64
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AI SaaS Optimization Engine",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper function to get base64 background image
def get_base64_img(img_path):
    if os.path.exists(img_path):
        with open(img_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return None

bg_base64 = get_base64_img("background.png")
bg_css = f"""
    background-image: linear-gradient(rgba(240, 244, 248, 0.72), rgba(240, 244, 248, 0.85)), url("data:image/png;base64,{bg_base64}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
""" if bg_base64 else "background-color: #EBF0F5 !important;"

# ==========================================
# THEME CONFIGURATION
# ==========================================
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light"

with st.sidebar:
    st.markdown("### ⚙️ Interface")
    theme_choice = st.radio(
        "Display Mode",
        ["☀️ Glass Light", "🌙 Glass Dark"],
        index=0 if st.session_state.theme_mode == "Light" else 1,
        horizontal=True
    )
    st.session_state.theme_mode = "Light" if "Light" in theme_choice else "Dark"

is_dark = st.session_state.theme_mode == "Dark"

# Theme Glass Variables
if is_dark:
    if bg_base64:
        bg_css = f"""
            background-image: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.92)), url("data:image/png;base64,{bg_base64}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        """
    glass_card_bg = "rgba(30, 41, 59, 0.55)"
    glass_sidebar_bg = "rgba(15, 23, 42, 0.65)"
    glass_border = "rgba(255, 255, 255, 0.12)"
    glass_highlight = "rgba(255, 255, 255, 0.1)"
    text_primary = "#F8FAFC"
    text_secondary = "#94A3B8"
    input_bg = "rgba(30, 41, 59, 0.5)"
    input_border = "rgba(255, 255, 255, 0.15)"
    btn_glass = "linear-gradient(135deg, rgba(255, 255, 255, 0.18) 0%, rgba(255, 255, 255, 0.05) 100%)"
    btn_color = "#F8FAFC"
else:
    glass_card_bg = "rgba(255, 255, 255, 0.55)"
    glass_sidebar_bg = "rgba(255, 255, 255, 0.65)"
    glass_border = "rgba(255, 255, 255, 0.75)"
    glass_highlight = "rgba(255, 255, 255, 0.9)"
    text_primary = "#0F172A"
    text_secondary = "#475569"
    input_bg = "rgba(255, 255, 255, 0.5)"
    input_border = "rgba(255, 255, 255, 0.8)"
    btn_glass = "linear-gradient(135deg, rgba(255, 255, 255, 0.85) 0%, rgba(240, 245, 250, 0.55) 100%)"
    btn_color = "#0F172A"

# Liquid Glassmorphic CSS Injection
st.markdown(f"""
<style>
    /* Full App Glassmorphism Background */
    .stApp {{
        {bg_css}
        color: {text_primary};
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif;
    }}
    
    header {{visibility: hidden;}}
    
    /* Frosted Glass Sidebar */
    section[data-testid="stSidebar"] {{
        background: {glass_sidebar_bg} !important;
        backdrop-filter: blur(24px) saturate(190%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(190%) !important;
        border-right: 1px solid {glass_border} !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: {text_primary};
    }}
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label {{
        color: {text_secondary} !important;
    }}
    
    /* Glassmorphic Pill Button (Matching "✨ Generate" reference image) */
    .stButton > button {{
        background: {btn_glass} !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        color: {btn_color} !important;
        border: 1px solid {glass_border} !important;
        border-radius: 9999px !important;
        padding: 12px 32px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        letter-spacing: -0.2px;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.08), inset 0 1px 2px {glass_highlight} !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        width: 100%;
        margin-top: 8px;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 16px 36px -6px rgba(0, 0, 0, 0.14), inset 0 1px 3px rgba(255, 255, 255, 0.95) !important;
        border-color: rgba(255, 255, 255, 0.9) !important;
    }}
    .stButton > button:active {{
        transform: translateY(1px) scale(0.99);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08), inset 0 2px 4px rgba(0,0,0,0.1) !important;
    }}

    /* Frosted Glass Cards */
    .glass-card {{
        background: {glass_card_bg};
        backdrop-filter: blur(24px) saturate(190%);
        -webkit-backdrop-filter: blur(24px) saturate(190%);
        border: 1px solid {glass_border};
        border-radius: 28px;
        padding: 24px;
        box-shadow: 0 12px 36px -6px rgba(0, 0, 0, 0.06), inset 0 1px 1px {glass_highlight};
        margin-bottom: 20px;
    }}

    /* Modern Glass Slider Styling */
    div[data-baseweb="slider"] {{
        background: transparent !important;
    }}
    div[data-baseweb="slider"] div {{
        border-radius: 999px !important;
    }}
    div[data-baseweb="slider"] [role="slider"] {{
        background: #0F172A !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2) !important;
        width: 20px !important;
        height: 20px !important;
    }}

    /* Glass Inputs & Uploaders */
    .stTextInput > div > div, 
    .stNumberInput > div > div, 
    .stFileUploader section {{
        background: {input_bg} !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid {input_border} !important;
        border-radius: 20px !important;
        color: {text_primary} !important;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }}
    
    /* Table Glass Styling */
    .stDataFrame {{
        background: {glass_card_bg} !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border-radius: 24px !important;
        border: 1px solid {glass_border} !important;
        overflow: hidden !important;
    }}

    /* Gradient Hero Stat Cards with Glass Edge */
    .glass-hero-coral {{
        background: linear-gradient(135deg, rgba(255, 138, 120, 0.85) 0%, rgba(255, 101, 132, 0.85) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 26px;
        padding: 24px;
        color: #FFFFFF;
        box-shadow: 0 14px 34px -8px rgba(255, 101, 132, 0.38), inset 0 1px 1px rgba(255, 255, 255, 0.8);
        height: 100%;
    }}

    .glass-hero-teal {{
        background: linear-gradient(135deg, rgba(45, 212, 191, 0.85) 0%, rgba(20, 184, 166, 0.85) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 26px;
        padding: 24px;
        color: #FFFFFF;
        box-shadow: 0 14px 34px -8px rgba(20, 184, 166, 0.38), inset 0 1px 1px rgba(255, 255, 255, 0.8);
        height: 100%;
    }}

    .glass-hero-indigo {{
        background: linear-gradient(135deg, rgba(129, 140, 248, 0.85) 0%, rgba(99, 102, 241, 0.85) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 26px;
        padding: 24px;
        color: #FFFFFF;
        box-shadow: 0 14px 34px -8px rgba(99, 102, 241, 0.38), inset 0 1px 1px rgba(255, 255, 255, 0.8);
        height: 100%;
    }}
    
    .metric-badge {{
        background: rgba(255, 255, 255, 0.25);
        border-radius: 12px;
        padding: 4px 10px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
    }}
</style>
""", unsafe_allow_html=True)

# ==========================================
# BUSINESS LOGIC & DATA GENERATOR
# ==========================================
def generate_sample_data(num_rows=2500):
    user_ids = [f"EMP-{str(i).zfill(4)}" for i in range(1, (num_rows // 5) + 2)]
    departments = ['Sales', 'HR', 'IT', 'Customer Support', 'Marketing', 'Finance']
    
    auto_tasks = [
        'Copy-pasting emails into CRM', 
        'Data entry from invoices', 
        'Sorting spreadsheets', 
        'Scheduling calendar invites',
        'Extracting numbers from PDFs',
        'Formatting monthly reports',
        'Sending automated follow-ups'
    ]
    human_tasks = [
        'Negotiating client contract', 
        'Interviewing candidates', 
        'High-level strategy planning', 
        'Designing branding assets', 
        'Resolving employee dispute',
        'Facilitating executive meeting',
        'Auditing strategic compliance'
    ]

    records = []
    for _ in range(num_rows):
        dept = random.choice(departments)
        uid = random.choice(user_ids)
        if dept in ['Customer Support', 'Sales', 'Finance']:
            task = random.choice(auto_tasks + human_tasks[:2])
        else:
            task = random.choice(human_tasks + auto_tasks[:2])
        records.append({'User_ID': uid, 'Department': dept, 'Task_Description': task})
    return pd.DataFrame(records)

def clean_data(df):
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].astype(str).str.strip().str.title()
    return df

def classify_task(task_desc):
    task = str(task_desc).lower()
    auto_kw = ['copy', 'paste', 'data', 'sort', 'format', 'schedule', 'extract', 'compile', 'automated', 'entry']
    human_kw = ['negotiate', 'interview', 'design', 'strategy', 'resolve', 'brainstorm', 'counsel', 'lead', 'audit', 'meeting']
    
    if any(k in task for k in human_kw):
        return "Not Automatable"
    elif any(k in task for k in auto_kw):
        return "Automatable"
    return "Needs Review"

def process_pipeline(df, software_cost=100, cut_threshold=80):
    df_clean = clean_data(df.copy())
    if 'Task_Description' in df_clean.columns:
        df_clean['Automation_Status'] = df_clean['Task_Description'].apply(classify_task)
    else:
        df_clean['Automation_Status'] = 'Automatable'
        
    df_clean['Is_Auto'] = df_clean['Automation_Status'].apply(lambda x: 1 if x == 'Automatable' else 0)
    
    user_grp = df_clean.groupby(['User_ID', 'Department']).agg(
        Total_Tasks=('Automation_Status', 'count'),
        Auto_Tasks=('Is_Auto', 'sum')
    ).reset_index()
    
    user_grp['Automation_Rate'] = (user_grp['Auto_Tasks'] / user_grp['Total_Tasks']) * 100
    user_grp['Flag_Cancel'] = user_grp['Automation_Rate'] >= cut_threshold
    
    tot_emps = len(user_grp)
    seats_to_cancel = int(user_grp['Flag_Cancel'].sum())
    savings = seats_to_cancel * software_cost
    
    return user_grp, tot_emps, seats_to_cancel, savings

# Default dataset in session state
if 'raw_data' not in st.session_state:
    st.session_state['raw_data'] = generate_sample_data(1500)

# ==========================================
# SIDEBAR CONTROLS
# ==========================================
with st.sidebar:
    st.markdown(f"""
    <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 6px;'>
        <span style='font-size: 26px;'>✨</span>
        <h2 style='margin:0; font-size: 22px; font-weight: 800; color:{text_primary};'>Insights Studio</h2>
    </div>
    <p style='font-size: 13px; color: {text_secondary}; margin-bottom: 22px;'>Glassmorphic SaaS License Intelligence</p>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<div style='font-weight: 700; font-size: 13px; margin-bottom: 4px; color: {text_primary}; text-transform: uppercase; letter-spacing: 0.5px;'>Generate & Analyze</div>", unsafe_allow_html=True)
    
    # Styled "✨ Generate" Pill Button
    if st.button("✨ Generate"):
        with st.spinner("Processing workflows..."):
            time.sleep(0.3)
            st.session_state['raw_data'] = generate_sample_data(2500)
    
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload Data (CSV)", type=["csv"])
    if uploaded is not None:
        st.session_state['raw_data'] = pd.read_csv(uploaded)
        
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-weight: 700; font-size: 13px; margin-bottom: 8px; color: {text_primary}; text-transform: uppercase; letter-spacing: 0.5px;'>Parameters</div>", unsafe_allow_html=True)
    
    # Modern Sliders
    cut_threshold = st.slider("Automation Threshold (%)", min_value=50, max_value=95, value=80, step=5, help="Mark licenses for removal if tasks reach this % of automation")
    seat_cost = st.slider("License Cost per Seat ($)", min_value=10, max_value=500, value=100, step=10)
    
    st.divider()
    st.markdown(f"<div style='font-size: 12px; color: {text_secondary}; text-align: center; font-weight: 500;'>Liquid Glass UI • Active</div>", unsafe_allow_html=True)

# ==========================================
# MAIN DASHBOARD
# ==========================================

# Run Data Pipeline
results_df, total_emps, seats_cancelled, total_savings = process_pipeline(st.session_state['raw_data'], seat_cost, cut_threshold)

# Header Row
head_left, head_right = st.columns([3, 1])
with head_left:
    st.markdown(f"""
    <div style='margin-bottom: 24px;'>
        <h1 style='font-size: 32px; font-weight: 800; color: {text_primary}; margin: 0; letter-spacing: -0.5px;'>Visitors Insights & Optimization</h1>
        <p style='font-size: 15px; color: {text_secondary}; margin-top: 4px;'>Dynamic workforce automation audit & license recovery</p>
    </div>
    """, unsafe_allow_html=True)
with head_right:
    st.markdown(f"""
    <div style='text-align: right; padding-top: 10px;'>
        <span style='background: {glass_card_bg}; backdrop-filter: blur(16px); border: 1px solid {glass_border}; border-radius: 999px; padding: 10px 20px; font-size: 13px; font-weight: 700; color: {text_primary}; box-shadow: 0 4px 16px rgba(0,0,0,0.05);'>
            ⚡ Live Engine
        </span>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# ROW 1: TRANSLUCENT FROSTED GLASS HERO METRIC CARDS
# ----------------------------------------------------
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="glass-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size: 12px; font-weight: 700; color: {text_secondary}; text-transform: uppercase;">Total Workforce</span>
            <span style="font-size: 16px;">👥</span>
        </div>
        <div style="font-size: 38px; font-weight: 800; color: {text_primary}; margin: 10px 0 2px 0;">{total_emps:,}</div>
        <div style="font-size: 13px; color: {text_secondary}; font-weight: 500;">Active accounts monitored</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    pct_cut = round((seats_cancelled / total_emps * 100), 1) if total_emps else 0
    st.markdown(f"""
    <div class="glass-hero-coral">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="metric-badge">Traffic Overview</span>
            <span style="font-size: 16px;">🎯</span>
        </div>
        <div style="font-size: 38px; font-weight: 800; margin: 10px 0 2px 0;">{pct_cut}%</div>
        <div style="font-size: 13px; opacity: 0.95; font-weight: 500;">{seats_cancelled:,} Redundant seats flagged</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="glass-hero-teal">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="metric-badge">Conversion Rate</span>
            <span style="font-size: 16px;">💵</span>
        </div>
        <div style="font-size: 38px; font-weight: 800; margin: 10px 0 2px 0;">${total_savings:,}</div>
        <div style="font-size: 13px; opacity: 0.95; font-weight: 500;">Monthly recovered budget</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    annual_savings = total_savings * 12
    st.markdown(f"""
    <div class="glass-hero-indigo">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="metric-badge">Annualized ROI</span>
            <span style="font-size: 16px;">📈</span>
        </div>
        <div style="font-size: 38px; font-weight: 800; margin: 10px 0 2px 0;">${annual_savings:,}</div>
        <div style="font-size: 13px; opacity: 0.95; font-weight: 500;">Run-rate capital saved</div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# ROW 2: GLASS CHARTS & SPLINE ANALYTICS
# ----------------------------------------------------
c_left, c_right = st.columns([1.8, 1.2])

with c_left:
    st.markdown(f"""
    <div class="glass-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div>
                <h3 style="font-size: 18px; font-weight: 800; color: {text_primary}; margin: 0;">User Engagement & Focus Velocity</h3>
                <p style="font-size: 13px; color: {text_secondary}; margin-top: 2px;">Monthly AI automation curve vs manual overhead</p>
            </div>
            <span style="font-size: 12px; background: {input_bg}; border: 1px solid {glass_border}; padding: 6px 14px; border-radius: 999px; color: {text_secondary}; font-weight: 700;">Range: Last 6 mo</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Smooth Spline Curve Chart
    timeline_months = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=timeline_months, y=[28, 64, 42, 85, 58, 80],
        mode='lines+markers',
        name='AI Automation Capacity',
        line=dict(color='#FF6584', width=4, shape='spline'),
        marker=dict(size=7, color='#FF6584')
    ))
    
    fig.add_trace(go.Scatter(
        x=timeline_months, y=[72, 38, 60, 24, 48, 22],
        mode='lines+markers',
        name='Manual Effort Required',
        line=dict(color='#3B82F6', width=4, shape='spline'),
        marker=dict(size=7, color='#3B82F6')
    ))
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(color=text_secondary, size=12)),
        xaxis=dict(showgrid=True, gridcolor="rgba(150, 150, 150, 0.1)", color=text_secondary, showline=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(150, 150, 150, 0.1)", color=text_secondary, showticklabels=False, showline=False, zeroline=False)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

with c_right:
    st.markdown(f"""
    <div class="glass-card">
        <h3 style="font-size: 18px; font-weight: 800; color: {text_primary}; margin: 0 0 4px 0;">Departmental Density</h3>
        <p style="font-size: 13px; color: {text_secondary}; margin-bottom: 16px;">Automation potential per business unit</p>
    """, unsafe_allow_html=True)
    
    dept_breakdown = results_df.groupby('Department').agg(
        Avg_Auto=('Automation_Rate', 'mean'),
        Cancels=('Flag_Cancel', 'sum')
    ).reset_index().sort_values(by='Avg_Auto', ascending=False)
    
    for _, row in dept_breakdown.iterrows():
        dept_name = row['Department']
        rate = int(row['Avg_Auto'])
        cancels = int(row['Cancels'])
        bar_color = "#FF6584" if rate >= 70 else ("#2DD4BF" if rate >= 40 else "#818CF8")
        
        st.markdown(f"""
        <div style="margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 700; margin-bottom: 4px;">
                <span style="color: {text_primary};">{dept_name}</span>
                <span style="color: {text_secondary};">{rate}% ({cancels} cuts)</span>
            </div>
            <div style="width: 100%; height: 8px; background-color: {input_bg}; border-radius: 999px; overflow: hidden; border: 1px solid {glass_border};">
                <div style="width: {rate}%; height: 100%; background: {bar_color}; border-radius: 999px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# ROW 3: ACTIONABLE LICENSE TABLE
# ----------------------------------------------------
st.markdown(f"""
<div class="glass-card">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <div>
            <h3 style="font-size: 18px; font-weight: 800; color: {text_primary}; margin: 0;">Redundant Accounts Flagged for Revocation</h3>
            <p style="font-size: 13px; color: {text_secondary}; margin-top: 2px;">Employees with &ge; {cut_threshold}% repetitive automatable tasks</p>
        </div>
        <span style="background: rgba(255, 101, 132, 0.15); color: #FF6584; padding: 6px 16px; border-radius: 999px; font-size: 13px; font-weight: 800; border: 1px solid rgba(255,101,132,0.3);">
            {seats_cancelled} Licenses Eligible
        </span>
    </div>
""", unsafe_allow_html=True)

cancel_table = results_df[results_df['Flag_Cancel'] == True].copy()
cancel_table['Automation_Rate'] = cancel_table['Automation_Rate'].round(1).astype(str) + "%"
cancel_table = cancel_table.rename(columns={
    'User_ID': 'Employee ID',
    'Department': 'Department',
    'Total_Tasks': 'Logged Tasks',
    'Auto_Tasks': 'Automatable Tasks',
    'Automation_Rate': 'Automation Score'
}).drop(columns=['Flag_Cancel'])

st.dataframe(
    cancel_table.sort_values(by='Logged Tasks', ascending=False),
    use_container_width=True,
    hide_index=True
)
st.markdown("</div>", unsafe_allow_html=True)
