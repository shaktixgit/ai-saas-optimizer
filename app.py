import streamlit as st
import pandas as pd
import random
import time
import os
import base64
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="OptiCore | Workforce & SaaS Optimization",
    page_icon="🏢",
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

# ==========================================
# THEME CONFIGURATION
# ==========================================
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light"

with st.sidebar:
    st.markdown("<p style='font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;'>Workspace Theme</p>", unsafe_allow_html=True)
    theme_choice = st.radio(
        "Display Mode",
        ["Light Glass", "Dark Glass"],
        index=0 if st.session_state.theme_mode == "Light" else 1,
        horizontal=True,
        label_visibility="collapsed"
    )
    st.session_state.theme_mode = "Light" if "Light" in theme_choice else "Dark"

is_dark = st.session_state.theme_mode == "Dark"

# Theme Glass Variables
if is_dark:
    bg_overlay = "linear-gradient(rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.94))"
    glass_card_bg = "rgba(30, 41, 59, 0.65)"
    glass_sidebar_bg = "rgba(15, 23, 42, 0.75)"
    glass_border = "rgba(255, 255, 255, 0.12)"
    glass_highlight = "rgba(255, 255, 255, 0.08)"
    text_primary = "#F8FAFC"
    text_secondary = "#94A3B8"
    input_bg = "rgba(30, 41, 59, 0.7)"
    input_border = "rgba(255, 255, 255, 0.15)"
    btn_glass = "linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%)"
    btn_color = "#F8FAFC"
    table_head_bg = "rgba(255, 255, 255, 0.08)"
    table_row_alt = "rgba(255, 255, 255, 0.03)"
    table_border = "rgba(255, 255, 255, 0.1)"
    uploader_btn_bg = "rgba(255, 255, 255, 0.1)"
    uploader_btn_border = "rgba(255, 255, 255, 0.2)"
else:
    bg_overlay = "linear-gradient(rgba(240, 244, 248, 0.78), rgba(240, 244, 248, 0.88))"
    glass_card_bg = "rgba(255, 255, 255, 0.75)"
    glass_sidebar_bg = "rgba(255, 255, 255, 0.75)"
    glass_border = "rgba(255, 255, 255, 0.85)"
    glass_highlight = "rgba(255, 255, 255, 0.95)"
    text_primary = "#0F172A"
    text_secondary = "#475569"
    input_bg = "rgba(255, 255, 255, 0.65)"
    input_border = "rgba(0, 0, 0, 0.1)"
    btn_glass = "linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(240, 245, 250, 0.7) 100%)"
    btn_color = "#0F172A"
    table_head_bg = "rgba(0, 0, 0, 0.04)"
    table_row_alt = "rgba(0, 0, 0, 0.015)"
    table_border = "rgba(0, 0, 0, 0.08)"
    uploader_btn_bg = "rgba(15, 23, 42, 0.06)"
    uploader_btn_border = "rgba(15, 23, 42, 0.15)"

bg_css = f"""
    background-image: {bg_overlay}, url("data:image/png;base64,{bg_base64}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
""" if bg_base64 else f"background-color: {'#0F172A' if is_dark else '#F1F5F9'} !important;"

# Liquid Glassmorphic CSS Injection
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    .stApp {{
        {bg_css}
        color: {text_primary};
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    
    header {{visibility: hidden;}}
    
    /* Preserve Streamlit Material Icon ligatures so 'upload' does not render as text */
    span[data-testid="stIconMaterial"], 
    i, 
    [data-testid="stIconMaterial"],
    .material-symbols-rounded {{
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;
        font-style: normal !important;
        font-weight: normal !important;
        text-transform: none !important;
    }}
    
    /* Frosted Glass Sidebar */
    section[data-testid="stSidebar"] {{
        background: {glass_sidebar_bg} !important;
        backdrop-filter: blur(28px) saturate(190%) !important;
        -webkit-backdrop-filter: blur(28px) saturate(190%) !important;
        border-right: 1px solid {glass_border} !important;
    }}
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span:not([data-testid="stIconMaterial"]), 
    section[data-testid="stSidebar"] label {{
        color: {text_secondary};
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {text_primary};
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    
    /* Primary Glass Pill Button */
    .stButton > button {{
        background: {btn_glass} !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        color: {btn_color} !important;
        border: 1px solid {glass_border} !important;
        border-radius: 9999px !important;
        padding: 10px 24px !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        letter-spacing: -0.2px;
        box-shadow: 0 8px 20px -4px rgba(0, 0, 0, 0.06), inset 0 1px 2px {glass_highlight} !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        width: 100%;
        margin-top: 4px;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 25px -4px rgba(0, 0, 0, 0.12), inset 0 1px 3px rgba(255, 255, 255, 0.95) !important;
    }}

    /* Frosted Glass Containers */
    .glass-card {{
        background: {glass_card_bg};
        backdrop-filter: blur(28px) saturate(190%);
        -webkit-backdrop-filter: blur(28px) saturate(190%);
        border: 1px solid {glass_border};
        border-radius: 24px;
        padding: 22px;
        box-shadow: 0 10px 30px -6px rgba(0, 0, 0, 0.05), inset 0 1px 1px {glass_highlight};
        margin-bottom: 18px;
    }}

    /* FILE UPLOADER CLEANUP */
    div[data-testid="stFileUploader"] {{
        background: {input_bg} !important;
        border: 1px dashed {input_border} !important;
        border-radius: 16px !important;
        padding: 10px !important;
    }}
    div[data-testid="stFileUploader"] section {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }}
    div[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"],
    div[data-testid="stFileUploader"] button {{
        background: {uploader_btn_bg} !important;
        color: {text_primary} !important;
        border: 1px solid {uploader_btn_border} !important;
        border-radius: 10px !important;
        padding: 6px 14px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }}
    div[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"]:hover,
    div[data-testid="stFileUploader"] button:hover {{
        background: {btn_glass} !important;
        border-color: {glass_border} !important;
    }}
    
    /* Modern Glass Table Styling */
    .custom-table-wrap {{
        max-height: 400px;
        overflow-y: auto;
        border-radius: 16px;
        border: 1px solid {table_border};
        margin-top: 10px;
    }}
    .custom-table-wrap::-webkit-scrollbar {{
        width: 6px;
    }}
    .custom-table-wrap::-webkit-scrollbar-thumb {{
        background: rgba(150, 150, 150, 0.3);
        border-radius: 999px;
    }}
    table.glass-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
        text-align: left;
        margin: 0;
        padding: 0;
    }}
    table.glass-table th {{
        background: {table_head_bg};
        color: {text_secondary};
        font-weight: 700;
        text-transform: uppercase;
        font-size: 11px;
        letter-spacing: 0.6px;
        padding: 12px 16px;
        border-bottom: 1px solid {table_border};
        position: sticky;
        top: 0;
        backdrop-filter: blur(12px);
    }}
    table.glass-table td {{
        padding: 12px 16px;
        color: {text_primary};
        border-bottom: 1px solid {table_border};
        font-weight: 500;
    }}
    table.glass-table tr:nth-child(even) {{
        background: {table_row_alt};
    }}
    table.glass-table tr:hover {{
        background: rgba(255, 101, 132, 0.08);
    }}

    /* Stat Cards */
    .glass-hero-coral {{
        background: linear-gradient(135deg, rgba(255, 138, 120, 0.88) 0%, rgba(255, 101, 132, 0.88) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 22px;
        padding: 20px;
        color: #FFFFFF;
        box-shadow: 0 10px 28px -8px rgba(255, 101, 132, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.8);
        height: 100%;
    }}

    .glass-hero-teal {{
        background: linear-gradient(135deg, rgba(45, 212, 191, 0.88) 0%, rgba(20, 184, 166, 0.88) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 22px;
        padding: 20px;
        color: #FFFFFF;
        box-shadow: 0 10px 28px -8px rgba(20, 184, 166, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.8);
        height: 100%;
    }}

    .glass-hero-indigo {{
        background: linear-gradient(135deg, rgba(129, 140, 248, 0.88) 0%, rgba(99, 102, 241, 0.88) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 22px;
        padding: 20px;
        color: #FFFFFF;
        box-shadow: 0 10px 28px -8px rgba(99, 102, 241, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.8);
        height: 100%;
    }}
    
    .badge-pill {{
        background: rgba(255, 255, 255, 0.22);
        border-radius: 999px;
        padding: 3px 9px;
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: 0.4px;
    }}

    .action-pill {{
        background: rgba(239, 68, 68, 0.12);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.25);
        padding: 3px 9px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 700;
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
    <div style='margin-bottom: 20px;'>
        <h2 style='margin:0; font-size: 20px; font-weight: 800; letter-spacing: -0.5px; color:{text_primary};'>OptiCore Platform</h2>
        <p style='font-size: 12.5px; color: {text_secondary}; margin-top: 3px; font-weight: 500;'>Workforce & SaaS Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<p style='font-weight: 700; font-size: 11px; margin-bottom: 6px; color: {text_secondary}; text-transform: uppercase; letter-spacing: 0.8px;'>Workforce Data</p>", unsafe_allow_html=True)
    
    if st.button("Generate Logs"):
        with st.spinner("Processing logs..."):
            time.sleep(0.3)
            st.session_state['raw_data'] = generate_sample_data(2500)
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload CSV Dataset", type=["csv"], help="Upload custom usage_logs.csv")
    if uploaded is not None:
        st.session_state['raw_data'] = pd.read_csv(uploaded)
        
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-weight: 700; font-size: 11px; margin-bottom: 6px; color: {text_secondary}; text-transform: uppercase; letter-spacing: 0.8px;'>Optimization Controls</p>", unsafe_allow_html=True)
    
    cut_threshold = st.slider("Cut Threshold (%)", min_value=50, max_value=95, value=80, step=5)
    seat_cost = st.slider("License Cost / Seat ($)", min_value=10, max_value=500, value=100, step=10)
    
    st.divider()
    st.markdown(f"<p style='font-size: 11px; color: {text_secondary}; text-align: center; font-weight: 600;'>Enterprise Engine v3.1</p>", unsafe_allow_html=True)

# ==========================================
# MAIN DASHBOARD
# ==========================================

# Run Data Pipeline
results_df, total_emps, seats_cancelled, total_savings = process_pipeline(st.session_state['raw_data'], seat_cost, cut_threshold)

# Header Row
head_left, head_right = st.columns([3, 1])
with head_left:
    st.markdown(f"""
    <div style='margin-bottom: 20px;'>
        <h1 style='font-size: 28px; font-weight: 800; color: {text_primary}; margin: 0; letter-spacing: -0.6px;'>Workforce Optimization Overview</h1>
        <p style='font-size: 13.5px; color: {text_secondary}; margin-top: 4px;'>Automated license reclamation analysis & departmental velocity</p>
    </div>
    """, unsafe_allow_html=True)
with head_right:
    st.markdown(f"""
    <div style='text-align: right; padding-top: 8px;'>
        <span style='background: {glass_card_bg}; backdrop-filter: blur(16px); border: 1px solid {glass_border}; border-radius: 999px; padding: 7px 16px; font-size: 12px; font-weight: 700; color: {text_primary}; box-shadow: 0 4px 14px rgba(0,0,0,0.04);'>
            System Active
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
        <span style="font-size: 11px; font-weight: 700; color: {text_secondary}; text-transform: uppercase; letter-spacing: 0.6px;">Total Workforce</span>
        <div style="font-size: 34px; font-weight: 800; color: {text_primary}; margin: 8px 0 2px 0;">{total_emps:,}</div>
        <div style="font-size: 12px; color: {text_secondary}; font-weight: 500;">Active accounts monitored</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    pct_cut = round((seats_cancelled / total_emps * 100), 1) if total_emps else 0
    st.markdown(f"""
    <div class="glass-hero-coral">
        <span class="badge-pill">Redundancy Rate</span>
        <div style="font-size: 34px; font-weight: 800; margin: 8px 0 2px 0;">{pct_cut}%</div>
        <div style="font-size: 12px; opacity: 0.92; font-weight: 500;">{seats_cancelled:,} Seats flagged for cut</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="glass-hero-teal">
        <span class="badge-pill">Monthly Recovery</span>
        <div style="font-size: 34px; font-weight: 800; margin: 8px 0 2px 0;">${total_savings:,}</div>
        <div style="font-size: 12px; opacity: 0.92; font-weight: 500;">Direct monthly savings</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    annual_savings = total_savings * 12
    st.markdown(f"""
    <div class="glass-hero-indigo">
        <span class="badge-pill">Annual Projection</span>
        <div style="font-size: 34px; font-weight: 800; margin: 8px 0 2px 0;">${annual_savings:,}</div>
        <div style="font-size: 12px; opacity: 0.92; font-weight: 500;">Run-rate capital saved</div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# ROW 2: GLASS CHARTS & SPLINE ANALYTICS
# ----------------------------------------------------
c_left, c_right = st.columns([1.8, 1.2])

with c_left:
    st.markdown(f"""
    <div class="glass-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <div>
                <h3 style="font-size: 16.5px; font-weight: 700; color: {text_primary}; margin: 0;">Automation Velocity Trend</h3>
                <p style="font-size: 12px; color: {text_secondary}; margin-top: 2px;">Quarterly AI automation capacity vs manual overhead</p>
            </div>
            <span style="font-size: 11px; background: {input_bg}; border: 1px solid {glass_border}; padding: 4px 10px; border-radius: 999px; color: {text_secondary}; font-weight: 700;">H2 Analysis</span>
        </div>
    """, unsafe_allow_html=True)
    
    timeline_months = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=timeline_months, y=[28, 64, 42, 85, 58, 80],
        mode='lines',
        name='AI Automation Capacity',
        line=dict(color='#FF6584', width=3.5, shape='spline')
    ))
    
    fig.add_trace(go.Scatter(
        x=timeline_months, y=[72, 38, 60, 24, 48, 22],
        mode='lines',
        name='Manual Effort Required',
        line=dict(color='#3B82F6', width=3.5, shape='spline')
    ))
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=230,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="center", x=0.5, font=dict(color=text_secondary, size=11)),
        xaxis=dict(showgrid=True, gridcolor="rgba(150, 150, 150, 0.1)", color=text_secondary, showline=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(150, 150, 150, 0.1)", color=text_secondary, showticklabels=False, showline=False, zeroline=False)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

with c_right:
    st.markdown(f"""
    <div class="glass-card">
        <h3 style="font-size: 16.5px; font-weight: 700; color: {text_primary}; margin: 0 0 4px 0;">Departmental Density</h3>
        <p style="font-size: 12px; color: {text_secondary}; margin-bottom: 12px;">Automation potential per business unit</p>
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
        <div style="margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 700; margin-bottom: 3px;">
                <span style="color: {text_primary};">{dept_name}</span>
                <span style="color: {text_secondary};">{rate}% ({cancels} cuts)</span>
            </div>
            <div style="width: 100%; height: 6px; background-color: {input_bg}; border-radius: 999px; overflow: hidden; border: 1px solid {glass_border};">
                <div style="width: {rate}%; height: 100%; background: {bar_color}; border-radius: 999px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# ROW 3: CLEAN NATIVE GLASS TABLE
# ----------------------------------------------------
st.markdown(f"""
<div class="glass-card">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <div>
            <h3 style="font-size: 16.5px; font-weight: 700; color: {text_primary}; margin: 0;">License Reclamation Audit</h3>
            <p style="font-size: 12px; color: {text_secondary}; margin-top: 2px;">Employees with &ge; {cut_threshold}% repetitive automatable workflows</p>
        </div>
        <span style="background: rgba(255, 101, 132, 0.14); color: #FF6584; padding: 5px 14px; border-radius: 999px; font-size: 11.5px; font-weight: 800; border: 1px solid rgba(255,101,132,0.3);">
            {seats_cancelled} Licenses Eligible
        </span>
    </div>
""", unsafe_allow_html=True)

cancel_table = results_df[results_df['Flag_Cancel'] == True].sort_values(by='Total_Tasks', ascending=False)

rows_list = []
for _, r in cancel_table.iterrows():
    rows_list.append(
        f"<tr>"
        f"<td style='font-weight:700;'>{r['User_ID']}</td>"
        f"<td>{r['Department']}</td>"
        f"<td>{r['Total_Tasks']}</td>"
        f"<td>{r['Auto_Tasks']}</td>"
        f"<td style='color:#FF6584; font-weight:700;'>{r['Automation_Rate']:.1f}%</td>"
        f"<td><span class='action-pill'>Revoke License</span></td>"
        f"</tr>"
    )

table_body = "".join(rows_list)

table_html = (
    f"<div class='custom-table-wrap'>"
    f"<table class='glass-table'>"
    f"<thead><tr>"
    f"<th>Employee ID</th>"
    f"<th>Department</th>"
    f"<th>Logged Tasks</th>"
    f"<th>Automatable Tasks</th>"
    f"<th>Automation Score</th>"
    f"<th>Recommended Action</th>"
    f"</tr></thead>"
    f"<tbody>{table_body}</tbody>"
    f"</table>"
    f"</div>"
)

st.markdown(table_html, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
