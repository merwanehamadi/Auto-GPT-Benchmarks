import os
import json
import base64
import pandas as pd
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# Load environment variables from .env file
load_dotenv()

# Get the base64 string from the environment variable
base64_creds = os.getenv("MY_BASE64_STRING")

# Decode the base64 string into bytes
creds_bytes = base64.b64decode(base64_creds)

# Convert the bytes into a string
creds_string = creds_bytes.decode('utf-8')

# Parse the string into a JSON object
creds_info = json.loads(creds_string)

# Define the base directory containing JSON files
base_dir = "reports"

# Create a list to store each row of data
rows = []

# Loop over each directory in the base directory
for sub_dir in os.listdir(base_dir):
    # Define the subdirectory path
    sub_dir_path = os.path.join(base_dir, sub_dir)

    # Ensure the sub_dir_path is a directory
    if os.path.isdir(sub_dir_path):
        # Loop over each file in the subdirectory
        for filename in os.listdir(sub_dir_path):
            # Check if the file is a JSON file
            if filename.endswith(".json"):
                # Define the file path
                file_path = os.path.join(sub_dir_path, filename)

                # Load the JSON data from the file
                with open(file_path, "r") as f:
                    data = json.load(f)

                # Loop through each test
                for test_name, test_info in data["tests"].items():
                    # Create a dictionary to hold the information for this row
                    row = {
                        "Agent": sub_dir,
                        "Command": data["command"],
                        "Completion Time": data["completion_time"],
                        "Total Run Time": data["metrics"]["run_time"],
                        "Highest Difficulty": data["metrics"]["highest_difficulty"],
                        "Workspace": data["config"]["workspace"],
                        "Test Name": test_name,
                        "Data Path": test_info["data_path"],
                        "Is Regression": test_info["is_regression"],
                        "Difficulty": test_info["metrics"]["difficulty"],
                        "Success": test_info["metrics"]["success"],
                        "Success %": test_info["metrics"]["success_%"],
                        "Run Time": test_info["metrics"]["run_time"]
                    }

                    # Add this row to the list
                    rows.append(row)

# Convert the list of rows into a DataFrame
df = pd.DataFrame(rows)

# Define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# Add your service account credentials
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)

# Authorize the clientsheet
client = gspread.authorize(creds)

# Get the instance of the Spreadsheet
sheet = client.open('test-benchmark')

# Get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

# Convert dataframe to list of lists for uploading to Google Sheets
values = df.values.tolist()

# Prepend the header to the values list
values.insert(0, df.columns.tolist())

# Clear the existing values in the worksheet
sheet_instance.clear()

# Update the worksheet with the new values
sheet_instance.append_rows(values)