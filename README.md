# DuplDeleter.py

Please exercise caution when deleting files, and ensure you have a backup if needed. Have a good day.

## Overview
DuplDeleter.py is a Python script designed to check and remove duplicate files within a specified folder. It calculates the hash values of files to identify duplicates and provides options to remove them.

## Usage
1. Clone or download the repository to your local machine.

2. Open a terminal and navigate to the directory where `DuplDeleter.py` is located.

3. Run the script with the following command:
   ```bash
   python3 DuplDeleter.py folder_path [file_extensions] [-r]

folder_path: Path to the folder containing files.
file_extensions: (Optional) Specify file extensions to check for duplicates.
-r or --recursive: (Optional) Search files in all subdirectories recursively.

The script will display information about duplicate files found, including their hash values.

If duplicates are found, you will be prompted to confirm if you want to remove them.

Respond with "Yes" or "No" to proceed or abort the deletion process.

## Example

Check for duplicate files in the folder '/home/user/Documents' with file extensions 'txt' and 'pdf', including subdirectories:
   ```bash
   python3 DuplDeleter.py /home/user/Documents txt pdf -r
