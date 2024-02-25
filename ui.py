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

from file_organizer import admin_func, load_file, create_new_file, file_search, delete_file, read_file, active_file_path
from pathlib import Path
from ds_client import send
from Profile import Profile, Post, DsuFileError

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
    print("8 - Connect to server.")
    print("Q - Quit")


def handle_create():
    """
    Handles the creation of a new DSU file.
    """
    global active_file_path
    directory = input("Enter the directory path to create the DSU file: ")
    filename = input("Enter the DSU filename: ")
    choice = input("Would you like to connect to a server(type y or n)? ")
    
    if choice.lower() == 'y':
        server = input("Enter the desire server you would like to connect to: ")
        active_file_path = create_new_file(server, directory, filename)
    else:
        server = None
        active_file_path = create_new_file(server, directory, filename)
    
    
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


def handle_post_entry():
    if not active_file_path:
        print("No profile loaded. Please load a profile first.")
        return
    # Load the profile
    profile = Profile()
    profile.load_profile(active_file_path)

    
    if profile.dsuserver == None:
        server_input = input("Please enter your desired server id: ")
        profile.dsuserver = server_input

    print(profile.dsuserver)
    # Let the user select an entry to post or create a new entry for posting
    entry = input("Enter your journal entry to post: ")

    # Create a new Post object
    new_post = Post(entry = entry)
    # Add the new post to the profile
    profile.add_post(new_post)
    # Save the profile with the new post
    try:
        profile.save_profile(active_file_path)
        print("Entry added to your journal and ready for posting.")
    except DsuFileError as e:
        print(f"Failed to save the profile with the new entry: {e}")
        return  # Exit if unable to save the profile
    
    # Use the send function to post the entry
    send(profile.dsuserver, 3021, profile.username, profile.password, entry)


def handle_edit_profile():
    if not active_file_path:
        print("No profile loaded. Please load a profile first.")
        return
    # Load the profile
    profile = Profile()
    profile.load_profile(active_file_path)

    print("\nEdit Profile")
    print("1 - Username")
    print("2 - Password")
    print("3 - Bio")
    print("4 - DSP Server Address")
    choice = input("Select the information you want to edit: ")

    if choice == '1':
        new_username = input("Enter new username: ")
        profile.username = new_username
    elif choice == '2':
        new_password = input("Enter new password: ")
        profile.password = new_password
    elif choice == '3':
        new_bio = input("Enter new bio: ")
        profile.bio = new_bio
    elif choice == '4':
        new_server = input("Enter new DSP Server Address: ")
        profile.dsuserver = new_server
    else:
        print("Invalid choice.")
        return

    # Save the updated profile
    try:
        profile.save_profile(active_file_path)
        print("Profile updated successfully.")
    except DsuFileError as e:
        print(f"Failed to save the updated profile: {e}")


def handle_print_profile():
    if not active_file_path:
        print("No profile loaded. Please load a profile first.")
        return
    # Load the profile
    profile = Profile()
    profile.load_profile(active_file_path)

    print("\nProfile Information")
    print(f"Username: {profile.username}")
    # Consider security implications of printing the password. Maybe just indicate if it's set.
    print("Password: [HIDDEN]")
    print(f"Bio: {profile.bio}")
    print(f"DSP Server Address: {profile.dsuserver}")
    print("Posts:")
    for idx, post in enumerate(profile.get_posts()):
        print(f"{idx + 1}: {post.entry}")


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
        elif choice == '6':
            handle_edit_profile()
        elif choice == '7':
            handle_print_profile()
        elif choice == '8':
            handle_post_entry()
        elif choice.lower() == 'admin':
            enter_admin_mode()
        elif choice == 'q':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")




