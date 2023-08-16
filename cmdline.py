#!/usr/bin/env python3

#################################################################################
#                                 cmdline.py                                    #
#-------------------------------------------------------------------------------#
# By             | cGull                                                        #
# Date           | November 4, 2022 (11/04/2022)                                #
# Version        | 1.1.7 Panda                                                  #
# Version (Main) | 2.0.3 (5.8)                                                  #
# Source Code    | I don't know when but it will be open                        #
#################################################################################

try:
    from GF import p, flp, makeBox, genIterList, GF_VERSION, GF_EDITION, GF_EDITION_SHORT, sysDetect
    from main import run, version_main
    from sys import *
    import getopt
    import os
except ImportError as gfNotFound:
    print(f"Gull/Panda Framework or in it is not found \n{gfNotFound}")

def init_cmd_opt():
    """
####################################
# Creates a dictionary that's all. #
####################################

    :return:
    """
    # CODE
    return {"short": {}, "long": {}}

def main(argv):
    """
#############################################################################
#                               Main Function                               #
#---------------------------------------------------------------------------#
# Acts like a simple but mainly complicated command-line program            #
# (Unix-like) just follows a series of checks and info, it also includes    #
# '-h' (help) argument data.                                                #
#############################################################################

    :param argv:
    :return:
    """
    # INIT
    op = init_cmd_opt()
    # STR
    version = '1.1.7 Command-line Python Program, Panda'
    help_file = ''
    # BOOL
    # ;True
    ips_enable = True
    ipw_enable = True
    # ;False
    verbose_mode = False
    test_mode = False
    link_icons = False
    ipw_enable_link = False
    ips_enable_link = False
    use_apptitle = False
    use_apptitle_plasma_panel = False
    save_packages_installed = False
    take_screenshot = False
    # LIST
    contents = genIterList(2)
    # NONE
    name = None
    # DICT
    descs = {
        0: "Info (Default options)",
        1: ['--ver\n--version', "\t\tPrints script's version."],
        2: ['\n-h', "\t\t\tShows Help"],
        3: "Non-commandline options (Program specific options)",
        4: ['\n--name', '\t\t\tName of backup'],
        5: ['\n--test-mode', '\t\tEnables test mode'],
        6: ['\n--link_icons', "\t\tDon't copy the icons folder link it"],
        7: ['\n--dipw', "\t\t\tSkips copying/linking of Plasma Wallpapers (Grabs it from plasmarc)"],
        8: ['\n--link_wall', "\t\tLinks Plasma Wallpapers instead of copying them (only executes when --dipw isn't used)"],
        9: ['\n--dips', "\t\t\tSkips copying/linking of current Plasma Sounds (grabs all files from the current user's config files with anything that has the '.notifyrc' file extentsion)"],
        10: ['\n--link_sfx', "\t\tLinks current Plasma Sounds instead of copying them (only executes when --dipw isn't used)"],
        11: ['\n--use_apptitle', "\t\tOverrides 'Name' with scanned current layout of KDE Plasma using 'lattedockrc' or 'plasma-org.kde.plasma.desktop-appletrc' (NOTE: You need an app title plasmoid to use this mainly look for 'org.communia.apptitle)'"],
        12: ['\n\t--use_kpanel', "\t\t (short for KDE Plasma Panel) uses 'plasma-org.kde.plasma.desktop-appletrc' instead of 'lattedockrc"],
        13: ['\n-sp', "\t\t(short for Save Packages) YOU NEED APT OR PACMAN INSTALLED"],
        14: ['\n   --save-packages', "\tAlias for -sp"],
        15: ['\n-ts', "\t\t\t(short for Take Screenshot) YOU NEED SPECTACLE INSTALLED, Takes screenshot of the entire screen as reference to what the backup looks like"],
        16: ['\n   --take-screenshot', "\tAlias for -ts"],
        17: "DisSav Functions (Make it from a file example file is in the main directory)",
        18: ['\nF()', "\tget_current_firefox_profile() --> firefox profile"],
        19: ['\nL()', "\tget_current_librewolf_profile() --> Librewolf profile"],
        20: ['\nS()', "\tget_current_plasma_sounds()"],
        21: ['\nI()', "\tgrabs (/usr/share/icons, /usr/share/WindowMaker/Icons and user icons)"]
    }
    # CODE
    
    def short(cmd, opt, b):
        # CODE
        op['short'].update({cmd: [opt, b]})

    def long(cmd, opt, b):
        # CODE
        op['long'].update({cmd: [opt, b]})
    
    # ;if 1, then require argument
    # ;if 0, then acts like command-line function with no arguments
    short("v", "v", 0)  # ;Prints Everything
    short("h", "h", 0)  # ;Shows Help
    short("sp", "sp", 0)
    short("ts", "ts", 0)
    long("version", 'ver,version', 0)  # ;Prints the version of this script
    long("name", 'name', 1) # ;Name of Backup
    long("test mode", 'test-mode', 0) # ;Enables test mode
    long("link_icons", "link_icons", 0) # ;link icons
    long("dipw", "dipw", 0) # ;Skips the adding/linking of plasmarc wallpapers
    long("link_wall", "link_wall", 0) # ;links plasmarc wallpapers instead of copying them (REQUIRES --DIPW TO NOT BE USED)
    long("dips", "dips", 0) # ;Skips the adding/linking of Plasma sounds
    long("link_sfx", "link_sfx", 0) # ;Links the current Plasma sounds instead of copying them (REQUIRES --DIPS TO NOT BE USED)
    long("use_apptitle", "use_apptitle", 0)
    long("use_kpanel", "use_kpanel", 0)
    long("save-packages", "save-packages", 0)
    long("take-screenshot", "take-screenshot", 0)
    makeBox(os.getcwd())

    def check(var, sender, r1, r2, **kwargs):
        """
        Honestly I forgot what this actually does

        :param var:
        :param sender:
        :param r1:
        :param r2:
        :param kwargs:
        :return:
        """
        # KWARGS
        send_to_list = kwargs.get("send_to_list", False)
        # CODE
        try:
            if send_to_list is False:
                if var[1] == 1:
                    sender += r1
                else:
                    sender += r2
            else:
                if var[1] == 1:
                    sender.append(r1)
                else:
                    sender.append(r2)
        except TypeError as fdl_terr:
            p(f"var: {var}")
            p(fdl_terr)
        return sender

    for cat in op:
        if cat == 'short':
                s = ''
        elif cat == "long":
            l = []
        point = op[cat]
        for option in point:
            v = point[option]
            if cat == 'short':
                s = check(v, s, f'{v[0]}:', f'{v[0]}')
                contents[0] += 1
            elif cat == 'long':
                if v[0].__contains__(','):
                    mo = v[0].split(',')
                    for ao in mo:
                        check(v, l, f'{ao}=', f'{ao}', send_to_list=True)
                    contents[1] += 1
                else:
                    check(v, l, f'{v[0]}=', f'{v[0]}', send_to_list=True)
                    contents[1] += 1

    try:
        opts, args = getopt.getopt(argv, s, l)
    except getopt.GetoptError as goe:
        makeBox("Syntax: save-config <NAME> <options>")
        p(goe)
        exit(2)

    for opt, arg in opts:
        # ;options (no argument required)
        if opt == '-h':
            makeBox(os.getcwd())
            for o in descs:
                help_file_cmd = descs[o]
                help_file_cmd_prev_is_string = False
                help_file_cmd_prev_is_list = False
                if o - 1 != -1:
                    if type(descs[o - 1]) is str:
                        help_file_cmd_prev_is_string = True
                    if type(descs[o - 1]) is list:
                        help_file_cmd_prev_is_list = True
                if type(descs[o]) is list:
                    for c in help_file_cmd:
                        if help_file_cmd_prev_is_string:
                            help_file += f"\n{c}"
                            help_file_cmd_prev_is_string = False
                        else:
                            help_file += f"{c}"
                elif type(descs[o]) is str:
                    if help_file_cmd_prev_is_list:
                        help_file += f"\n\n{makeBox(descs[o], no_print=True)}"
                    else:
                        help_file += f"{makeBox(descs[o], no_print=True)}\n"
            p('\n' + help_file + "\n")
            makeBox(str(contents))
            p('\n')
            exit(0)
        if opt in ['--ver', '--version']:
            for script in [version_main, version, f"Panda Framework {GF_VERSION} {GF_EDITION_SHORT}"]:
                makeBox(script)
            exit(0)
        # ;options
        if opt == '-v':
            verbose_mode = True
        if opt == '--name':
            name = arg
        if opt == '--test-mode':
            test_mode = True
        if opt == '--link_icons':
            link_icons = True
        if opt == '--dipw':
            ipw_enable = False
        if opt == '--link_wall':
            if ipw_enable:
                ipw_enable_link = True
        if opt == '--dips':
            ips_enable = False
        if opt == '--link_wall':
            if ips_enable:
                ips_enable_link = True
        if opt == '--use_apptitle':
            use_apptitle = True
        if opt == descs[12][0][len("\n\t"):] and use_apptitle is True:
            use_apptitle_plasma_panel = True
        if opt in ["-sp", "--save-packages"]:
            save_packages_installed = True
        if opt in ["-ts", "--take-screenshot"]:
            take_screenshot = True

    if name is not None or name != "":
        run(name=name,
            verbose_mode=verbose_mode,
            testmode=test_mode,
            no_copy_icons=link_icons,
            include_plasma_wallpapers=ipw_enable,
            link_p_w=ipw_enable_link,
            include_plasma_system_sounds=ips_enable,
            link_p_s=ips_enable_link,
            use_apptitle=use_apptitle,
            use_plasma_panel=use_apptitle_plasma_panel,
            include_packages=save_packages_installed,
            screenshot=take_screenshot
        )
    elif use_apptitle:
        run(verbose_mode=verbose_mode,
            testmode=test_mode,
            no_copy_icons=link_icons,
            include_plasma_wallpapers=ipw_enable,
            link_p_w=ipw_enable_link,
            include_plasma_system_sounds=ips_enable,
            link_p_s=ips_enable_link,
            use_apptitle=use_apptitle,
            use_plasma_panel=use_apptitle_plasma_panel,
            include_packages=save_packages_installed,
            screenshot=take_screenshot
        )


if __name__ == "__main__":
    main(argv[1:])
