import streamlit as st
import pandas as pd
import random
import time
import plotly.express as px

# ==========================================
# STEP 5: Beautiful Minimal UI (Streamlit)
# ==========================================
st.set_page_config(page_title="AI SaaS Optimizer", layout="wide", page_icon="✨")

# Inject Custom CSS for Minimal Soft/Neumorphic UI
st.markdown("""
<style>
    /* Main Background - Soft light gray like the dashboard image */
    .stApp {
        background-color: #f4f5f7;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Header */
    header {visibility: hidden;}

    /* Styling the Metric Cards (Glassmorphic / Soft look) */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #ffffff 0%, #f9f9fa 100%);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.8);
    }
    div[data-testid="metric-container"] label {
        color: #64748b;
        font-weight: 500;
        font-size: 14px;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #0f172a;
        font-weight: 700;
        font-size: 36px;
    }

    /* Neumorphic Dark Button (from Image 2) */
    .stButton > button {
        background: #2a2a2a !important;
        color: #a0a0a0 !important;
        border: 1px solid #3a3a3a !important;
        border-radius: 20px !important;
        padding: 10px 30px !important;
        font-size: 18px !important;
        font-weight: 500 !important;
        letter-spacing: 1px;
        box-shadow: 
            inset 2px 2px 5px rgba(255,255,255,0.05), 
            inset -3px -3px 7px rgba(0,0,0,0.5),
            4px 4px 10px rgba(0,0,0,0.2) !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        color: #ffffff !important;
        transform: translateY(-1px);
        box-shadow: 
            inset 2px 2px 5px rgba(255,255,255,0.08), 
            inset -3px -3px 7px rgba(0,0,0,0.6),
            5px 5px 12px rgba(0,0,0,0.3) !important;
    }
    .stButton > button:active {
        transform: translateY(2px);
        box-shadow: 
            inset 3px 3px 7px rgba(0,0,0,0.6), 
            inset -2px -2px 5px rgba(255,255,255,0.05) !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Clean up the dataframe */
    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# STEP 1: Fake Data Generation
# ==========================================
def generate_sample_data(num_rows=500):
    user_ids = [f"EMP-{str(i).zfill(3)}" for i in range(1, (num_rows // 5) + 2)]
    departments = ['Sales', 'HR', 'IT', 'Customer Support', 'Marketing']
    
    automatable_tasks = ['Copy-pasting emails', 'Data entry', 'Sorting spreadsheets', 'Scheduling']
    human_tasks = ['Negotiating', 'Interviewing', 'Strategy planning', 'Designing', 'Resolving conflict']

    data = []
    for _ in range(num_rows):
        dept = random.choice(departments)
        user_id = random.choice(user_ids)
        task = random.choice(human_tasks + automatable_tasks) if dept in ['IT', 'HR'] else random.choice(automatable_tasks + human_tasks)
        data.append({'User_ID': user_id, 'Department': dept, 'Task_Description': task})
    return pd.DataFrame(data)

# ==========================================
# STEP 2 & 3 & 4: Processing
# ==========================================
def clean_data(df):
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].astype(str).str.strip().str.title()
    return df

def classify_task(task_description):
    task = str(task_description).lower()
    auto = ['copy', 'paste', 'data', 'sort', 'format', 'schedule', 'extract', 'compile']
    human = ['negotiate', 'interview', 'design', 'strategy', 'resolve', 'brainstorm', 'counsel', 'lead']
    if any(k in task for k in human): return "Not Automatable"
    elif any(k in task for k in auto): return "Automatable"
    return "Needs Review"

def classify_dataframe(df):
    if 'Task_Description' in df.columns:
        df['Automation_Status'] = df['Task_Description'].apply(classify_task)
    return df

def calculate_financials(df, software_cost=100):
    if 'User_ID' not in df.columns or 'Automation_Status' not in df.columns:
        return pd.DataFrame(), 0, 0, 0
    df['Is_Automatable_Num'] = df['Automation_Status'].apply(lambda x: 1 if x == 'Automatable' else 0)
    user_stats = df.groupby(['User_ID', 'Department']).agg(
        Total_Tasks=('Automation_Status', 'count'),
        Automatable_Tasks=('Is_Automatable_Num', 'sum')
    ).reset_index()
    user_stats['Automation_Percentage'] = (user_stats['Automatable_Tasks'] / user_stats['Total_Tasks']) * 100
    user_stats['Cancel_Account'] = user_stats['Automation_Percentage'] >= 80
    return user_stats, len(user_stats), user_stats['Cancel_Account'].sum(), user_stats['Cancel_Account'].sum() * software_cost


# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ✨ Welcome, Admin")
    st.markdown("Your optimization dashboard")
    st.divider()
    
    if st.button("start"):
        st.session_state['raw_data'] = generate_sample_data(1000)
        
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        st.session_state['raw_data'] = pd.read_csv(uploaded_file)
        
    software_cost = st.number_input("License Cost ($)", value=100, step=10)

# --- MAIN DASHBOARD ---
st.markdown("<h2 style='font-weight: 600; color: #1e293b; margin-bottom: 30px;'>Optimization Overview</h2>", unsafe_allow_html=True)

if 'raw_data' not in st.session_state:
    st.info("Click 'start' in the sidebar or upload data.")
else:
    with st.spinner("Analyzing..."):
        time.sleep(0.5)
        cleaned_df = clean_data(st.session_state['raw_data'].copy())
        classified_df = classify_dataframe(cleaned_df)
        results_df, total_emps, seats_cancelled, total_savings = calculate_financials(classified_df, software_cost)
        
    if not results_df.empty:
        # TOP METRICS
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Employees", f"{total_emps:,}")
        with c2: st.metric("Seats to Cancel", f"{seats_cancelled:,}", "+83% Avg. Completed") # Mimicking the image text vibe
        with c3: st.metric("Dollars Saved", f"${total_savings:,}", "+56% Additional")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # CHARTS (Minimal styling)
        dept_stats = results_df.groupby('Department').agg(
            Avg_Automation=('Automation_Percentage', 'mean'),
            Accounts_Flagged=('Cancel_Account', 'sum')
        ).reset_index()
        
        # Create a smooth line chart similar to the "Focusing" chart in image 1
        st.markdown("<h4 style='font-weight: 600; color: #1e293b;'>Productivity analytics</h4>", unsafe_allow_html=True)
        
        # Fake some timeline data for the beautiful spline chart
        timeline_data = pd.DataFrame({
            'Month': ['Aug', 'Sep', 'Oct', 'Nov'],
            'Max Focus': [40, 80, 30, 60],
            'Min Focus': [20, 60, 40, 50]
        })
        
        fig_line = px.line(
            timeline_data, x='Month', y=['Max Focus', 'Min Focus'],
            color_discrete_sequence=['#ff6b6b', '#4834d4']
        )
        fig_line.update_traces(line_shape='spline', line=dict(width=3))
        fig_line.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#f1f2f6', title='', showline=False, zeroline=False),
            yaxis=dict(showgrid=True, gridcolor='#f1f2f6', title='', showticklabels=False, showline=False, zeroline=False),
            legend_title='',
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # DATA TABLE
        st.markdown("<h4 style='font-weight: 600; color: #1e293b; margin-top: 30px;'>Developed areas (Actionable Licenses)</h4>", unsafe_allow_html=True)
        cancellations = results_df[results_df['Cancel_Account'] == True].copy()
        cancellations['Automation_Percentage'] = cancellations['Automation_Percentage'].round(1).astype(str) + "%"
        st.dataframe(cancellations.drop(columns=['Cancel_Account']), use_container_width=True)
