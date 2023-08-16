##############################################################################
#                                 DisSav                                     #
#----------------------------------------------------------------------------#
# By            | cGull                                                      #
# Date Created  | February 24, 2023 7:37 PM (2/24/2023)                      #
# Version       | 6a                                                         #
# Source Code   | Open                                                       #
# Note          | Forked from SavePlasmaConfig                               #
##############################################################################
# This program I took inspiration from a KDE Plasma Plasmoid that kinda does #
# the same thing as this program except you can do it with any file.         #
##############################################################################
# TODO: Clean up code to open it
# ;Imports
try:
    from vars.init import *
    import pathlib
    import subprocess
except ImportError as IE:
    print(f"IMPORT ERROR: {IE}")
# ;Vars
operating_system_info = sysDetect(getMoreInfo=True, quiet=True)
version_main = "DisSav 6"
# ;Code

def run(file=f"{GF_FILE_PATH}/Plasma.txt", **ro):
    """
#############################################################################
#                               Main Function                               #
#---------------------------------------------------------------------------#
# Copies files/folders (if found) listed above (lookfor) and puts them in a #
# folder called 'Bakup' and within that folder is another folder called by  #
# whatever name the user gives it (Linux only)                              #
#############################################################################
    :param name:
    :param ro:
    """
    # GLOBALS
    global ro_verbose_mode
    # RO
    verbose_mode = ro.get("verbose_mode", False)
    ro_test_mode = ro.get("testmode", False)
    ro_no_copy_icons = ro.get("no_copy_icons", False)
    ro_include_installed_packages = ro.get("include_packages", False)
    ro_use_plasma_apptitle = ro.get("use_apptitle", False) # ; If True Name gets the value from the keyword args but eventually overrides it before the main process begins
    ro_use_plasma_apptitle_plasma_panel = ro.get("use_plasma_panel", False) # ; Go with _/
    comment_char = ro.get("void", "{") # ;A comment character (like python's #) that will allow step 1 to skip line if ever used
    ro_take_screenshot = ro.get("screenshot", False)  # ; Need SPECTACLE for this
    # RO_COMPAT
    name = ro.get("name", "")
    # BOOL
    tab_length_found = False
    # INT
    tab_length = 0
    # STR
    start_date = f"{datetime.now().strftime('%Y-%m-%d %I:%M %p')}"
    tab_length_string = f""
    output = ""
    # DICT
    references = {} # ;Lookfor allows this program to look through the user's config directory
    # LIST
    functions = ["F()", "W()", "L()", "S()", "I()"]
    # NONE
    firefox_browser_profile = None
    librewolf_browser_profile = None
    # CODE
    # ;Setting up
    ro_verbose_mode = verbose_mode # ;Tell init.py file that the keyword argument is True so that the functions inside it that use 'ro_verbose_mode' can refer to the value that's ran in the cmdline.py
    filtered_line_counter = 0
    # ;Step 1: Filter the data by removing custom made tabs that python3 (as of 3.8) not detecting tabs so that it would be easier to read later (this also filters out comments)
    p(f"Step 1 Started\t<{datetime.now().strftime('%Y-%m-%d %I:%M %p')}>\n")
    with open(file, "r") as preper_file:
        opened_file = preper_file.read().split("\n")
        opened_file_removed_tabs = []
        for line in opened_file:
            if not line.__contains__(comment_char): # ;Comment
                if not line == "": # ;Filter out empty lines
                    if line[0].isspace() and tab_length_found is False: # ;Tab detection and spaces, ran only once since the text file should only have more than one tab made per line
                        while line[tab_length].isspace():
                            tab_length += 1
                            tab_length_string += " "
                        tab_length_found = True
                    if line.__contains__(tab_length_string) and tab_length_found:
                        p(line[tab_length:], cond=verbose_mode)
                        opened_file_removed_tabs.append(line[tab_length:])
                    else:
                        p(line, cond=verbose_mode)
                        opened_file_removed_tabs.append(line)
    # ;Step 2: Use that filtered list to give the necessary information to 'references' to even better the 'lookfor' dictionary in my personal version yet infieror version my cmdline program called 'SavePlasmaConfig'
    p(f"Step 2 Started\t<{datetime.now().strftime('%Y-%m-%d %I:%M %p')}>\n")
    for declaration in opened_file_removed_tabs:
        filtered_line_counter += 1
        if declaration.__contains__("!"):
            reference_name = declaration[:len(declaration)-1]
            references.update(
                {declaration[:len(declaration)-1]: {
                    "folders": {
                        "root": {},
                        "user": {},
                    },
                    "files": {
                        "root": {},
                        "user": {},
                    },
                }
            })
        elif declaration.__contains__("="):
            # ;Var and Values
            declaration_split = declaration.split("=")
            if declaration.__contains__("|"):
                declaration_custom_list = declaration_split[1].split(" | ")
                destination_taop = declaration_custom_list[1]
                # ;Path
                destination_str = declaration_custom_list[0]
                destination = destination_str[1:len(destination_str) - 1]
                destination_function_detected = False
                for function in functions:
                    if destination.__contains__(function):
                        destination_function_detected = True
                # ;Tags
                tag_list_str = ""
                for destination_taop_chars in destination_taop:  # ;Filter out these characters so that python can accurately convert the string to list
                    if destination_taop_chars == "[":
                        pass
                    elif destination_taop_chars != "]":
                        tag_list_str += destination_taop_chars
                    else:
                        break
                tag_list = tag_list_str.split(",")
                p(tag_list_str, cond=verbose_mode)
                for tag in tag_list:
                    if tag[0].isspace():  # ;Detect if the looped index's first character is a space, if so leave it out of the picture, otherwise ignore it
                        tag_list[tag_list.index(tag)] = tag[1:]
                        # ;Options
                        options = destination_taop[destination_taop.index("?"):]
                        requires_root = False
                        is_folder = False
                        for option_index in options:
                            for option in option_index:
                                if option == ";":
                                    requires_root = True
                                if option == ":":
                                    is_folder = True
                if destination[0] == "$":
                    destination = destination.replace("$", os.environ["HOME"])
                    if destination[len(os.environ["HOME"]) + 1] != "/":
                        destination = insert_string(destination, len(os.environ["HOME"]), "/")
                if requires_root:
                    if is_folder:
                        references[reference_name]["folders"]["root"].update({declaration_split[0]: {"destination": destination, "tags": tag_list, "flags": options, "isPresent": getPresSpec(destination), "hasFunction": destination_function_detected}})
                    else:
                        references[reference_name]["files"]["root"].update({declaration_split[0]: {"destination": destination, "tags": tag_list, "flags": options, "isPresent": getPresSpec(destination), "hasFunction": destination_function_detected}})
                else:
                    if is_folder:
                        references[reference_name]["folders"]["user"].update({declaration_split[0]: {"destination": destination, "tags": tag_list, "flags": options, "isPresent": getPresSpec(destination), "hasFunction": destination_function_detected}})
                    else:
                        references[reference_name]["files"]["user"].update({declaration_split[0]: {"destination": destination, "tags": tag_list, "flags": options, "isPresent": getPresSpec(destination), "hasFunction": destination_function_detected}})
            else:
                declaration_custom_list = declaration_split[1].split("?")
                # ;Tags
                requires_root = False
                is_folder = False
                for tag in declaration_custom_list[1]:
                    if tag == ";":
                        requires_root = True
                    if tag == ":":
                        is_folder = True
                # ;Destination
                destination_str = declaration_custom_list[0]
                destination = destination_str[1:len(destination_str) - 1]
                destination_function_detected = False
                for function in functions:
                    if destination.__contains__(function):
                        destination_function_detected = True
                if destination[0] == "$":
                    destination = destination.replace("$", os.environ["HOME"])
                    if destination[len(os.environ["HOME"]) + 1] != "/":
                        destination = insert_string(destination, len(os.environ["HOME"]), "/")
                if requires_root:
                    if is_folder:
                        references[reference_name]["folders"]["root"].update({declaration_split[0]: {"destination": destination, "tags": None, "flags": declaration_custom_list[1], "isPresent": getPresSpec(destination), "hasFunction": destination_function_detected}})
                    else:
                        references[reference_name]["files"]["root"].update({declaration_split[0]: {"destination": destination, "tags": None, "flags": declaration_custom_list[1], "isPresent": getPresSpec(destination), "hasFunction": destination_function_detected}})
                else:
                    if is_folder:
                        references[reference_name]["folders"]["user"].update({declaration_split[0]: {"destination": destination, "tags": None, "flags": declaration_custom_list[1], "isPresent": getPresSpec(destination), "hasFunction": destination_function_detected}})
                    else:
                        references[reference_name]["files"]["user"].update({declaration_split[0]: {"destination": destination, "tags": None, "flags": declaration_custom_list[1], "isPresent": getPresSpec(destination), "hasFunction": destination_function_detected}})
    # ; Debug
    if verbose_mode:
        for reference in references:
            p(reference)
            for type_data in references[reference]:
                p(f"\t{type_data}")
                for user_type in references[reference][type_data]:
                    p(f"\t\t{user_type}")
                    for var_name in references[reference][type_data][user_type]:
                        p(f"\t\t\t{var_name}")
                        for values in references[reference][type_data][user_type][var_name]:
                            p(f"\t\t\t\t{values}: {references[reference][type_data][user_type][var_name][values]}")

    # Step 3: Copy
    p(f"\nStep 3 Started\t<{datetime.now().strftime('%Y-%m-%d %I:%M %p')}>\n")
    p(operating_system_info)
    if ro_test_mode or operating_system_info["system"] != "Linux":
        if operating_system_info["system"] != "Linux":
            makeBox(f"Operating System must be 'Linux' or simply a Linux Distro")
            p(f"Reason: operating_system_info['system'] = {operating_system_info['system']}")
        pass
    else:
        if ro_use_plasma_apptitle:
            app_title = grab_application_title_text(plasma_panel=ro_use_plasma_apptitle_plasma_panel)
            if app_title[0] is None:
                name = str(tt).translate(str(tt).maketrans(":", "_"))
            elif app_title[0] == "":
                name = str(tt).translate(str(tt).maketrans(":", "_"))
            elif app_title[1] is True:
                if app_title[0] in ["", None]:
                    name = str(tt).translate(str(tt).maketrans(":", "_"))
                else:
                    name = app_title[0]
        elif name == "":
            name = "test_save"
        for bakup in os.walk(f"{homepath}/Bakup").__next__()[1]:
            if bakup == name:
                overwrite_warning = input("Overwrite?\n\nChoices\n----------------\ny = yes\n\nAnything else will cancel overwriting which will exit the program\n\nChoice: ")
                if overwrite_warning in ["Y", "y"]:
                    pass
                else:
                    exit(0)
        getPresSpec(f"{homepath}/Bakup/{name}/", create_folder=True)
        target_path = f"{homepath}Bakup/{name}"
        is_sudo_access_granted = False
        output += f"[Info]" \
                  f"\nName={name}" \
                  f"\nSavedBy={gp.getuser()}" \
                  f"\nSaveStartDate={start_date}" \
                  f"\nSaveEndDate=\n" \
                  f"[Info/Specs]" \
                  f"\nArchitecture={operating_system_info['machine']}" \
                  f"\nCPU={operating_system_info['cpu']}" \
                  f"\nSystem={operating_system_info['system']}\n"
        path_filter = []
        for section in references:
            output += f"\n[{section}]"
            for _type in references[section]:
                for perm_type in references[section][_type]:
                    for data_title in references[section][_type][perm_type]:
                        properties = references[section][_type][perm_type][data_title]
                        if _type == "folders":
                            path = references[section][_type][perm_type][data_title]["destination"]
                            destination = target_path + path.replace(gp.getuser(), "USER")
                            hasFunction = references[section][_type][perm_type][data_title]["hasFunction"]
                            flags = references[section][_type][perm_type][data_title]["flags"]
                            tags = references[section][_type][perm_type][data_title]["tags"]
                            if hasFunction is False:
                                path = str(pathlib.Path(path).resolve())
                            if getPresSpec(path):
                                for function in functions:
                                    if not path.__contains__(function):
                                        if path not in path_filter:
                                            path_filter.append(path)
                                            if destination[-1] == "/":
                                                getPresSpec(destination[:index(destination, "/")[-2]], create_folder=True)
                                            else:
                                                getPresSpec(destination[:index(destination, "/")[-1]], create_folder=True)
                                            if flags is not None:
                                                if flags.__contains__(";") and is_sudo_access_granted is False:
                                                    p("Requiring root access")
                                                    if verbose_mode:
                                                        subprocess.run(["sudo", "cp", "-RT", path, destination, "-v"])
                                                    else:
                                                        subprocess.run(["sudo", "cp", "-RT", path, destination])
                                                    is_sudo_access_granted = True
                                                elif flags.__contains__(";"):
                                                    if verbose_mode:
                                                        subprocess.run(["sudo", "cp", "-RT", path, destination, "-v"])
                                                    else:
                                                        subprocess.run(["sudo", "cp", "-RT", path, destination])
                                                elif verbose_mode:
                                                    subprocess.run(["cp", "-r", path, destination, "-v"])
                                                else:
                                                    subprocess.run(["cp", "-r", path, destination])
                                                tags_output = get_tags(tags)
                                                output += "\n" + data_title + "=" + path + " --> " + destination + tags_output
                                            break
                        elif _type == "files":
                            path = references[section][_type][perm_type][data_title]["destination"]
                            destination = target_path + path.replace(gp.getuser(), "USER")
                            hasFunction = references[section][_type][perm_type][data_title]["hasFunction"]
                            flags = references[section][_type][perm_type][data_title]["flags"]
                            tags = references[section][_type][perm_type][data_title]["tags"]
                            tags_output = ""
                            if hasFunction is False:
                                path = str(pathlib.Path(path).resolve())
                            if getPresSpec(path):
                                for function in ["F()", "W()", "L()", "S()"]:
                                    if not path.__contains__(function):
                                        if path not in path_filter:
                                            path_filter.append(path)
                                            if destination[-1] == "/":
                                                getPresSpec(destination[:index(destination, "/")[-2]], create_folder=True)
                                            else:
                                                getPresSpec(destination[:index(destination, "/")[-1]], create_folder=True)
                                            if flags is not None:
                                                if flags.__contains__(";") and is_sudo_access_granted is False:
                                                    p("Requiring root access")
                                                    if verbose_mode:
                                                        subprocess.run(["sudo", "cp", path, destination, "-v"])
                                                    else:
                                                        subprocess.run(["sudo", "cp", path, destination])
                                                    is_sudo_access_granted = True
                                                elif flags.__contains__(";"):
                                                    if verbose_mode:
                                                        subprocess.run(["sudo", "cp", path, destination, "-v"])
                                                    else:
                                                        subprocess.run(["sudo", "cp", path, destination])
                                                elif verbose_mode:
                                                    subprocess.run(["cp", path, destination, "-v"])
                                                else:
                                                    subprocess.run(["cp", path, destination])
                                                tags_output = get_tags(tags)
                                                if destination[-1] == "/":
                                                    output += f"\n{data_title} = {path} --> {destination[:index(destination, '/')[-2]]}{tags_output}"
                                                else:
                                                    output += f"\n{data_title} = {path} --> {destination[:index(destination, '/')[-1]]}{tags_output}"
                                            break

                        if destination.__contains__("W()"):
                            getPresSpec(target_path+"/"+"Wallpapers/KDE/", create_folder=True)
                            getPresSpec(target_path+"/"+"Wallpapers/Defaults/WindowMaker/", create_folder=True)
                            output += "\n[Wallpapers/Plasma]"
                            # ;Tag Gen
                            tags_output = get_tags(tags)
                            # ;KDE Plasma 5
                            for wallpaper in get_plasma_wallpapers():
                                if getPresSpec(wallpaper):
                                    filename = wallpaper.split("/")[-1].split(".")[0]
                                    if verbose_mode:
                                        subprocess.run(["cp", wallpaper, f"{target_path}/Wallpapers/KDE/", "-v"])
                                    else:
                                        subprocess.run(["cp", wallpaper, f"{target_path}/Wallpapers/KDE/"])
                                    output += f"\n{filename}={wallpaper} --> {target_path}/Wallpapers/KDE/ {tags_output}"
                            # ; Local Wallpapers
                            if getPresSpec(f"{os.environ['HOME']}/.local/share/wallpapers"):
                                local_wallpapers = os.walk(f"{os.environ['HOME']}/.local/share/wallpapers").__next__()
                                local_wallpapers_path = local_wallpapers[0]
                                local_wallpapers_folders = local_wallpapers[1]
                                local_wallpapers_files = local_wallpapers[2]
                                for _file in local_wallpapers_files:
                                    filename = _file.split("/")[-1].split(".")[0]
                                    output += f"\n{filename}={local_wallpapers_path}/{_file} --> {target_path}/Wallpapers/KDE/{_file} {tags_output}"
                                    if verbose_mode:
                                        subprocess.run(["cp", local_wallpapers_path + "/" + _file, f"{target_path}/Wallpapers/KDE/{_file}", "-v"])
                                    else:
                                        subprocess.run(["cp", local_wallpapers_path+"/"+_file, f"{target_path}/Wallpapers/KDE/{_file}"])
                                output += "\n[Wallpapers/Plasma/Folders]"
                                for folder in local_wallpapers_folders:
                                    output += f"\n{folder}={local_wallpapers_path}/{folder} --> {target_path}/Wallpapers/KDE/{folder} {tags_output}"
                                    if verbose_mode:
                                        subprocess.run(["cp", "-r", local_wallpapers_path + "/" + folder, f"{target_path}/Wallpapers/KDE/", "-v"])
                                    else:
                                        subprocess.run(["cp", "-r", local_wallpapers_path+"/"+folder, f"{target_path}/Wallpapers/KDE/"])
                            # ;Other
                            if getPresSpec("/usr/share/wallpapers/"):
                                root_wallpapers = os.walk("/usr/share/wallpapers/").__next__()
                                root_wallpapers_path = root_wallpapers[0]
                                root_wallpapers_folders = root_wallpapers[1]
                                root_wallpapers_files = root_wallpapers[2]
                                for _file in root_wallpapers_files:
                                    filename = _file.split("/")[-1].split(".")[0]
                                    output += f"\n{filename}={str(pathlib.Path(f'{root_wallpapers_path}/{_file}').resolve())} --> {target_path}/Wallpapers/Defaults/{_file} <wallpaper> <distro>"
                                    if verbose_mode:
                                        subprocess.run(["cp", str(pathlib.Path(f"{root_wallpapers_path}/{_file}").resolve()), f"{target_path}/Wallpapers/Defaults/{_file}", "-v"])
                                    else:
                                        subprocess.run(["cp", str(pathlib.Path(f"{root_wallpapers_path}/{_file}").resolve()), f"{target_path}/Wallpapers/Defaults/{_file}"])
                                for folder in root_wallpapers_folders:
                                    output += f"\n{folder}={str(pathlib.Path(f'{root_wallpapers_path}/{folder}').resolve())} --> {target_path}/Wallpapers/Defaults/{folder} <wallpaper> <distro>"
                                    if verbose_mode:
                                        subprocess.run(["cp", "-r", str(pathlib.Path(f"{root_wallpapers_path}/{folder}").resolve()), f"{target_path}/Wallpapers/Defaults/", "-v"])
                                    else:
                                        subprocess.run(["cp", "-r", str(pathlib.Path(f"{root_wallpapers_path}/{folder}").resolve()), f"{target_path}/Wallpapers/Defaults/"])
                            # ;Window Maker/Open Step/GNUStep
                            if getPresSpec("/usr/share/WindowMaker/Backgrounds/"):
                                root_window_maker_wallpapers = os.walk("/usr/share/WindowMaker/Backgrounds/").__next__()
                                root_window_maker_wallpapers_path = root_window_maker_wallpapers[0]
                                root_window_maker_wallpapers_folders = root_window_maker_wallpapers[1]
                                root_window_maker_wallpapers_files = root_window_maker_wallpapers[2]
                                for _file in root_window_maker_wallpapers_files:
                                    filename = _file.split("/")[-1].split(".")[0]
                                    output += f"\n{filename}={str(pathlib.Path(f'{root_window_maker_wallpapers_path}/{_file}').resolve())} --> {target_path}/Wallpapers/Defaults/WindowMaker/{_file} <wallpaper> <WindowMaker>"
                                    if verbose_mode:
                                        subprocess.run(["cp", str(pathlib.Path(f"{root_window_maker_wallpapers_path}/{_file}").resolve()), f"{target_path}/Wallpapers/Defaults/WindowMaker/", "-v"])
                                    else:
                                        subprocess.run(["cp", str(pathlib.Path(f"{root_window_maker_wallpapers_path}/{_file}").resolve()), f"{target_path}/Wallpapers/Defaults/WindowMaker/"])
                                for folder in root_window_maker_wallpapers_folders:
                                    output += f"\n{folder}={str(pathlib.Path(f'{root_window_maker_wallpapers_path}/{folder}').resolve())} --> {target_path}/Wallpapers/Defaults/WindowMaker/{folder} <wallpaper> <WindowMaker>"
                                    if verbose_mode:
                                        subprocess.run(["cp", "-r", str(pathlib.Path(f"{root_window_maker_wallpapers_path}/{folder}").resolve()), f"{target_path}/Wallpapers/Defaults/WindowMaker"])
                                    else:
                                        subprocess.run(["cp", "-r", str(pathlib.Path(f"{root_window_maker_wallpapers_path}/{folder}").resolve()), f"{target_path}/Wallpapers/Defaults/WindowMaker"])

                        if destination.__contains__("F()"):
                            if firefox_browser_profile is None:
                                firefox_profile = ".mozilla/firefox/"+get_current_firefox_profile()
                                firefox_browser_profile = firefox_profile
                                path = path.replace("F()", firefox_profile)
                            else:
                                path = path.replace("F()", firefox_browser_profile)
                            destination = destination.replace("F()", ".mozilla/firefox/Add to profile")
                            if getPresSpec(path):
                                getPresSpec(destination, create_folder=True)
                                tags_output = get_tags(tags)
                                output += f"\n{data_title}={path} --> {destination}{tags_output}"
                                if verbose_mode:
                                    subprocess.run(["cp", "-RT", path, destination, "-v"])
                                else:
                                    subprocess.run(["cp", "-RT", path, destination])

                        if destination.__contains__("L()"): # ;Librewolf
                            if librewolf_browser_profile is None:
                                librewolf_profile = f".librewolf/{get_current_librewolf_profile()}"
                                librewolf_browser_profile = librewolf_profile
                                path = path.replace("L()", librewolf_profile)
                            else:
                                path = path.replace("L()", librewolf_browser_profile)
                            destination = destination.replace("L()", ".librewolf/Add to profile")
                            if getPresSpec(path):
                                getPresSpec(destination, create_folder=True)
                                tags_output = get_tags(tags)
                                output += f"\n{data_title}={path} --> {destination}{tags_output}"
                                if verbose_mode:
                                    subprocess.run(["cp", "-RT", path, destination, "-v"])
                                else:
                                    subprocess.run(["cp", "-RT", path, destination])

                        if destination.__contains__("S()"): # ;Get System Sounds (currently used ones)
                            plasma_sounds_list_targets = get_current_plasma_sounds()
                            plasma_sounds_list_destinations = plasma_sounds_list_targets.copy()
                            plasma_sounds_list_destination_target = destination.replace("S()", "")+"Sounds/"
                            getPresSpec(plasma_sounds_list_destination_target, create_folder=True)
                            tags_output = get_tags(tags)
                            for sound_index in range(len(plasma_sounds_list_destinations)):
                                plasma_sounds_list_destinations[sound_index] = plasma_sounds_list_destinations[sound_index].replace(gp.getuser(), "USER")
                                plasma_sounds_list_destinations[sound_index] = plasma_sounds_list_destination_target+plasma_sounds_list_destinations[sound_index].split("/")[-1]
                            output += "\n[Sounds]"
                            for sound in range(len(plasma_sounds_list_targets)):
                                p_sfx_target = plasma_sounds_list_targets[sound]
                                p_sfx_destination = plasma_sounds_list_destinations[sound]
                                filename = p_sfx_destination.split("/")[-1].split(".")[0]
                                output += f"\n{filename}={p_sfx_target} --> {p_sfx_destination}{tags_output}"
                                if verbose_mode:
                                    subprocess.run(["cp", p_sfx_target, p_sfx_destination, "-v"])
                                else:
                                    subprocess.run(["cp", p_sfx_target, p_sfx_destination])

                        if destination.__contains__("I()"):
                            # ;f"{homepath}.local/share/icons", "/usr/share/icons", "/usr/share/WindowMaker/"
                            local_icons = os.walk(f"{homepath}.local/share/icons").__next__()
                            local_icons_path = local_icons[0]
                            local_icons_folders = local_icons[1]
                            local_icons_files = local_icons[2]

                            root_icons = os.walk("/usr/share/icons").__next__()
                            root_icons_path = root_icons[0]
                            root_icons_folders = root_icons[1]
                            root_icons_files = root_icons[2]

                            root_window_maker = os.walk("/usr/share/WindowMaker/").__next__()
                            root_window_maker_path = root_window_maker[0]
                            root_window_maker_folders = [
                                root_window_maker[1][4],
                                root_window_maker[1][3],
                                root_window_maker[1][2]
                            ]
                            tags_output = get_tags(tags)
                            if ro_no_copy_icons is False:
                                if getPresSpec(local_icons_path):
                                    destination = f"{target_path}{str(pathlib.Path(f'{local_icons_path}').resolve()).replace(gp.getuser(), 'USER')}"
                                    getPresSpec(destination, create_folder=True)
                                    output += "\n[UserIcons]"
                                    for _file in local_icons_files:
                                        filename = _file.split("/")[-1].split(".")[0]
                                        target = str(pathlib.Path(f'{local_icons_path}/{_file}').resolve())
                                        output += f"\n{filename}={target} --> {destination}/{_file} {tags_output} <User>"
                                        if verbose_mode:
                                            subprocess.run(["cp", target, destination, "-v"])
                                        else:
                                            subprocess.run(["cp", target, destination])
                                    for folder in local_icons_folders:
                                        target = f"{str(pathlib.Path(f'{local_icons_path}/{folder}').resolve())}"
                                        output += f"\n{folder}={target} --> {destination} {tags_output} <User>"
                                        if verbose_mode:
                                            subprocess.run(["cp", "-r", f"{pathlib.Path(f'{local_icons_path}/{folder}').resolve()}", destination, "-v"])
                                        else:
                                            subprocess.run(["cp", "-r", f"{pathlib.Path(f'{local_icons_path}/{folder}').resolve()}", destination])
                                if getPresSpec(root_icons_path):
                                    destination = f"{target_path}{str(pathlib.Path(f'{root_icons_path}').resolve())}"
                                    getPresSpec(destination, create_folder=True)
                                    output += "\n[RootIcons]"
                                    for _file in root_icons_files:
                                        filename = _file.split("/")[-1].split(".")[0]
                                        target = str(pathlib.Path(f'{root_icons_path}/{_file}').resolve())
                                        output += f"\n{filename}={target} --> {destination}/{_file} {tags_output} <Root>"
                                        if is_sudo_access_granted:
                                            if verbose_mode:
                                                subprocess.run(["sudo", "cp", target, destination, "-v"])
                                            else:
                                                subprocess.run(["sudo", "cp", target, destination])
                                        else:
                                            p("Requiring root access")
                                            if verbose_mode:
                                                subprocess.run(["sudo", "cp", target, destination, "-v"])
                                            else:
                                                subprocess.run(["sudo", "cp", target, destination])
                                    for folder in root_icons_folders:
                                        target = str(pathlib.Path(f'{root_icons_path}/{folder}').resolve())
                                        output += f"\n{folder}={target} --> {destination}/{_file} {tags_output} <Root>"
                                        if is_sudo_access_granted:
                                            if verbose_mode:
                                                subprocess.run(["sudo", "cp", "-r", target, destination, "-v"])
                                            else:
                                                subprocess.run(["sudo", "cp", "-r", target, destination])
                                        else:
                                            p("Requiring root access")
                                            if verbose_mode:
                                                subprocess.run(["sudo", "cp", "-r", target, destination, "-v"])
                                            else:
                                                subprocess.run(["sudo", "cp", "-r", target, destination])
                                if getPresSpec(root_window_maker_path):
                                    destination = f"{target_path}{str(pathlib.Path(f'{root_window_maker_path}').resolve())}"
                                    getPresSpec(destination, create_folder=True)
                                    output += "\n[WindowMakerIcons]"
                                    for folder in root_window_maker_folders:
                                        target = str(pathlib.Path(f'{root_window_maker_path}/{folder}').resolve())
                                        output += f"\n{folder}={target} --> {destination} {tags_output} <Root> <WindowMaker>"
                                        if is_sudo_access_granted:
                                            if verbose_mode:
                                                subprocess.run(["sudo", "cp", "-r", target, destination, "-v"])
                                            else:
                                                subprocess.run(["sudo", "cp", "-r", target, destination])
                                        else:
                                            p("Requiring root access")
                                            if verbose_mode:
                                                subprocess.run(["sudo", "cp", "-r", target, destination, "-v"])
                                            else:
                                                subprocess.run(["sudo", "cp", "-r", target, destination])
                            else:
                                if getPresSpec(local_icons_path):
                                    destination = f"{target_path}{str(pathlib.Path(f'{local_icons_path}').resolve()).replace(gp.getuser(), 'USER')}"
                                    getPresSpec(destination, create_folder=True)
                                    output += "\n[UserIcons]"
                                    for _file in local_icons_files:
                                        filename = _file.split("/")[-1].split(".")[0]
                                        target = str(pathlib.Path(f'{local_icons_path}/{_file}').resolve())
                                        output += f"\n{filename}={target} --> {destination}/{_file} {tags_output} <User> <Linked>"
                                        if verbose_mode:
                                            subprocess.run(["ln", "-s", target, destination, "-v"])
                                        else:
                                            subprocess.run(["ln", "-s", target, destination])
                                    for folder in local_icons_folders:
                                        target = f"{str(pathlib.Path(f'{local_icons_path}/{folder}').resolve())}"
                                        output += f"\n{folder}={target} --> {destination} {tags_output} <User> <Linked>"
                                        if verbose_mode:
                                            subprocess.run(["ln", "-s", f"{pathlib.Path(f'{local_icons_path}/{folder}').resolve()}", destination, "-v"])
                                        else:
                                            subprocess.run(["ln", "-s", f"{pathlib.Path(f'{local_icons_path}/{folder}').resolve()}", destination])
                                if getPresSpec(root_icons_path):
                                    destination = f"{target_path}{str(pathlib.Path(f'{root_icons_path}').resolve())}"
                                    getPresSpec(destination, create_folder=True)
                                    output += "\n[RootIcons]"
                                    for _file in root_icons_files:
                                        filename = _file.split("/")[-1].split(".")[0]
                                        target = str(pathlib.Path(f'{root_icons_path}/{_file}').resolve())
                                        output += f"\n{filename}={target} --> {destination}/{_file} {tags_output} <Root> <Linked>"
                                        if is_sudo_access_granted:
                                            if verbose_mode:
                                                subprocess.run(["sudo", "ln", "-s", target, destination, "-v"])
                                            else:
                                                subprocess.run(["sudo", "ln", "-s", target, destination])
                                        else:
                                            p("Requiring root access")
                                            if verbose_mode:
                                                subprocess.run(["sudo", "ln", "-s", target, destination, "-v"])
                                            else:
                                                subprocess.run(["sudo", "ln", "-s", target, destination])
                                    for folder in root_icons_folders:
                                        target = str(pathlib.Path(f'{root_icons_path}/{folder}').resolve())
                                        output += f"\n{folder}={target} --> {destination}/{_file} {tags_output} <Root>"
                                        if is_sudo_access_granted:
                                            if verbose_mode:
                                                subprocess.run(["sudo", "ln", "-s", target, destination, "-v"])
                                            else:
                                                subprocess.run(["sudo", "ln", "-s", target, destination])
                                        else:
                                            p("Requiring root access")
                                            if verbose_mode:
                                                subprocess.run(["sudo", "ln", "-s", target, destination, "-v"])
                                            else:
                                                subprocess.run(["sudo", "ln", "-s", target, destination])
                                if getPresSpec(root_window_maker_path):
                                    destination = f"{target_path}{str(pathlib.Path(f'{root_window_maker_path}').resolve())}"
                                    getPresSpec(destination, create_folder=True)
                                    output += "\n[WindowMakerIcons]"
                                    for folder in root_window_maker_folders:
                                        target = str(pathlib.Path(f'{root_window_maker_path}/{folder}').resolve())
                                        output += f"\n{folder}={target} --> {destination} {tags_output} <Root> <WindowMaker> <Linked>"
                                        if is_sudo_access_granted:
                                            if verbose_mode:
                                                subprocess.run(["sudo", "ln", "-s", target, destination, "-v"])
                                            else:
                                                subprocess.run(["sudo", "ln", "-s", target, destination])
                                        else:
                                            p("Requiring root access")
                                            if verbose_mode:
                                                subprocess.run(["sudo", "ln", "-s", target, destination, "-v"])
                                            else:
                                                subprocess.run(["sudo", "ln", "-s", target, destination])

        if ro_include_installed_packages:
            output += f"\n\n-Packages({operating_system_info['distro']})-"
            if operating_system_info['distro'].__contains__("Debian"):
                apt_packages = subprocess.run(["sudo", "apt", "list", "--installed"], capture_output=True, universal_newlines="\n").stdout.split("\n")
                apt_packages.pop(0)
                output += "\nAPT"
                for package in apt_packages:
                    output += f"\n\t{package}"
                if len(subprocess.run(["pip", "list"], capture_output=True, universal_newlines="\n").stdout.split(pip_list_len())) > 0:
                    pip_packages = subprocess.run(["pip", "list"], capture_output=True, universal_newlines="\n").stdout.split(pip_list_len())[1]
                    pip_packages = pip_packages.split("\n")
                    if pip_packages[0] == '':
                        pip_packages.pop(0)
                    if len(pip_packages) > 0:
                        output += "\nPIP"
                        for package in pip_packages:
                            output += f"\n\t{package}"
                if homebrew_installed():
                    homebrew_packages = subprocess.run(["brew", "list", "-1", "--full-name"], capture_output=True, universal_newlines="\n").stdout.split("\n")
                    if len(homebrew_packages) > 0:
                        output += "\nHomebrew"
                        for package in homebrew_packages:
                            output += f"\n\t{package}"
                    else:
                        p("and yet no brew packages have been installed")
                if flatpak_installed():
                    flatpak_packages = subprocess.run(["flatpak", "list"], capture_output=True, universal_newlines="\n").stdout.split("\n")
                    if flatpak_packages[-1] == "":
                        flatpak_packages.pop(-1)
                    if len(flatpak_packages) > 0:
                        output += "\nFlatpak"
                        for package in flatpak_packages:
                            flat_package = package.split("\t")
                            if len(flat_package) >= 0:
                                flat_package_info = {
                                    "name": flat_package[0],
                                    "app_id": flat_package[1],
                                    "version": flat_package[2],
                                    "branch": flat_package[3],
                                    "installation": flat_package[4]
                                }
                                for info in flat_package_info:
                                    if info == "name":
                                        output += f"\n\t{flat_package_info[info]}"
                                    elif flat_package_info[info] == "":
                                        output += f"\n\t\t{info}: None"
                                    else:
                                        output += f"\n\t\t{info}: {flat_package_info[info]}"
                    else:
                        p("and yet there's no packages installed for Flatpak")

            elif operating_system_info['distro'].__contains__("arch"):
                packages = subprocess.run(["sudo", "pacman", "-Qq"], capture_output=True, universal_newlines="\n").stdout.split("\n")
                for package in packages:
                    output += f"\n{package}"
                if len(subprocess.run(["pip", "list"], capture_output=True, universal_newlines="\n").stdout.split(pip_list_len())) > 0:
                    pip_packages = subprocess.run(["pip", "list"], capture_output=True, universal_newlines="\n").stdout.split(pip_list_len())[1]
                    pip_packages = pip_packages.split("\n")
                    if pip_packages[0] == '':
                        pip_packages.pop(0)
                    if len(pip_packages) > 0:
                        output += "\nPIP"
                        for package in pip_packages:
                            output += f"\n\t{package}"
                if homebrew_installed():
                    homebrew_packages = subprocess.run(["brew", "list", "-1", "--full-name"], capture_output=True, universal_newlines="\n").stdout.split("\n")
                    if len(homebrew_packages) > 0:
                        output += "\nHomebrew"
                        for package in homebrew_packages:
                            output += f"\n\t{package}"
                    else:
                        p("and yet no brew packages have been installed")
                if flatpak_installed():
                    flatpak_packages = subprocess.run(["flatpak", "list"], capture_output=True, universal_newlines="\n").stdout.split("\n")
                    if flatpak_packages[-1] == "":
                        flatpak_packages.pop(-1)
                    if len(flatpak_packages) > 0:
                        output += "\nFlatpak"
                        for package in flatpak_packages:
                            flat_package = package.split("\t")
                            if len(flat_package) >= 0:
                                flat_package_info = {
                                    "name": flat_package[0],
                                    "app_id": flat_package[1],
                                    "version": flat_package[2],
                                    "branch": flat_package[3],
                                    "installation": flat_package[4]
                                }
                                for info in flat_package_info:
                                    if info == "name":
                                        output += f"\n\t{flat_package_info[info]}"
                                    elif flat_package_info[info] == "":
                                        output += f"\n\t\t{info}: None"
                                    else:
                                        output += f"\n\t\t{info}: {flat_package_info[info]}"
                    else:
                        p("Yet there's no packages installed for FlatPak")

        if ro_take_screenshot:
            makeBox("Taking Screenshot, You'll be notified")
            subprocess.run(["spectacle", "-f", "-b", "-o", f"{homepath}Bakup/{name}/{name}.png"])

        output = output.replace("SaveEndDate=", f"SaveEndDate={datetime.now().strftime('%Y-%m-%d %I:%M %p')}")
        p(f"\nStep 4 Started\t<{datetime.now().strftime('%Y-%m-%d %I:%M %p')}>\n")
        with open(f"{homepath}/Bakup/{name}/Save_info.txt", "w+") as save_output:
            save_output.write(output)
        p(f"\nFinished {name} at {datetime.now().strftime('%Y-%m-%d %I:%M %p')} in {homepath}Bakup/{name}/\n")

