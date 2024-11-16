"""
Module: EPUB File Consistency Checker

This script ensures consistency between metadata entries in a CSV file and corresponding EPUB files in a directory. 
It provides two key functionalities to help users verify the presence and alignment of metadata and EPUB files.

## Features:
1. **Check for Missing EPUB Files**:
   - Reads a CSV file containing metadata, including an `ID` column.
   - Verifies if an EPUB file exists in a specified directory for each ID in the metadata.
   - Outputs a list of IDs that are missing corresponding EPUB files.

2. **Check for EPUB Files without Metadata**:
   - Lists EPUB files in a specified directory.
   - Identifies EPUB files that do not have a corresponding entry in the CSV metadata file.

## Usage:
1. Ensure the metadata file is named `stories_metadata.csv`, or update the `csv_file_path` variable to the correct path.
2. Place the EPUB files in a directory named `content`, or update the `epub_directory` variable to the correct path.
3. Ensure the `ID` column in the CSV file matches the naming convention of the EPUB files (e.g., an entry with ID `123` should have a corresponding `123.epub` file).
4. Run the script to validate metadata and EPUB file consistency.

## Exception Handling:
- Handles errors related to missing or inaccessible files and directories.
- Provides clear error messages to guide the user in resolving issues.

## Output:
1. For missing EPUB files:
   - If any IDs are missing EPUB files, the script lists their IDs.
   - If all files are present, it confirms all metadata entries have corresponding EPUB files.
2. For EPUB files without metadata:
   - Lists EPUB files without a matching entry in the CSV file.
   - Confirms if all EPUB files have corresponding metadata entries.

## Example:
### Input Metadata (CSV):
ID,Title,Author
123,Story A,Author X
124,Story B,Author Y
125,Story C,Author Z

### EPUB Files in `content` Directory:
- `123.epub`
- `125.epub`
- `126.epub`

### Output:
- Missing EPUB files:
The following IDs do not have corresponding EPUB files:
124

- EPUB files without metadata:
The following EPUB files do not have corresponding entries in the CSV file:
126.epub
"""

import os
import csv

# Define paths
csv_file_path = "stories_metadata.csv"
epub_directory = "content"


# Function to check for missing EPUB files
def find_missing_epubs(csv_file_path, epub_directory):
    missing_ids = []
    try:
        # Open and read the CSV file
        with open(csv_file_path, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Replace 'ID' with the actual column name in your CSV that contains the ID
                file_id = row["ID"]
                epub_file = os.path.join(epub_directory, f"{file_id}.epub")
                if not os.path.exists(epub_file):
                    missing_ids.append(file_id)

        # Print IDs with missing EPUB files
        if missing_ids:
            print("The following IDs do not have corresponding EPUB files:")
            for file_id in missing_ids:
                print(file_id)
        else:
            print("All IDs have corresponding EPUB files.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to check for EPUB files without corresponding CSV entries
def find_epubs_without_csv_entries(csv_file_path, epub_directory):
    try:
        # Get all EPUB filenames from the directory
        epub_files = [f for f in os.listdir(epub_directory) if f.endswith(".epub")]
        epub_ids = {
            os.path.splitext(f)[0] for f in epub_files
        }  # Extract file IDs without extensions

        # Get all IDs from the CSV file
        csv_ids = set()
        with open(csv_file_path, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                csv_ids.add(row["ID"])

        # Find EPUB files without corresponding CSV entries
        missing_in_csv = epub_ids - csv_ids

        # Print results
        if missing_in_csv:
            print("The following EPUB files do not have corresponding entries in the CSV file:")
            for file_id in missing_in_csv:
                print(f"{file_id}.epub")
        else:
            print("All EPUB files have corresponding entries in the CSV file.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Call the function
find_missing_epubs(csv_file_path, epub_directory)

# Call the function
find_epubs_without_csv_entries(csv_file_path, epub_directory)
