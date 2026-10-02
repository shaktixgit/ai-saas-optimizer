import streamlit as st
import pandas as pd
import random
import time
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AI SaaS Optimization Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# THEME CONFIGURATION & DYNAMIC STYLING
# ==========================================
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light"

# Sidebar Theme Selector
with st.sidebar:
    st.markdown("### ⚙️ Preferences")
    theme = st.radio(
        "Interface Mode",
        ["☀️ Light", "🌙 Dark"],
        index=0 if st.session_state.theme_mode == "Light" else 1,
        horizontal=True
    )
    st.session_state.theme_mode = "Light" if "Light" in theme else "Dark"

is_dark = st.session_state.theme_mode == "Dark"

# Theme Palette Variables
if is_dark:
    bg_color = "#0F1115"
    sidebar_bg = "#16181D"
    card_bg = "#1C1F26"
    card_border = "rgba(255, 255, 255, 0.08)"
    text_primary = "#F1F5F9"
    text_secondary = "#94A3B8"
    input_bg = "#232730"
    input_border = "#333846"
    chart_grid = "rgba(255, 255, 255, 0.05)"
    chart_bg = "rgba(0,0,0,0)"
    btn_bg = "#22252C"
    btn_border = "#323742"
    btn_text = "#E2E8F0"
    btn_shadow = "inset 1px 1px 3px rgba(255,255,255,0.1), inset -2px -2px 5px rgba(0,0,0,0.7), 0 4px 12px rgba(0,0,0,0.5)"
else:
    bg_color = "#F4F6F9"
    sidebar_bg = "#FFFFFF"
    card_bg = "#FFFFFF"
    card_border = "rgba(0, 0, 0, 0.06)"
    text_primary = "#0F172A"
    text_secondary = "#64748B"
    input_bg = "#F8FAFC"
    input_border = "#E2E8F0"
    chart_grid = "rgba(0, 0, 0, 0.05)"
    chart_bg = "rgba(0,0,0,0)"
    btn_bg = "#1E2229"
    btn_border = "#2E3440"
    btn_text = "#D8DEE9"
    btn_shadow = "inset 2px 2px 4px rgba(255,255,255,0.12), inset -2px -2px 6px rgba(0,0,0,0.6), 0 6px 16px rgba(0,0,0,0.15)"

# Custom CSS Injection
st.markdown(f"""
<style>
    /* Global Styles */
    .stApp {{
        background-color: {bg_color};
        color: {text_primary};
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }}
    
    header {{visibility: hidden;}}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {card_border} !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: {text_primary};
    }}
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label {{
        color: {text_secondary} !important;
    }}
    
    /* Neumorphic Dark Pill Button (as in reference image) */
    .stButton > button {{
        background: {btn_bg} !important;
        color: {btn_text} !important;
        border: 1px solid {btn_border} !important;
        border-radius: 9999px !important;
        padding: 10px 28px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        box-shadow: {btn_shadow} !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        margin-top: 6px;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px);
        color: #FFFFFF !important;
        box-shadow: inset 2px 2px 5px rgba(255,255,255,0.2), inset -2px -2px 6px rgba(0,0,0,0.8), 0 8px 20px rgba(0,0,0,0.25) !important;
    }}
    .stButton > button:active {{
        transform: translateY(1px);
        box-shadow: inset 3px 3px 6px rgba(0,0,0,0.8), inset -1px -1px 3px rgba(255,255,255,0.1) !important;
    }}
    
    /* Inputs & File Uploader */
    .stTextInput > div > div, 
    .stNumberInput > div > div, 
    .stFileUploader > div > div {{
        background-color: {input_bg} !important;
        border: 1px solid {input_border} !important;
        border-radius: 14px !important;
        color: {text_primary} !important;
    }}
    
    .stFileUploader section {{
        background-color: {input_bg} !important;
        border: 1px dashed {input_border} !important;
        border-radius: 16px !important;
        padding: 12px !important;
    }}
    
    /* Streamlit Metric Container Override */
    div[data-testid="metric-container"] {{
        background-color: {card_bg};
        border: 1px solid {card_border};
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 20px -4px rgba(0, 0, 0, { "0.2" if is_dark else "0.04" });
    }}
    
    /* Dataframe Table Rounded */
    .stDataFrame {{
        border-radius: 18px !important;
        overflow: hidden !important;
        border: 1px solid {card_border} !important;
        background-color: {card_bg} !important;
    }}
    
    /* Card UI helpers */
    .custom-card {{
        background-color: {card_bg};
        border: 1px solid {card_border};
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 4px 24px -4px rgba(0, 0, 0, { "0.3" if is_dark else "0.05" });
        height: 100%;
    }}
    
    .gradient-card-coral {{
        background: linear-gradient(135deg, #FFB8A9 0%, #FF8F77 50%, #FF6584 100%);
        border-radius: 24px;
        padding: 24px;
        color: #1A1A1A;
        box-shadow: 0 8px 24px -4px rgba(255, 101, 132, 0.35);
        height: 100%;
        position: relative;
        overflow: hidden;
    }}
    
    .gradient-card-teal {{
        background: linear-gradient(135deg, #99F6E4 0%, #5EEAD4 50%, #2DD4BF 100%);
        border-radius: 24px;
        padding: 24px;
        color: #042F2E;
        box-shadow: 0 8px 24px -4px rgba(45, 212, 191, 0.35);
        height: 100%;
        position: relative;
        overflow: hidden;
    }}
    
    .gradient-card-purple {{
        background: linear-gradient(135deg, #DDD6FE 0%, #C4B5FD 50%, #A78BFA 100%);
        border-radius: 24px;
        padding: 24px;
        color: #2E1065;
        box-shadow: 0 8px 24px -4px rgba(167, 139, 250, 0.35);
        height: 100%;
        position: relative;
        overflow: hidden;
    }}
    
    .card-label {{
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        opacity: 0.85;
    }}
    .card-val {{
        font-size: 38px;
        font-weight: 800;
        margin: 12px 0 4px 0;
        line-height: 1.1;
    }}
    .card-sub {{
        font-size: 13px;
        font-weight: 500;
        opacity: 0.8;
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

def process_pipeline(df, software_cost=100):
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
    user_grp['Flag_Cancel'] = user_grp['Automation_Rate'] >= 80
    
    tot_emps = len(user_grp)
    seats_to_cancel = int(user_grp['Flag_Cancel'].sum())
    savings = seats_to_cancel * software_cost
    
    return user_grp, tot_emps, seats_to_cancel, savings

# Default initialize session state data
if 'raw_data' not in st.session_state:
    st.session_state['raw_data'] = generate_sample_data(1200)

# ==========================================
# SIDEBAR CONTROLS
# ==========================================
with st.sidebar:
    st.markdown(f"<div style='display: flex; align-items: center; gap: 10px; margin-bottom: 8px;'><span style='font-size: 24px;'>⚡</span><h2 style='margin:0; font-size: 20px; font-weight: 700; color:{text_primary};'>AI Optimizer</h2></div>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 13px; color: {text_secondary}; margin-bottom: 20px;'>Intelligent Workforce & SaaS License Audit</p>", unsafe_allow_html=True)
    
    st.markdown(f"<div style='font-weight: 600; font-size: 14px; margin-bottom: 6px; color: {text_primary};'>Data Source</div>", unsafe_allow_html=True)
    
    col_btn, col_empty = st.columns([1, 0.01])
    with col_btn:
        if st.button("start"):
            with st.spinner("Generating fresh logs..."):
                st.session_state['raw_data'] = generate_sample_data(2000)
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload logs (CSV)", type=["csv"], help="Upload your custom usage_logs.csv")
    if uploaded is not None:
        st.session_state['raw_data'] = pd.read_csv(uploaded)
        
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-weight: 600; font-size: 14px; margin-bottom: 4px; color: {text_primary};'>Cost Parameters</div>", unsafe_allow_html=True)
    seat_cost = st.number_input("License Cost per Seat ($)", min_value=10, max_value=5000, value=100, step=10)
    
    st.divider()
    st.markdown(f"<div style='font-size: 12px; color: {text_secondary}; text-align: center;'>Engine version 2.4 • Active</div>", unsafe_allow_html=True)

# ==========================================
# MAIN DASHBOARD AREA
# ==========================================

# Top Navigation Bar Simulation
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown(f"""
    <div style='margin-bottom: 24px;'>
        <h1 style='font-size: 28px; font-weight: 700; color: {text_primary}; margin: 0;'>Welcome, Admin</h1>
        <p style='font-size: 14px; color: {text_secondary}; margin-top: 4px;'>Your executive license optimization overview</p>
    </div>
    """, unsafe_allow_html=True)
with header_col2:
    st.markdown(f"""
    <div style='text-align: right; padding-top: 6px;'>
        <span style='background: {"rgba(255,255,255,0.06)" if is_dark else "#FFFFFF"}; border: 1px solid {card_border}; border-radius: 20px; padding: 8px 16px; font-size: 13px; font-weight: 600; color: {text_primary}; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
            🟢 Engine Connected
        </span>
    </div>
    """, unsafe_allow_html=True)

# Run Processing
results_df, total_emps, seats_cancelled, total_savings = process_pipeline(st.session_state['raw_data'], seat_cost)

# ----------------------------------------------------
# ROW 1: MINIMAL GRADIENT METRIC CARDS (from Reference)
# ----------------------------------------------------
c_metric1, c_metric2, c_metric3, c_metric4 = st.columns(4)

with c_metric1:
    st.markdown(f"""
    <div class="custom-card">
        <div class="card-label" style="color: {text_secondary};">Total Workforce</div>
        <div class="card-val" style="color: {text_primary};">{total_emps:,}</div>
        <div class="card-sub" style="color: {text_secondary};">Active accounts analyzed</div>
    </div>
    """, unsafe_allow_html=True)

with c_metric2:
    pct_cut = round((seats_cancelled / total_emps * 100), 1) if total_emps else 0
    st.markdown(f"""
    <div class="gradient-card-coral">
        <div class="card-label">Prioritized Cuts</div>
        <div class="card-val">{pct_cut}%</div>
        <div class="card-sub">{seats_cancelled:,} Seats eligible for removal</div>
    </div>
    """, unsafe_allow_html=True)

with c_metric3:
    st.markdown(f"""
    <div class="gradient-card-teal">
        <div class="card-label">Monthly Recovery</div>
        <div class="card-val">${total_savings:,}</div>
        <div class="card-sub">Direct software savings @ ${seat_cost}/seat</div>
    </div>
    """, unsafe_allow_html=True)

with c_metric4:
    annual_savings = total_savings * 12
    st.markdown(f"""
    <div class="gradient-card-purple">
        <div class="card-label">Annual Projected ROI</div>
        <div class="card-val">${annual_savings:,}</div>
        <div class="card-sub">Run-rate reduction efficiency</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# ----------------------------------------------------
# ROW 2: ANALYTICS & FOCUS HEATMAP (Spline Curve Chart)
# ----------------------------------------------------
chart_left, chart_right = st.columns([1.8, 1.2])

with chart_left:
    st.markdown(f"""
    <div class="custom-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div>
                <h3 style="font-size: 17px; font-weight: 700; color: {text_primary}; margin: 0;">Focusing & Task Automation Velocity</h3>
                <p style="font-size: 13px; color: {text_secondary}; margin-top: 2px;">Productivity shift over quarters</p>
            </div>
            <span style="font-size: 12px; background: {input_bg}; border: 1px solid {input_border}; padding: 4px 10px; border-radius: 12px; color: {text_secondary}; font-weight: 600;">Range: Last 6 mo</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Smooth Spline Trend Chart (Matching Image 1 reference)
    months = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
    fig_spline = go.Figure()
    
    fig_spline.add_trace(go.Scatter(
        x=months, y=[32, 68, 45, 82, 60, 78],
        mode='lines',
        name='AI Automation Capacity',
        line=dict(color='#FF6584', width=3.5, shape='spline'),
    ))
    
    fig_spline.add_trace(go.Scatter(
        x=months, y=[75, 42, 65, 30, 52, 28],
        mode='lines',
        name='Manual Effort Required',
        line=dict(color='#4F46E5', width=3.5, shape='spline'),
    ))
    
    fig_spline.update_layout(
        plot_bgcolor=chart_bg,
        paper_bgcolor=chart_bg,
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(color=text_secondary, size=12)),
        xaxis=dict(showgrid=True, gridcolor=chart_grid, color=text_secondary, showline=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=chart_grid, color=text_secondary, showticklabels=False, showline=False, zeroline=False)
    )
    
    st.plotly_chart(fig_spline, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

with chart_right:
    st.markdown(f"""
    <div class="custom-card">
        <h3 style="font-size: 17px; font-weight: 700; color: {text_primary}; margin: 0 0 4px 0;">Developed Areas</h3>
        <p style="font-size: 13px; color: {text_secondary}; margin-bottom: 16px;">Departmental Automation Breakdown</p>
    """, unsafe_allow_html=True)
    
    dept_breakdown = results_df.groupby('Department').agg(
        Avg_Auto=('Automation_Rate', 'mean'),
        Cancels=('Flag_Cancel', 'sum')
    ).reset_index().sort_values(by='Avg_Auto', ascending=False)
    
    for _, row in dept_breakdown.iterrows():
        dept_name = row['Department']
        rate = int(row['Avg_Auto'])
        cancels = int(row['Cancels'])
        
        # Color indicator based on rate
        bar_color = "#FF6584" if rate >= 70 else ("#2DD4BF" if rate >= 40 else "#6366F1")
        
        st.markdown(f"""
        <div style="margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 600; margin-bottom: 4px;">
                <span style="color: {text_primary};">{dept_name}</span>
                <span style="color: {text_secondary};">{rate}% ({cancels} cuts)</span>
            </div>
            <div style="width: 100%; height: 8px; background-color: {input_bg}; border-radius: 999px; overflow: hidden; border: 1px solid {card_border};">
                <div style="width: {rate}%; height: 100%; background: {bar_color}; border-radius: 999px; transition: width 0.8s ease;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# ----------------------------------------------------
# ROW 3: ACTIONABLE SEATS TABLE
# ----------------------------------------------------
st.markdown(f"""
<div class="custom-card">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <div>
            <h3 style="font-size: 17px; font-weight: 700; color: {text_primary}; margin: 0;">Flagged Accounts for Seat Revocation</h3>
            <p style="font-size: 13px; color: {text_secondary}; margin-top: 2px;">Employees with &ge; 80% repetitive tasks automated</p>
        </div>
        <span style="background: rgba(255, 101, 132, 0.12); color: #FF6584; padding: 6px 14px; border-radius: 12px; font-size: 13px; font-weight: 700;">
            {seats_cancelled} Redundant Licenses
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
