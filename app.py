import streamlit as st
import pandas as pd
import random
import time
import plotly.express as px

# ==========================================
# STEP 1: Fake Data Generation
# ==========================================
def generate_sample_data(num_rows=500):
    user_ids = [f"EMP-{str(i).zfill(3)}" for i in range(1, (num_rows // 5) + 2)]
    departments = ['Sales', 'HR', 'IT', 'Customer Support', 'Marketing']
    
    # Task pools
    automatable_tasks = [
        'Copy-pasting emails into CRM', 
        'Data entry from invoices', 
        'Sorting spreadsheets', 
        'Scheduling calendar invites',
        'Extracting numbers from PDFs',
        'Formatting reports'
    ]
    human_tasks = [
        'Negotiating a client contract', 
        'Interviewing new candidates', 
        'High-level strategy planning', 
        'Designing a new brand logo', 
        'Resolving employee conflict',
        'Leading a brainstorming session'
    ]

    data = []
    for _ in range(num_rows):
        dept = random.choice(departments)
        user_id = random.choice(user_ids)
        
        # Make some departments more automatable than others for realistic variance
        if dept in ['IT', 'HR']: 
            task = random.choice(human_tasks + automatable_tasks[:2])
        else:
            task = random.choice(automatable_tasks + human_tasks[:2])
            
        data.append({
            'User_ID': user_id,
            'Department': dept,
            'Task_Description': task
        })
    return pd.DataFrame(data)

# ==========================================
# STEP 2: Data Cleaning
# ==========================================
def clean_data(df):
    # Strip whitespace and title case string columns
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].astype(str).str.strip().str.title()
    return df

# ==========================================
# STEP 3: NLP Classification (Rule-Based)
# ==========================================
def classify_task(task_description):
    task = str(task_description).lower()
    
    automatable_keywords = ['copy', 'paste', 'data entry', 'sort', 'format', 'schedule', 'extract', 'compile']
    human_keywords = ['negotiate', 'interview', 'design', 'strategy', 'resolve', 'brainstorm', 'counsel', 'lead']
    
    if any(keyword in task for keyword in human_keywords):
        return "Not Automatable"
    elif any(keyword in task for keyword in automatable_keywords):
        return "Automatable"
    return "Needs Review"

def classify_dataframe(df):
    if 'Task_Description' in df.columns:
        df['Automation_Status'] = df['Task_Description'].apply(classify_task)
    return df

# ==========================================
# STEP 4: Financial Math
# ==========================================
def calculate_financials(df, software_cost=100):
    if 'User_ID' not in df.columns or 'Automation_Status' not in df.columns:
        return pd.DataFrame(), 0, 0, 0
        
    df['Is_Automatable_Num'] = df['Automation_Status'].apply(lambda x: 1 if x == 'Automatable' else 0)
    
    # Group by User and keep Department
    user_stats = df.groupby(['User_ID', 'Department']).agg(
        Total_Tasks=('Automation_Status', 'count'),
        Automatable_Tasks=('Is_Automatable_Num', 'sum')
    ).reset_index()
    
    user_stats['Automation_Percentage'] = (user_stats['Automatable_Tasks'] / user_stats['Total_Tasks']) * 100
    user_stats['Cancel_Account'] = user_stats['Automation_Percentage'] >= 80
    
    total_employees = len(user_stats)
    seats_to_cancel = user_stats['Cancel_Account'].sum()
    total_saved = seats_to_cancel * software_cost
    
    return user_stats, total_employees, seats_to_cancel, total_saved

# ==========================================
# STEP 5: Streamlit Web Dashboard (UI/UX)
# ==========================================
st.set_page_config(page_title="AI SaaS Optimizer", layout="wide", page_icon="⚡")

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚡ AI SaaS Optimization Engine")
    st.markdown("""
    Welcome to the optimization engine! This app analyzes employee task logs to determine if their software licenses are actually needed, or if AI can fully automate their workflows.
    """)
    st.divider()
    
    st.header("1. Input Data")
    if st.button("Generate Sample Data", use_container_width=True):
        st.session_state['raw_data'] = generate_sample_data(1000)
        
    uploaded_file = st.file_uploader("Or upload your usage_logs.csv", type=["csv"])
    if uploaded_file is not None:
        st.session_state['raw_data'] = pd.read_csv(uploaded_file)
        
    software_cost = st.number_input("Cost per Software License ($)", value=100, step=10)

# --- MAIN DASHBOARD ---
st.title("Dashboard: License Optimization Results")

if 'raw_data' not in st.session_state:
    st.info("👈 Please generate sample data or upload a CSV in the sidebar to begin.")
else:
    # --- PROCESSING ENGINE ---
    with st.spinner("Analyzing workflows with AI..."):
        time.sleep(1) # Artificial delay for professional UX effect
        
        # Step 2
        cleaned_df = clean_data(st.session_state['raw_data'].copy())
        
        # Step 3
        classified_df = classify_dataframe(cleaned_df)
        
        # Step 4
        results_df, total_emps, seats_cancelled, total_savings = calculate_financials(classified_df, software_cost)
        
    if results_df.empty:
        st.error("The uploaded CSV is missing required columns: 'User_ID' or 'Task_Description'.")
    else:
        # --- TOP ROW: METRICS ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Employees Analyzed", f"{total_emps:,}")
        with col2:
            st.metric("Software Seats to Cancel", f"{seats_cancelled:,}", delta="Redundant")
        with col3:
            st.metric("Total Dollars Saved", f"${total_savings:,}", delta="Estimated ROI")
            
        st.divider()
        
        # --- MIDDLE ROW: CHARTS ---
        st.subheader("Automation Potential by Department")
        
        # Aggregate data for charting
        dept_stats = results_df.groupby('Department').agg(
            Avg_Automation=('Automation_Percentage', 'mean'),
            Accounts_Flagged=('Cancel_Account', 'sum')
        ).reset_index()
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Bar Chart
            fig_bar = px.bar(
                dept_stats, 
                x='Department', 
                y='Avg_Automation', 
                title='Average Automatable Tasks (%) per Department',
                labels={'Avg_Automation': '% Automatable'},
                color='Avg_Automation',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with chart_col2:
            # Heat Map equivalent (Scatter plot mapping impact vs accounts)
            fig_scatter = px.scatter(
                dept_stats,
                x='Avg_Automation',
                y='Accounts_Flagged',
                size='Accounts_Flagged',
                color='Department',
                title='Risk / Savings Heat-Map',
                labels={'Avg_Automation': 'Feasibility (% Automatable)', 'Accounts_Flagged': 'Impact (Seats to Cancel)'},
                size_max=40
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        st.divider()
        
        # --- BOTTOM ROW: DATA TABLE ---
        st.subheader("Actionable Results: Specific Licenses to Cancel")
        
        # Filter to only show users who we should cancel
        cancellations = results_df[results_df['Cancel_Account'] == True].copy()
        
        # Format for clean display
        cancellations['Automation_Percentage'] = cancellations['Automation_Percentage'].round(1).astype(str) + "%"
        cancellations = cancellations.drop(columns=['Cancel_Account'])
        
        st.dataframe(
            cancellations.sort_values(by='Total_Tasks', ascending=False),
            use_container_width=True,
            column_config={
                "User_ID": "Employee ID",
                "Department": "Department",
                "Total_Tasks": "Total Logged Tasks",
                "Automatable_Tasks": "Tasks AI Can Do",
                "Automation_Percentage": "Automation %"
            }
        )
