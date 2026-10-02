import pandas as pd
import os

# Optional: For AI API approach using Gemini
# pip install google-genai
try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None

def classify_task_rule_based(task_description):
    """
    Simple keyword-based NLP classification.
    """
    task = str(task_description).lower()
    
    # Keywords that suggest a task is easily automatable
    automatable_keywords = ['copy', 'paste', 'data entry', 'sort', 'format', 'schedule', 'input', 'extract', 'compile']
    
    # Keywords that suggest human touch is needed
    human_keywords = ['negotiate', 'interview', 'design', 'strategy', 'resolve', 'brainstorm', 'counsel', 'lead']
    
    if any(keyword in task for keyword in human_keywords):
        return "Not Automatable"
    elif any(keyword in task for keyword in automatable_keywords):
        return "Automatable"
    else:
        return "Needs Review" # Fallback if unsure

def classify_task_ai(task_description, client):
    """
    Uses Gemini AI to classify the task. Requires GOOGLE_API_KEY environment variable.
    """
    prompt = f"""
    Analyze the following task and classify whether it is "Automatable" (can be done by AI/scripts) 
    or "Not Automatable" (requires human judgment, empathy, or physical action).
    Task: "{task_description}"
    
    Reply with ONLY "Automatable" or "Not Automatable".
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        # Clean up the response to just the category
        result = response.text.strip().title()
        if "Not Automatable" in result:
            return "Not Automatable"
        return "Automatable"
    except Exception as e:
        print(f"API Error for task '{task_description}': {e}")
        return "Error"

def process_tasks(input_csv='cleaned_data.csv', output_csv='classified_data.csv', use_ai=False):
    print(f"Loading data from {input_csv}...")
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"Error: Could not find {input_csv}. Please run Step 2 first!")
        return

    # Check if a 'Task' or 'Description' column exists
    task_col = None
    for col in ['Task', 'Description', 'Task Description', 'Job']:
        if col in df.columns:
            task_col = col
            break
            
    if not task_col:
        print("Warning: Could not find a 'Task' column to classify.")
        print("Available columns:", df.columns.tolist())
        return

    print(f"Classifying tasks in column '{task_col}'...")
    
    if use_ai and genai and os.environ.get('GOOGLE_API_KEY'):
        print("Using Gemini API for classification...")
        client = genai.Client()
        df['Automation_Status'] = df[task_col].apply(lambda x: classify_task_ai(x, client))
    else:
        if use_ai:
            print("Notice: google-genai package or GOOGLE_API_KEY not found. Falling back to rule-based NLP.")
        print("Using simple Rule-Based NLP for classification...")
        df['Automation_Status'] = df[task_col].apply(classify_task_rule_based)

    # Save the results
    df.to_csv(output_csv, index=False)
    print(f"\nSuccessfully classified tasks and saved to {output_csv}")
    
    # Show a summary of the classification
    print("\nClassification Summary:")
    print(df['Automation_Status'].value_counts())

if __name__ == "__main__":
    # Set use_ai=True if you want to use the Gemini API (requires pip install google-genai and GOOGLE_API_KEY)
    process_tasks(input_csv='cleaned_data.csv', output_csv='classified_data.csv', use_ai=False)
