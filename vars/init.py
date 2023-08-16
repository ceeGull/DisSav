# ;Imports
try:
    from GF import *
except ImportError as IE:
    print(f"IMPORT ERROR: {IE}")

# ;Vars
# ; STR
homepath = f'/home/{gp.getuser()}/'
# ; DICT
targetPaths = {
    "config": f"{homepath}.config/",
    "data": f"{homepath}.local/share/",
    "root": "/"
}
# ; BOOL
ro_verbose_mode = True # ;Main.py run() function controls this value just because I'm lazy
# ;Functions
def get_tags(target: list):
    """
    :param target:
    :return result:
    """
    # STR
    result = ""
    # CODE
    if target is not None:
        for tag in target:
            result += f" <{tag}>"
    return result

def homebrew_installed():
    """
    Checks if homebrew is installed
    :return installed:
    """
    # BOOL
    installed = False
    # STR
    whereis = subprocess.run(["whereis", "brew"], capture_output=True, universal_newlines="\n").stdout.split("\n")
    # CODE
    whereis = whereis[0].split(":")[1][1:]
    if getPresSpec(whereis):
        installed = True
        p("Brew has been detected")
    # ;Another Egg was below here :)
    return installed

def flatpak_installed():
    """
    Checks if flatpak is installed
    :return installed:
    """
    # BOOL
    installed = False
    # STR
    whereis = subprocess.run(["whereis", "flatpak"], capture_output=True, universal_newlines="\n").stdout.split("\n")
    # CODE
    whereis = whereis[0].split(":")[1][1:17]
    if getPresSpec(whereis):
        installed = True
        p("Flatpak has been detected")
    # ;Another egg was spotted :)
    return installed

def pip_list_len():
    """
    Gets the length of pip list output which mainly targets the seperator between the fieldnames and values
    :return table_sep:
    """
    # CODE
    table_sep = subprocess.run(["pip", "list"], capture_output=True, universal_newlines="\n").stdout.split("\n")[1]
    return table_sep

# ; Desktop Environments
# ;     KDE-Plasma 5

def get_plasma_wallpapers():
        """
        ######################################################################################################################
        # Grabs all directories from the user's config/plasmarc file and returns a list of directories leading to the files  #
        ######################################################################################################################
        :return plasma_settings_wallpapers:
        """
        # LIST
        profile_contents = []
        profile_contents_filtered = []
        # DICT
        profile_dict = {}
        # CODE
        with open(f'{targetPaths["config"]}plasmarc', "r") as plasmarc_file:
            contents = plasmarc_file.read().split("\n")

        for profile in contents:
            profile_contents.append(profile)
        for index in profile_contents:
            if index in ['']:
                pass
            else:
                profile_contents_filtered.append(index)
        for index in profile_contents_filtered:
            if index.__contains__("[") and index.__contains__("]"):
                profile_name = ""
                for char in index:
                    if char == "[" or char == "]":
                        pass
                    else:
                        profile_name += char
                profile_properties = []
            else:
                profile_properties.append(index.split("="))
            profile_dict.update({profile_name: profile_properties})
        profile_dict["Wallpapers"][0].pop(0)
        plasma_settings_wallpapers = profile_dict["Wallpapers"][0].copy()
        profile_dict["Wallpapers"] = None
        plasma_settings_wallpapers = plasma_settings_wallpapers[0].split(",")
        return plasma_settings_wallpapers

def get_current_plasma_sounds():
    """
    #########################################################################
    # Grabs all KDE Plasma notifyrc SFX targets from the user config folder #
    #########################################################################
    :return:
    """
    # PATH
    cfg_dir = getDir(targetPaths["config"], filter=".notifyrc", alsoIncludeFileName=False, print_dict=False)
    # LIST
    known_sfx = []
    # CODE
    for directory in [cfg_dir[file] for file in cfg_dir]:
        with open(directory, "r") as plasma_sounds_file:
            data = plasma_sounds_file.read()
            contents = data.split("[")
            for props in contents:
                props_content = props.split("]")
                p(f"[props_content] {props_content}", cond=ro_verbose_mode)
                if len(props_content) >= 2:
                    event_name = props_content[0]
                    properties = props_content[1].split("\n")
                    for char in properties:
                        if char == "":
                            properties.pop(properties.index(char))
                        else:
                            property_name_and_values = char.split("=")
                            if property_name_and_values[1] == "":
                                del property_name_and_values
                            elif property_name_and_values[0] == "Sound" and not property_name_and_values[1] in known_sfx:
                                known_sfx.append(property_name_and_values[1])


def grab_application_title_text(**gatto):
    """
    ##############################################################################################################
    # Reads either 'org.kde.plasma.desktop-appletrc' file or 'lattedockrc' and tries to find the appmenu plugin  #
    ##############################################################################################################
    :param gatto:
    :return:
    """
    # GATTO
    gatto_use_plasma_panel = gatto.get("plasma_panel", False) # ;Use 'org.kde.plasma.desktop-appletrc' instead of targeting 'lattedockrc' and the layout linking from that
    # DICT
    plasmoids = {} # ; This will be huge depending on how you configured your DE
    # PATH
    target = f"{targetPaths['config']}lattedockrc"
    latte_dock_presets_path = f"{targetPaths['config']}latte/"
    # NONE
    target_preset = None
    plasmoid_name = None
    # BOOL
    plugin_target_found = False
    # CODE
    if gatto_use_plasma_panel:
        target = f"{targetPaths['config']}plasma-org.kde.plasma.desktop-appletsrc"
        try:
            with open(target, "r") as layout_file:
                for index in [plasmoid for plasmoid in layout_file.read().split("\n")]:
                    if index != '':
                        if index.__contains__("[") and index.__contains__("]") and not index.__contains__("="):
                            section_name = ''
                            for char in index:
                                section_name += char
                            section_props = []
                        else:
                            section_props.append(index.split("=", 1))
                            section_props_dict = {}
                            for value in section_props:
                                section_props_dict.update({value[0]: value[1]})
                            plasmoids.update({section_name: section_props_dict})

            for plasmoid_item in plasmoids:
                if plugin_target_found is True and type(plasmoid_name) is str:
                    if plasmoid_id == "org.communia.apptitle":
                        for plasmoid_item_config in plasmoids[plasmoid_name + "[Configuration][General]"]:
                            if plasmoid_item_config == "noWindowText":
                                if plasmoids[plasmoid_name + "[Configuration][General]"]["noWindowText"] not in ["", "\s"] and plasmoids[plasmoid_name + "[Configuration][General]"]["noWindowText"].isspace() is False:
                                    plasmoid_apptitle_nwt = plasmoids[plasmoid_name + "[Configuration][General]"]["noWindowText"]
                                    if ro_verbose_mode is False:
                                        p(f"Found Apptitle name: {plasmoid_apptitle_nwt}")
                                    else:
                                        p(f"[plasmoid_item_config] Found Apptitle name: {plasmoid_apptitle_nwt}")
                                    return [plasmoid_apptitle_nwt, True]
                            else:
                                plugin_target_found = False
                                p(f"[plasmoid_item_config] Couldn't find 'noWindowText' in '{plasmoid_name}', Looking for another instance of 'org.communia.apptitle'", cond=ro_verbose_mode)
                    elif plasmoid_id == "org.kde.windowtitle":
                        if "filterActivityInfo" in plasmoids[plasmoid_name + "[Configuration][General]"]:
                            for plasmoid_item_config in plasmoids[plasmoid_name + "[Configuration][General]"]:
                                if plasmoid_item_config == "placeHolder":
                                    if plasmoids[plasmoid_name + "[Configuration][General]"]["placeHolder"] not in ["", "\s"] and plasmoids[plasmoid_name + "[Configuration][General]"]["placeHolder"].isspace() is False:
                                        plasmoid_apptitle_nwt = plasmoids[plasmoid_name + "[Configuration][General]"]["placeHolder"]
                                        if ro_verbose_mode is False:
                                            p(f"Found Apptitle name: {plasmoid_apptitle_nwt}")
                                        else:
                                            p(f"[plasmoid_item_config] Found Apptitle name: {plasmoid_apptitle_nwt}")
                                        return [plasmoid_apptitle_nwt, True]
                            else:
                                plugin_target_found = False
                                p(f"[plasmoid_item_config] Couldn't find 'noWindowText' in '{plasmoid_name}', Looking for another instance of 'org.communia.apptitle'", cond=ro_verbose_mode)

                for plasmoid_item_props in plasmoids.get(plasmoid_item):
                    if plasmoid_item_props == "plugin":
                        if plasmoids[plasmoid_item].get(plasmoid_item_props) in ["org.communia.apptitle", "org.kde.windowtitle"]:
                            plugin_target_found = True
                            plasmoid_name = plasmoid_item
                            plasmoid_id = plasmoids[plasmoid_item].get(plasmoid_item_props)
                            p(f"[plasmoid_item_props] App title found in '{plasmoid_item}' with the name being '{plasmoids[plasmoid_item].get(plasmoid_item_props)}'", cond=ro_verbose_mode)
            return [None, False]


        except FileNotFoundError as err:
            p(f"'{err}' not found")
    else:
        try:
            with open(target, "r") as f:
                for new_line in [params for params in f.read().split("\n")]:
                    if new_line.__contains__("currentLayout"):
                        target_preset = new_line.split("=")[-1]
                        p(f"[new_line] Found Latte Dock Preset: {target_preset}", cond=ro_verbose_mode)
                        break

            with open(f"{latte_dock_presets_path}{target_preset}.layout.latte", "r") as layout_file:
                for index in [plasmoid for plasmoid in layout_file.read().split("\n")]:
                    if index != '':
                        if index.__contains__("[") and index.__contains__("]") and not index.__contains__("="):
                            section_name = ''
                            for char in index:
                                section_name += char
                            section_props = []
                        else:
                            section_props.append(index.split("=", 1))
                            section_props_dict = {}
                            for value in section_props:
                                section_props_dict.update({value[0]: value[1]})
                            plasmoids.update({section_name: section_props_dict})

            for plasmoid_item in plasmoids:
                if plugin_target_found is True and type(plasmoid_name) is str:
                    if plasmoid_id == "org.communia.apptitle":
                        for plasmoid_item_config in plasmoids[plasmoid_name + "[Configuration][General]"]:
                            if plasmoid_item_config == "noWindowText":
                                if plasmoids[plasmoid_name + "[Configuration][General]"]["noWindowText"] not in ["", "\s"] and plasmoids[plasmoid_name + "[Configuration][General]"]["noWindowText"].isspace() is False:
                                    plasmoid_apptitle_nwt = plasmoids[plasmoid_name + "[Configuration][General]"]["noWindowText"]
                                    if ro_verbose_mode is False:
                                        p(f"Found Apptitle name: {plasmoid_apptitle_nwt}")
                                    else:
                                        p(f"[plasmoid_item_config] Found Apptitle name: {plasmoid_apptitle_nwt}")
                                    return [plasmoid_apptitle_nwt, True]
                            else:
                                plugin_target_found = False
                                p(f"[plasmoid_item_config] Couldn't find 'noWindowText' in '{plasmoid_name}', Looking for another instance of 'org.communia.apptitle'", cond=ro_verbose_mode)
                    elif plasmoid_id == "org.kde.windowtitle":
                        if "filterActivityInfo" in plasmoids[plasmoid_name + "[Configuration][General]"]:
                            for plasmoid_item_config in plasmoids[plasmoid_name + "[Configuration][General]"]:
                                if plasmoid_item_config == "placeHolder":
                                    if plasmoids[plasmoid_name + "[Configuration][General]"][plasmoid_item_config] not in ["", "\s"] and plasmoids[plasmoid_name + "[Configuration][General]"][plasmoid_item_config].isspace() is False:
                                        plasmoid_apptitle_nwt = plasmoids[plasmoid_name + "[Configuration][General]"][plasmoid_item_config]
                                        if ro_verbose_mode is False:
                                            p(f"Found Apptitle name: {plasmoid_apptitle_nwt}")
                                        else:
                                            p(f"[plasmoid_item_config] Found Apptitle name: {plasmoid_apptitle_nwt}")
                                        return [plasmoid_apptitle_nwt, True]
                            else:
                                plugin_target_found = False
                                p(f"[plasmoid_item_config] Couldn't find 'noWindowText' in '{plasmoid_name}', Looking for another instance of 'org.communia.apptitle'", cond=ro_verbose_mode)

                for plasmoid_item_props in plasmoids.get(plasmoid_item):
                    if plasmoid_item_props == "plugin":
                        if plasmoids[plasmoid_item].get(plasmoid_item_props) in ["org.communia.apptitle", "org.kde.windowtitle"]:
                            plugin_target_found = True
                            plasmoid_name = plasmoid_item
                            plasmoid_id = plasmoids[plasmoid_item].get(plasmoid_item_props)
                            p(f"[plasmoid_item_props] App title found in '{plasmoid_item}' with the name being '{plasmoids[plasmoid_item].get(plasmoid_item_props)}'", cond=ro_verbose_mode)
            return [None, False]

        except FileNotFoundError as err:
            p(f"'{err}' not found")


def get_current_plasma_sounds():
    """
##########################
# Grabs all used sounds  #
##########################
    :return known_sfx:
    """
    # PATH
    cfg_dir = getDir(targetPaths["config"], filter=".notifyrc", alsoIncludeFileName=False, print_dict=False)
    # LIST
    known_sfx = []
    # CODE
    with open("/etc/sddm.conf.d/kde_settings.conf", "r") as sddm_configuration:
        data = sddm_configuration.read().split("\n")
        counter = 0
        theme_index = 0
        theme_section_end_index = 0
        switch = False
        for var in data:
            if var not in ["", " "]:
                if var == "[Theme]":
                    theme_index = counter+1
                    switch = True
                if switch:
                    if var != "[Theme]" and var[0] == "[":
                        theme_section_end_index = counter-1
                        switch = False
            counter += 1

        sddm_theme_configuration = data[theme_index:theme_section_end_index]
        if sddm_theme_configuration[-1] in ["", " "]:
            sddm_theme_configuration.pop(-1)
        for i in sddm_theme_configuration:
            var = i.split("=")[0].lower()
            value = i.split("=")[1]
            vars().update({var: value})

        with open(f"/usr/share/sddm/themes/{vars()['current']}/Main.qml", "r") as sddm_theme:
            main_qml = sddm_theme.read().split("\n")
            for line in main_qml:
                if line.__contains__("SoundEffect"):
                    qml_sfx = line.split("{")[1].split("}")[0].split(";")
                    if qml_sfx[0].split(":")[1][0] == " ":
                        identifier = qml_sfx[0].split(":")[1][1:]
                    else:
                        identifier = qml_sfx[0].split(":")[1]
                    if qml_sfx[1].split(":")[1][0] == " ":
                        source = qml_sfx[1].split(":")[1][1:]
                    else:
                        source = qml_sfx[1].split(":")[1]
                    if not source.__contains__(identifier) and source.__contains__('"'):
                        source = source.split('"')[1]
                        known_sfx.append(f"/usr/share/sddm/themes/{vars()['current']}/{source}")

    with open(f"/home/{gp.getuser()}/.bash_profile", "r") as bash_profile:
        contents = bash_profile.read().split("\n")
        for command in contents:
            if command.__contains__("    mpv"):
                arguments = command.split('"')
                arguments.pop(-1)
                window_maker_startup_sound = arguments[-1]
        if "window_maker_startup_sound" in vars():
            known_sfx.append(window_maker_startup_sound)
    for directory in [cfg_dir[file] for file in cfg_dir]:
        with open(directory, "r") as plasma_sounds_file:
            data = plasma_sounds_file.read()
            contents = data.split("[")
            for props in contents:
                props_content = props.split("]")
                p(f"[props_content] {props_content}", cond=ro_verbose_mode)
                if len(props_content) >= 2:
                    event_name = props_content[0]
                    properties = props_content[1].split("\n")
                    for char in properties:
                        if char == "":
                            properties.pop(properties.index(char))
                        else:
                            property_name_and_values = char.split("=")
                            if property_name_and_values[1] == "":
                                del property_name_and_values
                            elif property_name_and_values[0] == "Sound" and not property_name_and_values[1] in known_sfx:
                                known_sfx.append(property_name_and_values[1])
    return known_sfx

# ; Web Browsers
# ;     Gecko Engine
# ;         Mozilla FireFox
def get_current_firefox_profile():
    """
#############################################################################
# Grabs the current user's Mozilla Firefox default profile and returns the  #
# current Firefox profile folder as a string by looking through the file    #
# called 'profiles.ini' in the user's '.mozilla/firefox/' folder            #
#############################################################################
    :return profile_folder:
    """
    # LIST
    profile_contents = []
    profile_contents_filtered = []
    # DICT
    profile_dict = {}
    # NONE
    profile_folder = None
    # CODE
    with open(homepath+".mozilla/firefox/profiles.ini") as profiles_file:
        contents = profiles_file.read().split("\n")

    for profile in contents:
        profile_contents.append(profile)

    for index in profile_contents:
        if index in ['']:
            pass
        else:
            profile_contents_filtered.append(index)

    for index in profile_contents_filtered:
        if index.__contains__("[") and index.__contains__("]"):
            profile_name = ""
            for char in index:
                if char == "[" or char == "]":
                    pass
                else:
                    profile_name += char
            profile_properties = []
        else:
            profile_properties.append(index.split("="))
        profile_dict.update({profile_name: profile_properties})

    for profile in profile_dict:
        for profile_props in profile_dict[profile]:
            if profile_props[0] == "Locked" and profile_props[1].isnumeric():
                profile_default_value = int(profile_props[1])
                if profile_default_value == 1:
                    profile_look_into = profile
                    p(f"[profile_props] Found Default Profile: {profile_look_into}", cond=ro_verbose_mode)
                    if ro_verbose_mode:
                        for v in profile_dict[profile_look_into]:
                            p(f"\t{v[0]}: {v[1]}")
            elif profile_props[0] == "Default" and profile_props[1].isnumeric():
                profile_default_value = int(profile_props[1])
                if profile_default_value == 1:
                    profile_look_into = profile
                    p(f"[profile_props] Found Default Profile: {profile_look_into}", cond=ro_verbose_mode)
                    if ro_verbose_mode:
                        for v in profile_dict[profile_look_into]:
                            p(f"\t{v[0]}: {v[1]}")
    for profile_values in profile_dict[profile_look_into]:
        if profile_values[0] == "Default" and profile_values[1] is not profile_values[1].isnumeric():
            profile_folder = profile_values[1]
            break
        elif profile_values[0] == "Path":
            profile_folder = profile_values[1]
            break
    del profile_contents, profile_contents_filtered, profile_default_value, profile_look_into
    return profile_folder

# ;         Librewolf
def get_current_librewolf_profile():
    """
#########################################################################################################################
# Identifies what browser profile the user is currently using in which returns a string containing the current default, #
# pretty much the same thing as 'get_current_firefox_profile()' function.                                               #
#########################################################################################################################
    :return profile_folder:
    """
    # LIST
    profile_contents = []
    profile_contents_filtered = []
    # DICT
    profile_dict = {}
    # NONE
    profile_folder = None
    # CODE
    with open(homepath+".librewolf/profiles.ini") as profiles_file:
        contents = profiles_file.read().split("\n")

    for profile in contents:
        profile_contents.append(profile)
    for index in profile_contents:
        if index in ['']:
            pass
        else:
            profile_contents_filtered.append(index)
    for index in profile_contents_filtered:
        if index.__contains__("[") and index.__contains__("]"):
            profile_name = ""
            for char in index:
                if char == "[" or char == "]":
                    pass
                else:
                    profile_name += char
            profile_properties = []
        else:
            profile_properties.append(index.split("="))
        profile_dict.update({profile_name: profile_properties})
    for profile in profile_dict:
        for profile_props in profile_dict[profile]:
            if profile_props[0] == "Locked" and profile_props[1].isnumeric():
                profile_default_value = int(profile_props[1])
                if profile_default_value == 1:
                    profile_look_into = profile
                    p(f"[profile_props] Found Default Profile: {profile_look_into}", cond=ro_verbose_mode)
                    if ro_verbose_mode:
                        for v in profile_dict[profile_look_into]:
                            p(f"\t{v[0]}: {v[1]}")
            elif profile_props[0] == "Default" and profile_props[1].isnumeric():
                profile_default_value = int(profile_props[1])
                if profile_default_value == 1:
                    profile_look_into = profile
                    p(f"[profile_props] Found Default Profile: {profile_look_into}", cond=ro_verbose_mode)
                    if ro_verbose_mode:
                        for v in profile_dict[profile_look_into]:
                            p(f"\t{v[0]}: {v[1]}")
    for profile_values in profile_dict[profile_look_into]:
        if profile_values[0] == "Default" and profile_values[1] is not profile_values[1].isnumeric():
            profile_folder = profile_values[1]
            break
        elif profile_values[0] == "Path":
            profile_folder = profile_values[1]
            break
    del profile_contents, profile_contents_filtered, profile_default_value, profile_look_into
    return profile_folder

# ;An egg was below here :)
