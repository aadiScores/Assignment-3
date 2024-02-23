# ui.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Aadi Shanker
# aadidevs@uci.edu
# 75948470
# ui.py


# Import your main functions from a2 module. Adjust these imports based on your actual file structure and function names.
# ui.py


# Import your main functions from a2 module.
# Adjust these imports based on your actual file structure and function names.

from file_organizer import admin_func, load_file, create_new_file, file_search, delete_file, read_file
from pathlib import Path

def list_options():
    print("")
    print("1 - Output directory content recursively.")
    print("2 - Output only files, excluding directories in the results.")
    print("3 - Output only files that match a given file name.")
    print("4 - Output only files that match a given file extension.")


def print_menu():
    """
    Prints the main menu options to the console.
    """
    print("\nDSU File Manager")
    print("1 - Create a new DSU file")
    print("2 - Load an existing DSU file")
    print("3 - List the contents of the user specified directory.")
    print("4 - Delete File.")
    print("5 - Read the contents of a file.")
    print("6 - Edit profile.")
    print("7 - Print profile.")
    print("Q - Quit")

def handle_create():
    """
    Handles the creation of a new DSU file.
    """
    global active_file_path
    directory = input("Enter the directory path to create the DSU file: ")
    filename = input("Enter the DSU filename: ")
    active_file_path = create_new_file(directory, filename)
    #print(f"DSU file {filename} created in {directory}")

def handle_load():
    """
    Handles loading an existing DSU file.
    """
    global active_file_path
    filepath = input("Enter the path of the DSU file to load: ")
    active_file_path = load_file(filepath)
    #print(f"DSU file {filepath} loaded")

def handle_list():
    '''
    Handles listing the contetns of the user specified directory
    '''
    list_options()
    user_input = input("Enter your desired choice: ")

    if user_input == '1':
        filepath = input("Enter the directory path: ")
        directory = Path(filepath)
        file_list = file_search(directory, True)
    elif user_input == '2':
        filepath = input("Enter the directory path: ")
        directory = Path(filepath)
        file_list = file_search(directory, False, True)
    elif user_input == '3':
        filepath = input("Enter the directory path: ")
        directory = Path(filepath)

        file_name = input("Enter the given file name and extension (ex: student.txt): ")
        file_list = file_search(directory, False, False, file_name, None)
    elif user_input == '4':
        filepath = input("Enter the directory path: ")
        directory = Path(filepath)
        
        extension = input("Enter the file extension: ")
        file_list = file_search(directory, False, False, None, extension)

    for item in file_list:
        print(item)

def enter_admin_mode():
    """
    Enters the admin mode where commands are entered directly.
    """
    print("Entering admin mode. Type 'exit' to return to the main menu.")
    admin_func()

def handle_delete_file():
    user_input = input("Please enter the file path you want to remove (NOTE ONLY ABLE TO REMOVE DSU FILES): ")
    delete_file(user_input)

def handle_read():
    user_input = input("Enter the directory path with the 'dsu' file: ")
    read_file(user_input)



def ui_run():
    """
    The main loop for the user interface.
    """
    while True:
        print_menu()
        choice = input("Select an option: ").strip().lower()

        if choice == '1':
            handle_create()
        elif choice == '2':
            handle_load()
        elif choice == '3':
            handle_list()
        elif choice == '4':
            handle_delete_file()
        elif choice == '5':
            handle_read()
        elif choice.lower() == 'admin':
            enter_admin_mode()
        elif choice == 'q':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")




