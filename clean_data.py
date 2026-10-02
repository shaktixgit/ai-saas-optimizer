import pandas as pd

def clean_and_group_data(input_csv, output_csv='cleaned_data.csv'):
    print(f"Loading data from {input_csv}...")
    df = pd.read_csv(input_csv)
    
    print("Cleaning up messy text...")
    # Clean up messy text in string columns (strip whitespace, standardize to title case)
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].astype(str).str.strip().str.title()
        
    # Check if 'Department' column exists to organize by it
    if 'Department' in df.columns:
        print("Organizing data by Department (Sales, HR, IT)...")
        # Sort by Department so it is organized together
        df = df.sort_values(by='Department')
        
        # Group by department to demonstrate grouping
        grouped = df.groupby('Department')
        for dept, group_df in grouped:
            print(f"\n--- {dept} Department ---")
            print(group_df.head()) # Print first few rows of each group
    else:
        print("Warning: 'Department' column not found in the dataset.")
        
    # Save the cleaned and organized data
    df.to_csv(output_csv, index=False)
    print(f"\nCleaned data successfully saved to {output_csv}")

    return df

if __name__ == "__main__":
    # Replace 'spreadsheet.csv' with the actual filename from Step 1
    df = clean_and_group_data('spreadsheet.csv')
