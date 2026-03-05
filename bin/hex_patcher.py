import argparse
import sys
import os

# Hex Constants
SEARCH_PATTERN = "2D 76 00 69 61 6E 63 65 20 6F 6E 20 74 68 69 73 20 63 65 72 74 69 66 69 63 61 74 65 20 62 79 20 61 6E 79 20 70 61"

# Replacement for -a
REPLACE_A = "2D 76 20 61 6D 66 69 3D 30 78 66 66 20 63 73 5F 65 6E 66 6F 72 63 65 6D 65 6E 74 5F 64 69 73 61 62 6C 65 3D 31 00"

# Replacement for -r
REPLACE_R = "61 6D 66 69 3D 30 78 66 66 20 63 73 5F 65 6E 66 6F 72 63 65 6D 65 6E 74 5F 64 69 73 61 62 6C 65 3D 31 00 20 70 61"

def patch_file(file_path, mode):
    # Convert hex strings to bytes
    search_bytes = bytes.fromhex(SEARCH_PATTERN.replace(" ", ""))
    
    if mode == 'a':
        replace_bytes = bytes.fromhex(REPLACE_A.replace(" ", ""))
        label = "Mode -a (Append codesigning bootargs to verbose argument)"
    else:
        replace_bytes = bytes.fromhex(REPLACE_R.replace(" ", ""))
        label = "Mode -r (Replace verbose argument with codesigning bootargs)"

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        if search_bytes not in data:
            print("Error: Search pattern not found in the file.")
            sys.exit(1)

        print(f"Pattern found. Applying {label}...")
        new_data = data.replace(search_bytes, replace_bytes)

        with open(file_path, 'wb') as f:
            f.write(new_data)
        
        print("Successfully patched.")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Patch binary files with specific hex patterns.")
    parser.add_argument("file", help="The file to be patched")
    
    # Create a group so -a and -r can't be used at the same time
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", action="store_true", help="Append codesigning bootargs to verbose argument")
    group.add_argument("-r", action="store_true", help="Replace verbose argument with codesigning bootargs")

    args = parser.parse_args()

    mode = 'a' if args.a else 'r'
    patch_file(args.file, mode)
