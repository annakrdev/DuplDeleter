import argparse
import hashlib
import glob
import os

def calculate_hash(file_path, algorithm='sha256'):
    if os.path.isfile(file_path):  # Check if it's a file
        with open(file_path, 'rb') as file:
            hash_object = hashlib.new(algorithm)
            while True:
                block = file.read(4096)
                if not block:
                    break
                hash_object.update(block)
        hash_value = hash_object.hexdigest()
        return hash_value
    else:
        return None

def array_filler(folder_path, file_extensions=None, recursive=False):
    hash_result_array = []

    if file_extensions:
        for ext in file_extensions:
            if recursive:
                files = glob.glob(os.path.join(folder_path, f'**/*.{ext}'), recursive=True)
            else:
                files = glob.glob(os.path.join(folder_path, f'*.{ext}'))
            for file_path in files:
                result_hash = calculate_hash(file_path)
                if result_hash is not None:
                    file_name = os.path.relpath(file_path, folder_path)
                    hash_result_array.append((file_name, result_hash))
    else:
        if recursive:
            files = glob.glob(os.path.join(folder_path, '**/*'), recursive=True)
        else:
            files = glob.glob(os.path.join(folder_path, '*'))
        for file_path in files:
            result_hash = calculate_hash(file_path)
            if result_hash is not None:
                file_name = os.path.relpath(file_path, folder_path)
                hash_result_array.append((file_name, result_hash))

    return hash_result_array

def match_hash_checker(hash_sum_array):
    hash_dict = {}
    duplicates = []

    for filename, hash_sum in hash_sum_array:
        if hash_sum in hash_dict:
            hash_dict[hash_sum].append(filename)
        else:
            hash_dict[hash_sum] = [filename]

    for hash_sum, filenames in hash_dict.items():
        if len(filenames) > 1:
            duplicates.append((hash_sum, filenames))
    return duplicates

def remove_files(delete_list, folder_path):
    for item in delete_list:
        file_path = os.path.join(folder_path, item)
        try:
            os.remove(file_path)
            print(f"File {file_path} successfully deleted.")
        except OSError as e:
            print(f"Error deleting file {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Check and remove duplicate files in a folder.")
    parser.add_argument("folder_path", help="Path to the folder containing files.")
    parser.add_argument("file_extensions", nargs='*', help="File extensions to check for duplicates.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Search files in all subdirectories recursively.")
    args = parser.parse_args()

    folder_path = args.folder_path.strip()
    file_extensions = args.file_extensions
    recursive = args.recursive

    hash_result_array = array_filler(folder_path, file_extensions, recursive)
    duplicate_hash = match_hash_checker(hash_result_array)

    checker = False
    delete_list = []

    if duplicate_hash:
        checker = True
        print("Duplicates found:")
        for hash_sum, found_dupls in duplicate_hash:
            print(f"\tFor hash sum {hash_sum} of file {found_dupls[0]} found a clone - {', '.join(found_dupls[1:])}")
            delete_list.append(found_dupls[1:])
    else:
        print("No duplicates found")

    if checker:
        delete_question = input("\nDo you want to REMOVE duplicates? Yes/No: ").lower()
        if delete_question == "y" or delete_question == "yes":
            delete_list_1d = sum(delete_list, [])
            remove_files(delete_list_1d, folder_path)
        elif delete_question != "n" and delete_question != "no":
            print("Incorrect input")

if __name__ == "__main__":
    main()
