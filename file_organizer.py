#file_organizer.py

# Aadi Shanker
# aadidevs@uci.edu
# 75948470

from pathlib import Path
from Profile import Profile, DsuProfileError, DsuFileError, Post
# from ds_client import send

active_file_path = None

def file_search(directory, recursive=False, files_only=False, specific_file=None, specific_ext=None):
    file_list = []
    for child in directory.iterdir():
        if child.is_dir():
            if not files_only:
                if not (specific_file or specific_ext):
                    file_list.append(child)
            if recursive:
                file_list.extend(file_search(child, recursive, files_only, specific_file, specific_ext))
        elif child.is_file():
            if specific_file:
                if child.name == specific_file:
                    file_list.append(child)
            elif specific_ext:
                if child.suffix == f'.{specific_ext}':
                    file_list.append(child)
            else:
                file_list.append(child)
    return file_list

def create_new_file(dsuserver, directory, filename):
    full_file_name = f"{filename}.dsu"
    file_path = Path(directory) / full_file_name
    truefile_path = file_path
    
    
    #prompts the user for information
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    bio = input("Enter Bio: ")
    
    #create a profile
    profile = Profile(dsuserver, username=username, password=password)
    profile.bio = bio
    #create the file
    try:
        with open(file_path, 'x') as file:
            pass
        print(file_path)
    except FileExistsError:
        profile.load_profile(file_path)
    
    #save profile
    try:
        profile.save_profile(str(file_path))
        print(f"Profile created and saved in {file_path}")
    except DsuFileError as e:
        print(f"Error saving profile: {e}")
    except FileExistsError:
        print(f"The file {full_file_name} already exists")

    return truefile_path

def load_file(path_file):
    
    path = Path(path_file)
    
    if path.exists() and path.suffix == '.dsu':
        try:
            profile = Profile()
            profile.load_profile(path_file)
            print(f"Profile loaded for user {profile.username}")
            
        except (DsuFileError, DsuProfileError) as e:
            print(f"Failed to load profile: {e}")
            # Consider whether to clear active_file_path here if loading fails
            # active_file_path = None
    else:
        print("ERROR: Invalid file path or file type")

    return path_file


def edit_profile(options):
    global active_file_path
    if not active_file_path:
        print("No active file. Please load or create a file first.")
        return
    
    try:
        profile = Profile()
        profile.load_profile(active_file_path)
        
        #implement -usr option
        if '-usr' in options:
            username_index = options.index('-usr') + 1
            if options[username_index].startswith('"') and options[username_index].endswith('"'):
                word = options[username_index][1:-1]
                profile.username = word
            else:
                profile.username = options[username_index]
        
        #implement -pwd option
        if '-pwd' in options:
            password_index = options.index('-pwd') + 1
            if options[password_index].startswith('"') and options[password_index].endswith('"'):
                word = options[password_index][1:-1]
                profile.password = word
            else:
                profile.password = options[password_index]

        #implement -bio option
        if '-bio' in options:
            index = options.index('-bio') + 1
            joinlist = " ".join(options)
            split_quote = joinlist.split('"')
            bio_index = None
            
            for index, i in enumerate(split_quote):
                if '-bio' in i:
                    bio_index = index + 1
                    break
            profile.bio = split_quote[bio_index]    

        #implement -addpost option
        if '-addpost' in options:
            index = options.index('-addpost') + 1
            joinlist = " ".join(options)
            split_quote = joinlist.split('"')
            post_index = None
            for index, i in enumerate(split_quote):
                if '-addpost' in i:
                    post_index = index + 1
                    break
            post = Post(entry=split_quote[post_index]) 
            profile.add_post(post)

        #implement -delpost option
        if '-delpost' in options:
            delpost_index = options.index('-delpost') + 1
            if delpost_index < len(options):
                post_id = int(options[delpost_index])
                profile.del_post(post_id)

        profile.save_profile(active_file_path)   # Save the profile back to the same file
        print("Profile updated successfully.")
    except (DsuFileError, DsuProfileError) as e:
        print(f"Failed to edit profile: {e}")


def print_profile_data(option, profile):
    if option == "-usr":
        print(f"Username: {profile.username}")
    
    elif option == "-pwd":
        print(f"Password: {profile.password}")
    
    elif option == "-bio":
        print(f"Bio: {profile.bio}")
    
    elif option == "-posts":
        for idx, post in enumerate(profile.get_posts()):
            print(f"Post ID {idx}: {post.entry}")
    
    elif option.startswith("-post"):
        _, post_id_str = option.split(" ")
        post_id = int(post_id_str)
        if 0 <= post_id < len(profile.get_posts()):
            print(f"Post ID {post_id}: {profile.get_posts()[post_id].entry}")
        else:
            print("Invalid Post ID")
    
    elif option == "-all":
        print(f"Username: {profile.username}")
        print(f"Password: {profile.password}")
        print(f"Bio: {profile.bio}")
        for idx, post in enumerate(profile.get_posts()):
            print(f"Post ID {idx}: {post.entry}")


def delete_file(file_path):
    # store path to variable
    path = Path(file_path)

    # ccheck if file has a .dsu suffix/extension
    if path.exists() and path.suffix == '.dsu':
        # delete file
        path.unlink()
        print(f"{file_path} DELETED")
    else:
        print('ERROR')


def read_file(file_path):
    # store path to variable
    path = Path(file_path)
    
    # check if file has a .dsu suffix/extension
    if path.exists() and path.suffix == '.dsu':
        # open and read the file
        with open(path, 'r') as file:
            contents = file.read()
            if contents:
                print(contents, end='')
            else:
                print("EMPTY")
    else:
        print("ERROR")


def admin_func():
    global active_file_path
    
    # While True so it keeps running until the user presses 'q'
    while True:
        # User input
        user_input = input("admin mode(enter q to exit):").split(" ")
        # Check if the user presses 'q' to quit
        if user_input[0].upper() == "Q":
            break

        # Check if the user presses 'l'
        elif user_input[0].upper() == 'L':
            if len(user_input) < 2:
                print("Directory path not specified")
                continue

            directory = Path(user_input[1])
            if not directory.is_dir():
                print(f"{directory} is not a valid directory")
                continue

            recursive = '-r' in user_input
            files_only = '-f' in user_input
            specific_file = None
            specific_ext = None

            if '-s' in user_input:
                try:
                    specific_file = user_input[user_input.index('-s') + 1]
                except IndexError:
                    print("Specific file name not provided after -s")
                    continue

            if '-e' in user_input:
                try:
                    specific_ext = user_input[user_input.index('-e') + 1]
                except IndexError:
                    print("Specific file extension not provided after -e")
                    continue

            results = file_search(directory, recursive, files_only, specific_file, specific_ext)
            for item in results:
                print(item)
            
        
        # Check for extension option '-c'
        elif user_input[0].upper() == 'C':
            try:

                directory = user_input[1]
                
                file_name_option = '-n' in user_input
                if file_name_option:
                    file_name_index = user_input.index('-n') + 1
                    if file_name_index < len(user_input):
                        file_name = user_input[file_name_index]
                        active_file_path = create_new_file(directory, file_name)
                    else:
                        print("File name not specified")
                else:
                    print("File name option '-n' is required")
            
            except IndexError:
                print('ERROR')

        #check for extension option 'O'
        elif user_input[0].upper() == 'O':
            if len(user_input) >= 2:
                active_file_path = load_file(user_input[1])
                # print(active_file_path)
            else:
                print("ERROR file path not specified")
        
        #check for extension option 'e'
        elif user_input[0].upper() == 'E':
            #print(active_file_path)  # Debugging print, consider removing once issue is resolved
            
            if active_file_path:  # Ensure this checks the global variable correctly
                if len(user_input) >= 2:
                    edit_profile(user_input[1:])  # Pass only the options
                    # edit_profile(list)
                else:
                    print("ERROR: No options provided for editing.")
            else:
                print("No active file selected. Please load or create a file first.")

        #Check for extension option 'P'
        elif user_input[0].upper() == 'P':
            if not active_file_path:
                print("No DSU file loaded. Please load or create a file first.")
                continue

            try:
                profile = Profile()
                profile.load_profile(active_file_path)
            except (DsuFileError, DsuProfileError) as e:
                print(f"Failed to load profile: {e}")
                continue

            # Process options for the P command
            options = ' '.join(user_input[1:]).split(' -')
            if not options:
                print("No option provided for the P command.")
                continue

            for option in options:
                if option:  # Ensure there's an actual option to process
                    option = f"-{option.strip()}" if not option.startswith('-') else option
                    print_profile_data(option, profile)
            
        # Check for extension option '-d'
        elif user_input[0].upper() == 'D':
            if len(user_input) >= 2:
                file_path = user_input[1]
                delete_file(file_path)
            else:
                print("ERROR")
        
        #  Check for extension option '-r'
        elif user_input[0].upper() == 'R':
            if len(user_input) >= 2:
                file_path = user_input[1]
                read_file(file_path)
            else:
                print("ERROR")

        else:
            print("Invalid command")


# main()
