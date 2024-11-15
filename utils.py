import os

def print_folder_tree_excluding_git(folder_path, indent=''):
    try:
        # Get a list of all items in the current directory
        items = os.listdir(folder_path)
    except PermissionError:
        print(f"{indent}[Permission Denied]")
        return

    # Loop through each item in the folder
    for index, item in enumerate(sorted(items)):
        # Skip .git directory and its contents
        if item == '.git':
            continue

        # Construct the full item path
        item_path = os.path.join(folder_path, item)
        # Print the item with tree structure symbols
        connector = '├── ' if index < len(items) - 1 else '└── '
        print(f"{indent}{connector}{item}")

        # If the item is a directory, recursively print its contents
        if os.path.isdir(item_path):
            new_indent = indent + ('│   ' if index < len(items) - 1 else '    ')
            print_folder_tree_excluding_git(item_path, new_indent)


# Example usage:
FOLDER = r'C:\Users\User\OneDrive\Desktop\Code\ConnectFour'

print_folder_tree_excluding_git(FOLDER)