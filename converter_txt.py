import json
import os

def json_to_txt(json_filepath, output_dir):
   try:
       # Read the JSON file
       with open(json_filepath, 'r') as json_file:
           data = json.load(json_file)


       # Convert JSON data to a formatted string
       formatted_data = json.dumps(data, indent=4)


       # Generate the output text file path
       base_filename = os.path.basename(json_filepath)
       txt_filename = os.path.splitext(base_filename)[0] + '.txt'
       txt_filepath = os.path.join(output_dir, txt_filename)


       # Write the formatted string to a text file
       with open(txt_filepath, 'w') as txt_file:
           txt_file.write(formatted_data)


       print(f"Converted {json_filepath} to {txt_filepath}")
   except json.JSONDecodeError as e:
       print(f"Error decoding JSON in file {json_filepath}: {e}")
   except Exception as e:
       print(f"An error occurred while processing file {json_filepath}: {e}")

def convert_all_json_to_txt(input_dir, output_dir):
   # Create the output directory if it doesn't exist
   os.makedirs(output_dir, exist_ok=True)


   # Iterate through all files in the input directory
   for root, dirs, files in os.walk(input_dir):
       for file in files:
           if file.endswith('.json'):
               json_filepath = os.path.join(root, file)
               json_to_txt(json_filepath, output_dir)


# Input and output directories
input_dir = r"C:/Users/codeineteh/Downloads/Xls_json/Xls_json"
output_dir = r"C:/Users/codeineteh/PycharmProjects/pythonProject/masterDB"


# Convert all JSON files in the input directory to text files in the output directory
convert_all_json_to_txt(input_dir, output_dir)

