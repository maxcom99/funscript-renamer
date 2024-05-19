import os
import time
import requests
import shutil
import json
import re
import argparse
from tqdm import tqdm

# Configuration variables
X = 2  # Delay between requests in seconds
dirDone = './done'
dirJson = './done/json'
dirProcessed = './processed'
dirNotFound = './not_found'
api_url_base = 'https://api.sexlikereal.com/virtualreality/video/id/'

# Ensure the required directories exist
for dir_path in [dirDone, dirJson, dirProcessed, dirNotFound]:
    os.makedirs(dir_path, exist_ok=True)

# Function to extract the ID from the filename
def extract_id(filename):
    match = re.search(r'\.(\d+)\.(\d+)(?:\.\d)?\.\w+$', filename)
    if match:
        return match.group(1)
    else:
        return None

# Function to clean and format the title and paysite name
def clean_text(text):
    # Replace forbidden characters
    text = re.sub(r'[<>:"/\\|?*]', ' ', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to extract resolution from the filename
def extract_resolution(filename):
    match = re.search(r'\d+p', filename)
    return match.group(0) if match else None

# Function to generate a unique filename
def generate_unique_filename(directory, base_name, extension):
    counter = 1
    new_name = f"{base_name}{extension}"
    while os.path.exists(os.path.join(directory, new_name)):
        new_name = f"{base_name}_{counter}{extension}"
        counter += 1
    return new_name

# Function to process each file
def process_file(file_path, dupe_action):
    filename = os.path.basename(file_path)
    file_id = extract_id(filename)
    
    json_file_path = os.path.join(dirJson, f"{file_id}.json")
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            title = clean_text(data.get('title', ''))
            paysite_name = clean_text(data.get('paysite', {}).get('name', ''))

        resolution = extract_resolution(filename)
        if resolution:
            new_filename = f"{paysite_name}_{title}_{resolution}_{file_id}.funscript"
        else:
            new_filename = f"{paysite_name}_{title}_{file_id}.funscript"

        new_file_path = os.path.join(dirDone, new_filename)

        # Handle duplicates based on dupe_action
        if os.path.exists(new_file_path):
            if dupe_action == 'skip':
                print(f"Skipping file {new_filename} as it already exists.")
                return
            elif dupe_action == 'replace':
                print(f"Replacing file {new_filename}.")
            elif dupe_action == 'rename':
                file_base_name, file_extension = os.path.splitext(new_filename)
                new_filename = generate_unique_filename(dirDone, file_base_name, file_extension)
                new_file_path = os.path.join(dirDone, new_filename)

        # Copy the file to dirDone
        shutil.copy2(file_path, new_file_path)
        # Move the original file to dirProcessed
        shutil.move(file_path, os.path.join(dirProcessed, filename))
    else:
        # Construct the API URL
        api_url = f'{api_url_base}{file_id}'
        
        # Make the GET request
        response = requests.get(api_url)
        
        if response.status_code == 200:
            if response.text == '{"error_message":"404 Not Found"}':
                # Move the file to the not_found directory
                shutil.move(file_path, os.path.join(dirNotFound, filename))
            else:
                json_path = os.path.join(dirJson, f'{file_id}.json')
                with open(json_path, 'w') as json_file:
                    json_file.write(response.text)
                
                # Move the processed file to the processed directory
                shutil.move(file_path, os.path.join(dirProcessed, filename))
        else:
            print(f"Failed to fetch data for ID {file_id}. Status code: {response.status_code}")
            # Move the file to the not_found directory
            shutil.move(file_path, os.path.join(dirNotFound, filename))

# Main script logic
def main():
    parser = argparse.ArgumentParser(description="Process and rename .funscript files.")
    parser.add_argument('--dupe', choices=['skip', 'replace', 'rename'], default='rename',
                        help="Action to take if a file with the new name already exists: 'skip' to skip the file, 'replace' to overwrite it, 'rename' to generate a unique name.")

    args = parser.parse_args()

    # Get a list of all .funscript files in the current directory
    funscript_files = [f for f in os.listdir('.') if f.endswith('.funscript')]
    total_files = len(funscript_files)

    print("Running Phase 1: Getting Meta Data")
    try:
        with tqdm(total=total_files, unit="file", desc="Processing files", ascii=True) as pbar:
            for filename in funscript_files:
                process_file(filename, args.dupe)
                pbar.update(1)
                time.sleep(X)
    except KeyboardInterrupt:
        print("\nAborted. Saving current progress...")

    print("Running Phase 2: Renaming")

    # Get a list of all files in dirProcessed for renaming
    processed_files = [f for f in os.listdir(dirProcessed) if f.endswith('.funscript')]
    total_files = len(processed_files)

    try:
        with tqdm(total=total_files, unit="file", desc="Renaming files", ascii=True) as pbar:
            for filename in processed_files:
                process_file(os.path.join(dirProcessed, filename), args.dupe)
                pbar.update(1)
    except KeyboardInterrupt:
        print("\nAborted during renaming. Leaving files in their current state.")

if __name__ == '__main__':
    main()
