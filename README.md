<div align="center">

# ⚡ AI-Driven SaaS Optimization Engine

<p align="center">
  <a href="https://ai-saas-optimizer-xx3kq4f5ngjcs3urmyjh2x.streamlit.app/">
    <img src="https://img.shields.io/badge/🟢_LIVE_APP-CLICK_HERE_TO_TEST_THE_DASHBOARD-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live App" />
  </a>
</p>

<a href="https://git.io/typing-svg">
<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&color=4ADE80&background=0F172A&center=true&vCenter=true&width=800&lines=Analyze+SaaS+Licenses+with+AI;Identify+Redundant+Software+Accounts;Calculate+Instant+Financial+Savings;Data+Generation+%E2%86%92+Cleaning+%E2%86%92+NLP+%E2%86%92+Reporting" alt="Typing SVG" />
</a>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white" />
</p>

An intelligent, 5-step pipeline wrapped in a beautiful web application to help enterprises discover which employee software licenses can be safely canceled by leveraging Natural Language Processing (NLP) to detect highly automatable workflows.

</div>

---

## ✨ Features at a Glance

*   **1. Realistic Data Generation:** Simulates thousands of rows of realistic employee usage logs (`usage_logs.csv`), balancing automatable and non-automatable tasks across different departments.
*   **2. Data Cleaning & Normalization:** Employs `pandas` to sanitize messy text, strip whitespaces, and standardize case formats instantly.
*   **3. NLP Task Classification (The Brain):** Scans the text of every logged task and intelligently classifies it as **"Automatable"** or **"Not Automatable"** (differentiating data-entry from high-level strategy).
*   **4. Financial Math:** Analyzes user automation ratios. If an employee's tasks are `>= 80%` automatable, their software seat is flagged for cancellation.
*   **5. Executive Dashboard:** A rich, interactive Streamlit UI featuring a **Risk/Savings Heat-Map** and real-time ROI metrics.

---

## 🚀 Quick Start

### 1. View the Live App
No installation required! Simply visit the live deployment hosted on Streamlit Community Cloud:
👉 **[Launch AI SaaS Optimizer](https://ai-saas-optimizer-xx3kq4f5ngjcs3urmyjh2x.streamlit.app/)**

*(We have also provided a 20,000-row demo dataset `demo_usage_logs.csv` in this repository that you can upload to the live app!)*

### 2. Run Locally
```bash
git clone https://github.com/shaktixgit/ai-saas-optimizer.git
cd ai-saas-optimizer
pip install -r requirements.txt
streamlit run app.py
```

---

## 📸 Dashboard Preview

The dashboard handles data processing entirely behind the scenes and instantly renders three core layers:

1. **Top-Level Metrics:** Instantly see total employees analyzed, seats flagged for cancellation, and total estimated ROI.
2. **Departmental Heat-Map:** A Plotly scatter graph to visually map "Feasibility of Automation" vs "Impact (Seats to Cancel)".
3. **Actionable Table:** Clean, sortable data grid outputting the exact user IDs whose software licenses can be revoked.

<div align="center">
  <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Streamlit-Dark.svg" height="40" alt="Streamlit Logo"/>
  <p><i>Built seamlessly entirely in Python</i></p>
</div>

---

## 🧠 The 5-Step Pipeline Structure

| Step | Script File | Purpose |
| :--- | :--- | :--- |
| **Step 1** | `generate_logs.py` | Generates simulated SaaS task logs. |
| **Step 2** | `clean_data.py` | Standardizes string formats and fixes messy CSV data. |
| **Step 3** | `classify_tasks.py` | Assigns automation likelihood using NLP keywords/GenAI. |
| **Step 4** | `calculate_savings.py` | Aggregates the data and flags accounts >80% automated. |
| **Step 5** | `app.py` | Combines Steps 1-4 into the Streamlit Web Application. |

---

<div align="center">
  <br>
  <b>Optimizing enterprise software spend, one task at a time.</b>
  <br><br>
</div>