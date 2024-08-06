import os
import pandas as pd
import json

def excel_to_json_txt(input_folder, output_folder):
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Iterate over all Excel files in the input directory
    for filename in os.listdir(input_folder):
        if filename.endswith(".xls") or filename.endswith(".xlsx"):
            # Skip temporary files
            if filename.startswith("~$"):
                continue
            
            file_path = os.path.join(input_folder, filename)
            try:
                excel_data = pd.ExcelFile(file_path, engine='openpyxl')
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue
            
            # Dictionary to hold all sheets data
            all_sheets_data = {}
            
            for sheet_name in excel_data.sheet_names:
                # Read each sheet into a DataFrame
                df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, engine='openpyxl')
                
                # Find the header row (assuming the first non-empty row is the header)
                for i, row in df.iterrows():
                    if not row.isnull().all():
                        header_row = i
                        break
                
                # Read the sheet again with the correct header
                df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row, engine='openpyxl')
                
                # Convert the DataFrame to a dictionary
                sheet_data = df.to_dict(orient='records')
                all_sheets_data[sheet_name] = sheet_data
            
            # Convert the dictionary to a JSON string
            json_data = json.dumps(all_sheets_data, indent=4)
            
            # Write the JSON string to a text file
            output_file_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_file_path, 'w') as txt_file:
                txt_file.write(json_data)

# Define the input and output directories
input_folder = r"C:\Users\aurtshet\Box\Assessment Program\AI Assessment Program\Spreadsheets"
output_folder = r"C:\Users\aurtshet\Box\Assessment Program\AI Assessment Program\ai wise\.venv\masterDB"

# Run the function
excel_to_json_txt(input_folder, output_folder)
