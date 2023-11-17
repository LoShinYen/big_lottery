import json
import os

def convert_to_json(directory_path):
    # Initialize an empty list to store all lottery data
    lottery_data = []

    # Walk through the directory
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # Check if the file is a txt file
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                # Open the file and read it line by line
                with open(file_path, 'r', encoding='utf-8') as file:
                    entry = {}
                    for line in file:
                        line = line.strip()
                        if not line or line.startswith('----------------------------------------'):
                            # Skip empty lines and separators
                            if entry:  # If entry dict is not empty, an entry has ended
                                lottery_data.append(entry)
                                entry = {}  # Reset entry dict for the next entry
                            continue
                        key, value = line.split(': ', 1)  # Split the key and value
                        if key == 'Open_Date':
                            entry['Open_Date'] = value
                        elif key == 'Number':
                            # Convert number string to a list of integers
                            entry['Number'] = [int(num) for num in value.split(', ')]
                        elif key == 'Special':
                            entry['Special'] = int(value)

    # Convert the list to JSON format
    json_data = json.dumps({'data': lottery_data}, ensure_ascii=False, indent=4)
    return json_data

# The path to the directory containing the txt files
directory_path = './crawl_data'

# Convert all txt files in the directory to JSON
lottery_json_data = convert_to_json(directory_path)

# Print out the JSON data
print(lottery_json_data)

# Optionally, save the JSON data to a file
json_file_path = './json/all_lottery_data.json'
os.makedirs(os.path.dirname(json_file_path), exist_ok=True)  # Create the directory if it doesn't exist
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json_file.write(lottery_json_data)
